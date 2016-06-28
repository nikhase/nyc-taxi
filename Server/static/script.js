$(document).ready(function () {
    console.log("loaded")

    $('#btnGetGeo').click(function () {
        // Empty Error Textfield
        $('#errorBox').hide();
        $('#errortext').text("");

        $("#green").hide();
        $("#orange").hide();
        $("#red").hide();

        $("#map").empty()

        if (($('#autocomplete').val() == "") || $('#autocomplete2').val() == "") {
            // Set Error
            $('#errorBox').show();
            $('#errortext').text("Ups, you did not enter the correct info!");

        }
        else {


            var requestStart = $('#autocomplete').val() + "&key=AIzaSyA_MF2DqEyP732LOONDdJ0du_oaxii_8JE";  //Val Function to retrieve Value

            // Problem when the autocomplete reuslt is too exact
            // Only take Name/Address , City
            requestStartParts = requestStart.split(',');
            if (requestStartParts.length >= 3) {
                requestStart = requestStartParts[0] + "," + requestStartParts[1];
            }
            console.log(requestStart)
            var requestEnd = $('#autocomplete2').val() + "&key=AIzaSyA_MF2DqEyP732LOONDdJ0du_oaxii_8JE";
            requestEndParts = requestEnd.split(',');
            if (requestEndParts.length >= 3) {
                requestEnd = requestEndParts[0] + "," + requestEndParts[1];
            }
            console.log(requestEnd)
            var cartime = $('#cartime');
            var realtime = $('#realtime_traffic');
            var historic = $('#historic_traffic');
            var biketime = $('#biketime');
            var walkingtime = $('#walkingtime');
            var cab_price = $('#cab_price');
            var uberx_price = $('#uberx_price');
            var uberxl_price = $('#uberxl_price');
            var ubersuv_price = $('#ubersuv_price');
            var uberblack_price = $('#uberblack_price');
            var bike_price = $('#bike_price');
            var walking_calories = $('#walking_calories');
            var bike_calories = $('#bike_calories');
            var timestamp = $('#timestamp');
            var lighttaxi = $('#lighttaxi');
            var distanceEst = $('#distanceEstimation');




            // https://maps.googleapis.com/maps/api/geocode/json ?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyA_MF2DqEyP732LOONDdJ0du_oaxii_8JE
            $.ajax({
                url: "https://maps.googleapis.com/maps/api/geocode/json",
                method: 'get',                      //request type
                data: {address: requestStart},      //property name address, data to be stend to the server: requestStart
                dataType: 'json',                   //data we are expecting back from the server
                success: function (data) {           //callback funktion
                    //  resultStart.html("Startpoint: </br>Latitude " + data.results[0].geometry.location.lat + "</br>" + 'Longitude ' + data.results[0].geometry.location.lng);
                    lata = data.results[0].geometry.location.lat;
                    lga = data.results[0].geometry.location.lng;

                    $.ajax({
                        url: "https://maps.googleapis.com/maps/api/geocode/json",
                        method: 'get',
                        data: {address: requestEnd},
                        dataType: 'json',
                        success: function (data) {
                            //   resultEnd.html("Endpoint: </br>Latitude " + data.results[0].geometry.location.lat + "</br>" + 'Longitude ' + data.results[0].geometry.location.lng);
                            latb = data.results[0].geometry.location.lat;
                            lgb = data.results[0].geometry.location.lng;
                            geo = "lata=" + lata + "&lga=" + lga + "&latb=" + latb + "&lgb=" + lgb;
                            //link.html("http://localhost:5000/search?lata=" + lata +"&lga=" + lga + "&latb=" + latb + "&lgb=" + lgb);
                            // http://127.0.0.1:5000/search?lta=40.770475&lga=-73.879504&ltb=40.751573&lgb=-73.991857

                            if (typeof lata !== "undefined" && typeof latb !== "undefined" && typeof lga !== "undefined" && typeof lgb !== "undefined") {
                                $.ajax({
                                    url: "/search?" + geo,
                                    method: 'get',
                                    success: function (data) {
                                        cartime.html(data.taxi.historic);
                                        realtime.html(data.taxi.realtime);
                                        historic.html(data.taxi.historic);
                                        cab_price.html("$ " + data.prices.yellow_cab);
                                        uberblack_price.html("$ " + data.prices.uberBlack);
                                        ubersuv_price.html("$ " + data.prices.uberSUV);
                                        uberx_price.html("$ " + data.prices.uberX);
                                        uberxl_price.html("$ " + data.prices.uberXL);


                                        biketime.html(data.bike.historic);
                                        bike_calories.html(data.calories.bike);
                                        bike_price.html("$ " + data.prices.citibike);

                                        walkingtime.html(data.walking.estimation);
                                        walking_calories.html(data.calories.walking);

                                        timestamp.html(data.info.timestamp);
                                        distanceEst.html(data.estimated_distance + " Miles");


                                        //NEED TO TRANSFORM STRING TO DATETIME
                                        var histMin = parseInt(data.taxi.historic.split(":")[0] * 60 + data.taxi.historic.split(":")[1]);
                                        var realMin = parseInt(data.taxi.realtime.split(":")[0] * 60 + data.taxi.realtime.split(":")[1]);
                                        //console.log(histMin)
                                        //console.log(realMin + 5)

                                        if ((realMin <= 1.25 * histMin)) {
                                            $("#green").show();
                                        }
                                        else if ((realMin <= 1.5 * histMin) && (realMin > 1.25 * histMin)) {

                                            $("#orange").show();
                                        }
                                        else {
                                            $("#red").show();
                                        }



                                        //Go to second page
                                        window.location = "#secondpage";

                                    },
                                    error: function () {
                                        $('#errorBox').show();
                                        $('#errortext').text("Sorry, something went wrong handling your request. Please try again!");
                                    }
                                })
                            }
                            else {
                                $('#errorBox').show();
                                $('#errortext').text("Not so fast! Search Again");
                            }
                        }
                    });
                }
            });
        }

    });
})

var placeSearch, autocomplete, autocomplete2;
var componentForm = {
    street_number: 'short_name',
    route: 'long_name',
    locality: 'long_name',
    administrative_area_level_1: 'short_name',
    country: 'long_name',
    postal_code: 'short_name'
};

function addMap()
{
    console.log("Init Map")
    //Prepare Map
    var myLatLng = {lat: 40.773382, lng: -73.982392};


    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: myLatLng
    });

    var a = {lat: lata, lng: lga};

    var markerA = new google.maps.Marker({
          position: a,
          map: map,
    });

    var b = {lat: latb, lng: lgb};

    var markerB = new google.maps.Marker({
          position: b,
          map: map,
    });

}

function initAutocomplete() {
    // Create the autocomplete object, restricting the search to geographical
    // location types.
    autocomplete = new google.maps.places.Autocomplete(
        /** @type {!HTMLInputElement} */
        (document.getElementById('autocomplete')), {
            types: ['geocode']
        });

    // When the user selects an address from the dropdown, populate the address
    // fields in the form.
    autocomplete.addListener('place_changed', function () {
        fillInAddress(autocomplete, "");
    });

    autocomplete2 = new google.maps.places.Autocomplete(
        /** @type {!HTMLInputElement} */
        (document.getElementById('autocomplete2')), {
            types: ['geocode']
        });
    autocomplete2.addListener('place_changed', function () {
        fillInAddress(autocomplete2, "2");
    });

}

function fillInAddress(autocomplete, unique) {
    // Get the place details from the autocomplete object.
    var place = autocomplete.getPlace();

    for (var component in componentForm) {
        if (!!document.getElementById(component + unique)) {
            document.getElementById(component + unique).value = '';
            document.getElementById(component + unique).disabled = false;
        }
    }

    // Get each component of the address from the place details
    // and fill the corresponding field on the form.
    for (var i = 0; i < place.address_components.length; i++) {
        var addressType = place.address_components[i].types[0];
        if (componentForm[addressType] && document.getElementById(addressType + unique)) {
            var val = place.address_components[i][componentForm[addressType]];
            document.getElementById(addressType + unique).value = val;
        }
    }
}
//google.maps.event.addDomListener(window, "load", initAutocomplete);

function geolocate() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var geolocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            var circle = new google.maps.Circle({
                center: geolocation,
                radius: position.coords.accuracy
            });
            autocomplete.setBounds(circle.getBounds());
        });
    }
}

