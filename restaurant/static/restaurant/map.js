document.addEventListener('DOMContentLoaded', function() {

    // Map
    const apiKey = "ENTER_YOUR_API_KEY";
    const basemapEnum = "arcgis/navigation";

    const latitude_str = document.querySelector('#latitude').innerHTML;
    const latitude = Number(latitude_str)
    const longitude_str = document.querySelector('#longitude').innerHTML;
    const longitude = Number(longitude_str)

    var map = L.map('map').setView([latitude, longitude], 13);

    L.esri.Vector.vectorBasemapLayer(basemapEnum, {
        apiKey: apiKey
    }).addTo(map);

    L.marker([latitude, longitude]).addTo(map);

    L.Routing.control({
        waypoints:[
            L.latLng(),
            L.latLng(latitude ,longitude)
        ],
        routeWhileDragging: true,
        fitSelectedRoutes: true,
        geocoder: L.Control.Geocoder.nominatim()
    }).addTo(map);


});

