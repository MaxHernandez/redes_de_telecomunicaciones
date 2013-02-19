var map;
var pos;

function get_random_color() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.round(Math.random() * 15)];
    }
    return color;
}

function draw_circle(radio, essid, signal){
    var conf = {
	strokeColor: get_random_color(),
	strokeOpacity: 0.3,
	strokeWeight: 1,
	fillColor: get_random_color(),
	fillOpacity: 0.7,
	map: map,
	center: pos,
	radius: radio
    };
    circle = new google.maps.Circle(conf);
    google.maps.event.addListener(circle, 'click', function() {
	    description = document.getElementById('description');
	    description.innerHTML = ('<b>ESSID:</b> '+essid+'<br/>');
	    description.innerHTML += ('<b>Nivel de se&ntilde;al:</b> '+signal+' dBm<br/>');
	    description.innerHTML += ('<b>Distancia aproximada de la red:</b> '+radio+' metros<br/>');
	});
}

function main(redes) {
    map = new google.maps.Map(document.getElementById("mapa"));
    map.setZoom(19);
    map.setMapTypeId(google.maps.MapTypeId.HYBRID);
    navigator.geolocation.getCurrentPosition(
					     function(position){
						 pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude)
						     //pos = new google.maps.LatLng(25.724977, -100.3133) // Poscion de la huella de fime
						 map.setCenter(pos);
						 draw_signals();
					     } );
}
