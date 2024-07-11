function updateOwnData(){
    $.get("/fill_personal_info",function(data){
        const target = document.querySelectorAll(".box-x");
        target.forEach((elem)=>{
            if(elem.classList.contains('dur')){
                const duration = data.dur;
                const seconds = duration%60;
                const minutes = Math.floor(Math.floor(duration/60)%60);
                const hours = Math.floor(Math.floor(duration/(60*60)));
                let formatedData = `${formatt(hours)}:${formatt(minutes) }:${formatt(seconds)}`;
                elem.textContent=formatedData;
            }
            else if(elem.classList.contains('rate'))
                {
                    const formatedData = parseFloat(data.rate.toFixed(4));
                    elem.textContent = formatedData + " MB/Minute";
                }
            else if(elem.classList.contains('lim')){
                const limit = data.limit;
                var formatted = parseFloat(limit.toFixed(2));
                elem.value =  formatted;
            }
            else{
                elem.textContent = data.use;
                var odometerElement = new Odometer({
                    el: elem,
                    value: data.use,
                    format: '(,ddd)', 
                    theme: 'minimal', 
                    });
            
                odometerElement.update(data.use);
            }
        })
    })
}

updateOwnData();


setInterval(updateOwnData, 100);

function formatt(number){
    if(number<10)return `0${number}`;
    return number;
}