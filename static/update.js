  // Function to update data using AJAX
  function updateData() {
    $.get('/get_data', function(data) {
      const row = document.querySelectorAll('tr');

      if (data.length >= row.length && data.length > 0) {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `<td class='ip'>${data[row.length-1].ip}</td>
          <td class='mac'>${data[row.length-1].mac.toUpperCase()}</td>
          <td class='data odometer'>${data[row.length-1].data / (1024 * 1024)}</td>`;
        document.querySelector('tbody').appendChild(newRow);
      } else {
        const target = document.querySelectorAll('.data');

        for (let i = 0; i < data.length; i++) {
          var number = data[i].data / (1024 * 1024);
          var formatted = parseFloat(number.toFixed(4));

          // Use odometer to animate the update
          var odometerElement = new Odometer({
            el: target[i], // Target the specific odometer element
            value: formatted,
            format: '(,ddd).dddd', // Format as needed
            theme: 'minimal', // Choose a theme
          });

          odometerElement.update(formatted);
        }
      }
    });
  }
  updateData();


  setInterval(updateData, 100);