$(document).ready(function () {
    $('#switch').change(function () {
        var state = $(this).prop('checked') ? 'on' : 'off';
        $.ajax({
            url: '/toggle',
            method: 'POST',
            data: { state: state },
            statusCode: {
                204: function () {
                    console.log('LED state updated successfully.');
                }
            }
        });
    });

    $('#switch1').change(function () {
        var state = $(this).prop('checked') ? 'on' : 'off';
        $.ajax({
            url: '/toggle2',
            method: 'POST',
            data: { state: state },
            statusCode: {
                204: function () {
                    console.log('Button 2 state updated successfully.');
                }
            }
        });
    });

    $('#switch3').change(function () {
        var state = $(this).prop('checked') ? 'on' : 'off';
        $.ajax({
            url: '/toggle3',
            method: 'POST',
            data: { state: state },
            statusCode: {
                204: function () {
                    console.log('Button 3 state updated successfully.');
                }
            }
        });
    });
});






function changeText() {
    x= document.getElementById('text')
    if (x.innerHTML === 'LIGHT IS TURN OFF'){
      x.innerHTML = "LIGHTS IS TURN ON";
    }
    else{
      x.innerHTML = "LIGHT IS TURN OFF";
    }
  }

  function changeText1() {
    x= document.getElementById('text1');
    if (x.innerHTML === 'LIGHT-1 IS TURN OFF'){
      x.innerHTML = "LIGHTS-1 IS TURN ON";
    }
    else{
      x.innerHTML = "LIGHT-1 IS TURN OFF";
    }
  }

  function changeText2() {
    x= document.getElementById('text2');
    if (x.innerHTML === 'FAN IS TURN OFF'){
      x.innerHTML = "FAN  IS TURN ON";
    }
    else{
      x.innerHTML = "FAN IS TURN OFF";
    }
  }




 





