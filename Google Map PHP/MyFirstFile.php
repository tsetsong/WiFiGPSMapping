<?php 

function echo_ip(){
$user_ip = gethostbyname($_SERVER['SERVER_NAME']);;
$ip= 'Your IP address is :' .$user_ip;
echo $ip;
}
echo_ip();


?>

<html> 
<head> 
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" /> 
  <title>GPS Map Wifi Mapping</title> 
  <script src="http://maps.google.com/maps/api/js?sensor=false" 
          type="text/javascript"></script>
</head> 
<body>
  

  <script type="text/javascript">
 //marker object   
  var markers = [
    {
        "ssid": 'Tampines',
        "lat": '1.34',
        "lng": '103.95',
        "blk": '274',
        "type": 'WPA'
    },
        {
        "ssid": 'BEDOK',
        "lat": '1.32',
        "lng": '103.93',
        "blk": '24',
        "type": 'WEP'
        },
 
    ];
window.onload = function () {
 
    var mapOptions = {
        center: new google.maps.LatLng(markers[0].lat, markers[0].lng),
        zoom: 8,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var infoWindow = new google.maps.InfoWindow();
    var latlngbounds = new google.maps.LatLngBounds();
    var map = new google.maps.Map(document.getElementById("map"), mapOptions);
    var i = 0;
    
	//filtering marker colours 
	var interval = setInterval(function () {
        var data = markers[i]
        var myLatlng = new google.maps.LatLng(data.lat, data.lng);
        var icon = "";
        switch (data.type) {
            case "WEP":
                icon = "red";
                break;
            case "WPA":
                icon = "green";
                break;
        }
        icon = "http://maps.google.com/mapfiles/ms/icons/" + icon + ".png";
        var marker = new google.maps.Marker({
            position: myLatlng,
            map: map,
            title: data.title,
            animation: google.maps.Animation.DROP,
            icon: new google.maps.MarkerImage(icon)
        });
		
		// click event handling 
        (function (marker, data) {
            google.maps.event.addListener(marker, "click", function (e) {
                infoWindow.setContent(data.type);
                infoWindow.open(map, marker);
            });
        })(marker, data);
        latlngbounds.extend(marker.position);
        i++;
        if (i == markers.length) {
            clearInterval(interval);
            var bounds = new google.maps.LatLngBounds();
            map.setCenter(latlngbounds.getCenter());
            map.fitBounds(latlngbounds);
        }
    }, 80);
}
</script>
  
  <table>
<tr>
    <td>
        <div id="map" style="width: 500px; height: 500px">
        </div>
    </td>
    <td valign="top">
        <u>Legend:</u><br />
        <img alt="" src="http://maps.google.com/mapfiles/ms/icons/red.png" />
        WEP<br />
   
        <img alt="" src="http://maps.google.com/mapfiles/ms/icons/green.png" />
        WPA<br />
    </td>
</tr>
</table>
</body>
</html>