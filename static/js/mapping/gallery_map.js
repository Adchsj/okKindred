
var image_markers = new Array();

$(document).ready(function() {

    if ($('#gallery_map').length == 0) {
        return;
    }

    set_gallery_map();
});


function set_gallery_map() {

    var latitude = parseFloat($('#gallery_map').data('latitude'));
    var longitude = parseFloat($('#gallery_map').data('longitude'));
    var zoom = parseFloat($('#gallery_map').data('zoom'));

    var map = L.map('gallery_map', {
        center: [latitude, longitude],
        zoom: 5,
        zoomControl: false,
        minZoom: 2,
        scrollWheelZoom: true,
        detectRetina: true,
        maxBounds: [[-90, -200],[90, 200]]
    });

    L.tileLayer('https://{s}.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={token}', {
		subdomains: ['a','b','c','d'],
		id: 'okkindred.ldfc645h',
		token: 'pk.eyJ1Ijoib2traW5kcmVkIiwiYSI6Ild2MnY5dDQifQ.EHr6blIYPYeg4bWmSStT-g'
	}).addTo(map);

    map.addControl( L.control.zoom({position: 'bottomleft'}));

    get_gallery_map_data(map, true);

    map.on('zoomend', function(e) {
        get_gallery_map_data(e.target, false);
    });
}


function get_gallery_map_data(map, loading) {
    var bounds = map.getBounds()
    var min = bounds.getSouthWest().wrap();
    var max = bounds.getNorthEast().wrap();

    var max_num_points = Math.floor(Math.min($(document).height(),$(document).width()) / 100.0); //100 pixels per spot
    var min_lat_lng = Math.min(max.lng - min.lng, max.lat - min.lat);
    var division_size = min_lat_lng / max_num_points;

    var gallery_id = parseFloat($('#gallery_map').data('gallery_id'));

    var url = ['/gallery='];
    url.push(gallery_id);
    url.push('/map_data/');
    url.push(division_size);
    url.push('/');

    $.get(
        url.join(''),
        function(data) {

            var details_translation = $('#translate').data('details')

            for(i = 0; i < image_markers.length; i++) {
                map.removeLayer(image_markers[i]);
            }
            image_markers.length = 0;


            for (var key in data) {
                var loc = data[key];

                var myIcon = L.divIcon({
                    className:  'circle',
                    iconSize:   [40, 40], // size of the icon
                    iconAnchor: [20, 20], // point of the icon which will correspond to marker's location
                    popupAnchor:[0, -5], // point from which the popup should open relative to the iconAnchor
                    html:       loc.length
                });

                var marker = L.marker([loc[0].latitude,loc[0].longitude], {icon: myIcon}).addTo(map);
                image_markers.push(marker);

                var html = [];

                if (loc.length == 1) {
                    var popupWidth = 90;
                } else if (loc.length < 5){
                    var popupWidth = 180;
                } else {
                    var popupWidth = 270;
                }

                html.push('<div style="overflow: hidden; width:');
                html.push(popupWidth);
                html.push('px;">');

                for (var i = 0; i < loc.length; i++) {
                    var image = loc[i];
                    html.push('<a class="image_in_gallery" href="/media/');
                    html.push(image.large_thumbnail);
                    html.push('" data-lightbox="gallery"');
                    html.push(' data-title="');
                    html.push('&lt;a href=\'/image=');
                    html.push(image.id);
                    html.push('/details/\' class=\'btn btn-info\' &gt; ');
                    html.push(details_translation);
                    html.push(' &lt;/a&gt ');
                    html.push(image.title);
                    html.push('">');

                    html.push('<img class="map_thumbnail" src="/media/' + image.thumbnail + '" ');
                    html.push('alt="' + image.title +'/"')
                    html.push('/>');
                    html.push('</a>');
                }

                html.push('</div>');

                marker.bindPopup(html.join(''));
            }

            if (loading) {
                map.panTo(image_markers[0]._latlng, true);
            }
        }
    );
}