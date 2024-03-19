document.addEventListener('DOMContentLoaded', function() {

    // Map
    const apiKey = "AAPKfc8d74ba03df40b284c296e6a8c89fb8N1SgKAtjq0XUmUXFrHWz2B1vr_35AbRyZyySGghIO9TmYkPI_9AeiSPumcTH1WBX";
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

