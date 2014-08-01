function load() {
	if (GBrowserIsCompatible()) {
	    map = new GMap2(document.getElementById("map"));
		map.addControl(new GSmallMapControl());
		map.addControl(new GMapTypeControl());
	    map.setCenter(new GLatLng(map_lat, map_long), map_zoom);

		BaseIcon = new GIcon();
		BaseIcon.shadow = 'http://www.google.com/mapfiles/shadow50.png';
		BaseIcon.iconSize = new GSize(20, 34);
		BaseIcon.shadowSize = new GSize(37, 34);
		BaseIcon.iconAnchor = new GPoint(9, 34);
		BaseIcon.infoWindowAnchor = new GPoint(9, 2);
		BaseIcon.infoShadowAnchor = new GPoint(18, 25);

		if (article_list) {
			for (var i=0; i < article_list.length; i++) {
				add_article(article_list[i][0], article_list[i][1], article_list[i][2], article_list[i][3], article_list[i][4], article_list[i][5]);
			}
		}
	}
}

function add_article(lng, lat, title, section, url, address) {
	var markerpt = new GPoint(lng, lat);
	if (section) {
		var icon = new GIcon(BaseIcon);
		icon.image = 'http://pdxguide.org/media/img/icons/default.png';
/*		icon.image = 'http://pdxguide.org/media/img/' + section + '.png';*/
		var marker = new GMarker(markerpt, icon);
	}
	else {
		var marker = new GMarker(markerpt);
	}
	if (url) {
		var html = '<div style="width: 200px;"><p><strong><a href="' + url + '">' + title + '</a></strong></p><p>' + address + '</p></div>';
		GEvent.addListener(marker, "click", function() { marker.openInfoWindowHtml(html); });
	}
	map.addOverlay(marker);
    marker.openInfoWindowHtml(html);
}
