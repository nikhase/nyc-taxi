$(document).ready(function(){
console.log("loaded")
    
    $('#btnGetGeo').click(function(){
        var requestStart = $('#autocomplete').val() + "&key=AIzaSyA_MF2DqEyP732LOONDdJ0du_oaxii_8JE";  //Val Function to retrieve Value
        var requestEnd = $('#autocomplete2').val() + "&key=AIzaSyA_MF2DqEyP732LOONDdJ0du_oaxii_8JE";
        var resultStart = $('#resultDivStart');
        var resultEnd = $('#resultDivEnd');

        $.ajax({
            url: "https://maps.googleapis.com/maps/api/geocode/json",
            method: 'get',                      //request type
            data: {address: requestStart},      //property name address, data to be stend to the server: requestStart
            dataType: 'json',                   //data we are expecting back from the server
            success: function(data) {           //callback funktion
                resultStart.html("Startpoint: </br>Latitude " + data.results[0].geometry.location.lat + "</br>" + 'Longitude ' + data.results[0].geometry.location.lng);
            }
        });

        $.ajax({
            url: "https://maps.googleapis.com/maps/api/geocode/json",
            method: 'get',
            data: {address: requestEnd},
            dataType: 'json',
            success: function(data) {
                resultEnd.html("Endpoint: </br>Latitude " + data.results[0].geometry.location.lat + "</br>" + 'Longitude ' + data.results[0].geometry.location.lng);
            }
        });
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
  autocomplete.addListener('place_changed', function() {
    fillInAddress(autocomplete, "");
  });

  autocomplete2 = new google.maps.places.Autocomplete(
    /** @type {!HTMLInputElement} */
    (document.getElementById('autocomplete2')), {
      types: ['geocode']
    });
  autocomplete2.addListener('place_changed', function() {
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
google.maps.event.addDomListener(window, "load", initAutocomplete);

function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
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

