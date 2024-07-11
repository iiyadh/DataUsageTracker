from flask import Flask, render_template,jsonify,request,redirect,url_for,session
from scapy.all import sniff, IP, Ether
from threading import Thread
import time

app = Flask(__name__)
app.secret_key = 'blabla'


data_usage = []
personal_info = {}
timee = int(time.time())
limitvalue = 0
actuel_data_usage = -1
Is_In_mode = False





def packet_callback(packet):
    if IP in packet and Ether in packet:
        src_ether = packet[Ether].src
        src_ip = packet[IP].src
        length = len(packet)
        
        user_ind = get_index_of_user(data_usage,'mac',src_ether)
        if user_ind != -1:
            data_usage[user_ind]['data'] += length
        else:
            data_usage.append({
                'mac' : src_ether,
                'ip':src_ip,
                'data':length
            })

def get_index_of_user(data_usage, key, value):
    for user in range(len(data_usage)):
        if data_usage[user].get(key) == value:
            return user
    return -1

  
@app.route('/fill_personal_info')
def fill_personal_info():
    global personal_info
    global limitvalue
    global actuel_data_usage
    global Is_In_mode
    sum = 0
    for dataU in data_usage:
        sum += dataU["data"]
    personal_info["use"] = sum/1024**2    
    elaps = int(time.time()) - timee
    if elaps > 0 :
        rate = ((sum/1024**2)/(elaps/60))
        personal_info["rate"]= rate
    else :
        personal_info["rate"]= 0
        personal_info["use"] = 0
    personal_info["dur"] = elaps
    res = float(limitvalue) - (float(personal_info["use"]) -  float(actuel_data_usage))
    if res > 0 :
        personal_info["limit"] = res
    else:
        if Is_In_mode:
            Is_In_mode = False
        personal_info["limit"] = 0
    return jsonify(personal_info)

@app.route('/')
def index():
    return redirect(url_for('dashboard'))



@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',limita = limitvalue,modee = Is_In_mode)

@app.route("/dashboard/limit", methods=['GET', 'POST'])
def set_limit():
    global limitvalue
    global actuel_data_usage
    global personal_info
    global Is_In_mode
    if request.method == "POST":
        Is_In_mode =True
        limitvalue = request.form['myInput2']
        if "use" in personal_info :
            actuel_data_usage = personal_info["use"]
        else:
            actuel_data_usage = 0
    return redirect(url_for('dashboard'))

@app.route("/dashboard/cancel" , methods=['GET', 'POST'])
def remove_limit():
    global limitvalue
    global actuel_data_usage
    global personal_info
    global Is_In_mode
    if request.method == "POST":
        Is_In_mode = False
        limitvalue = 0
        actuel_data_usage = 0
    return redirect(url_for('dashboard'))

def capture_packets():
    sniff(prn=packet_callback, store=0)

capture_thread = Thread(target=capture_packets)
capture_thread.start()

@app.route('/get_data')
def get_data():
    return jsonify(data_usage)

if __name__ == '__main__':
    app.run(debug=True)
