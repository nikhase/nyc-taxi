$(document).ready(function(){
    console.log("loaded")

    $('#btnGetGeo').click(function(){
        var requestStart = $('#txtstart').val() + "&key=AIzaSyA_MF2DqEyP732LOONDdJ0du_oaxii_8JE";  //Val Function to retrieve Value
        var requestEnd = $('#txtend').val();
        var resultElement = $('#resultDiv');
        console.log("Button wurde geklicked.")
        $.ajax({
            url: "https://maps.googleapis.com/maps/api/geocode/json",
            method: 'get',                      //request type
            data: {address: requestStart},      //property name address, data to be send to the server: requestStart
            dataType: 'json',                   //data we are expecting back from the server
            success: function(data) {           //callback function
                 resultElement.html('Result' + data.results[0].address_components[0].long_name);
            }
        });
        //Test
        // TEST
        // https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyA_MF2DqEyP732LOONDdJ0du_oaxii_8JE
        // key: AIzaSyA_MF2DqEyP732LOONDdJ0du_oaxii_8JE
    });
})


