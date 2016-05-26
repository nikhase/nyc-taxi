$(document).ready(function(){
    console.log("loaded")

    $('#nextbtn').click( function(){
    	console.log("Button wurde geklicked.")

        $.getJSON( "/search?q=12", function (data) {
            console.log(data.toString());
        });
    });


	

})

