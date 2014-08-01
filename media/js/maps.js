// GLOBAL MAP VARS
var map; 
var BaseIcon; 
var OverIcon; 
var bounds = new GLatLngBounds();
var map_lat = 0;
var map_lon = 0;
var map_zoom = 1;
var marker_num = 0;
var article_lookup = [];
var htmls = [];
var offMarkers = [];
var onMarkers = [];

function loadMap() {
	if (GBrowserIsCompatible()) {
	    map = new GMap2(document.getElementById("map"));
		map.addControl(new GSmallMapControl());
		map.addControl(new GMapTypeControl());
	    map.setCenter(new GLatLng(map_lat, map_lon), map_zoom);

		BaseIcon = new GIcon();
		BaseIcon.shadow = 'http://www.google.com/mapfiles/shadow50.png';
		BaseIcon.iconSize = new GSize(20, 34);
		BaseIcon.shadowSize = new GSize(37, 34);
		BaseIcon.iconAnchor = new GPoint(9, 34);
		BaseIcon.infoWindowAnchor = new GPoint(9, 2);
		BaseIcon.infoShadowAnchor = new GPoint(18, 25);

		OverIcon = new GIcon(BaseIcon);
		OverIcon.image = 'http://pdxguide.org/media/img/icons/default.png';

		if (article_list) {
			for (var i=0; i < article_list.length; i++) {
				add_article(article_list[i][0], article_list[i][1], article_list[i][2], article_list[i][3], article_list[i][4], article_list[i][5], article_list[i][6], article_list[i][7], article_list[i][8]);
			}
		}
		map.setZoom(map.getBoundsZoomLevel(bounds));
		map.setCenter(bounds.getCenter());
	}
}

function add_article(lng, lat, title, section, url, address, phone, description,id ) {
    var markerpt = new GLatLng(lat,lng);
	bounds.extend(markerpt); // TO ZOOM MAP TO OUTER BOUNDS AFTER LOADING
	if (section) {
		var icon = new GIcon(BaseIcon);
		icon.image = 'http://pdxguide.org/media/img/icons/default.png';
		// todo: CUSTOM ICON FOR SECTION
		// icon.image = 'http://pdxguide.org/media/img/' + section + '.png';
		marker = new GMarker(markerpt, icon);
	}
	else {
		marker = new GMarker(markerpt);
	}
	if (url) {
		var html = '<div class="mapInfoBox"><h3><a href="' + url + '">' + title + '</a></h3>';
		if (phone)
			html += '<p class="phone">' + phone + '</p>';
		html += '<p class="address">' + address + '</p>';
		if (description)
			html += '<p class="description">' + description + '</p>';
		if (article_list.length!=1) {
			html += '<a class="details" href="' + url + '"><span>Details &#x2192;</span></a>';
		}
		html += '</div>';
		htmls[marker_num] = html;
	}
	// ARRAYS FOR MOUSEOVERS
/*	offMarkers[marker_num] = marker;*/
/*	onMarkers[marker_num] = new GMarker(markerpt,OverIcon);*/
	onMarkers[marker_num] = marker;

	map.addOverlay(onMarkers[marker_num]);
	GEvent.addListener(onMarkers[marker_num], "click", function() { this.openInfoWindowHtml(html); });

	// OPEN WINDOW IF ONLY ONE POINT
	if (article_list.length==1) {
    	marker.openInfoWindowHtml(html);
	}
	article_lookup[id] = marker_num;
	marker_num++;
}

// SHOW ARTICLE HTML IN MAP
function maplink_click(id) {
	i = article_lookup[id];
	onMarkers[i].openInfoWindowHtml(htmls[i]);
}

function maplink_over(id) {
	i = article_lookup[id];
/*	map.removeOverlay(offMarkers[i]);
	map.addOverlay(onMarkers[i]);*/
}

function maplink_out(id) {
	i = article_lookup[id];
/*	map.removeOverlay(onMarkers[i]);
	map.addOverlay(offMarkers[i]);*/
}