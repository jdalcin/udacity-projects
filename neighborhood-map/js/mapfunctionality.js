var map;
var markerIndex = 0;
var infoWindow;

function setBounds(locations) {
	var bounds = new google.maps.LatLngBounds();
	locations.forEach(function(location) {
		location.setMap(map);
		bounds.extend(location.position);
	});
	map.fitBounds(bounds);
}

function createMarker(location, id) {
	var marker = new google.maps.Marker({
			position: location.position,
			title: location.title,
			animation: google.maps.Animation.DROP,
			id: id
		});
	marker['infoWindow'] = new google.maps.InfoWindow();
	populateInfoWindow(marker['infoWindow'], marker);
	marker.addListener('click', function() {
		toggleBounce(this);
		toggleInfoWindow(this);
	});
	marker['infoWindow'].addListener('closeclick', function() {
		toggleBounce(marker);
		infoWindow.close();
	});
	MVVM.model.neighborhoodLocations.push(marker);
}

function populateInfoWindow(infoWindow, marker) {
	streetView = new google.maps.StreetViewService();
	var radius = 50;
	streetView.getPanoramaByLocation(marker.position, radius, getStreetView);

	function getStreetView(data, status) {
	     if (status == google.maps.StreetViewStatus.OK) {
	          var nearStreetViewLocation = data.location.latLng;
	          var heading = google.maps.geometry.spherical.computeHeading(
	              nearStreetViewLocation, marker.position);
	          infoWindow.setContent('<div><h3>' + marker.title + '</h3></div><div id="pano_' + marker.id + '"></div>');
	          var panoramaOptions = {
	               position: nearStreetViewLocation,
	               pov: { //pov:-> point of view
	               heading: heading,
	               pitch: 40 //slightly above the building
	              	}
	          };
	          	var panorama = new google.maps.StreetViewPanorama(document.getElementById('pano_' + marker.id), panoramaOptions);
	     } else {
	          infoWindow.setContent('<div>' + marker.title + '</div>' +
	              '<div>No Street View Found</div>');
	     }
	}

	// var wikiURL = 'http://en.wikipedia.org/w/api.php?action=opensearch&search=' + marker.title + '&format=json&callback=wikiCallback';
 //        $.ajax({
 //            url: wikiURL,
 //            dataType: "jsonp"
 //            }).done(function(response) {
 //                var articleStr = response[1];
 //                var URL = 'http://en.wikipedia.org/wiki/' + articleStr;
 //                // Use streetview service to get the closest streetview image within
 //                // 50 meters of the markers position
 //                console.log(infoWindow['streetview']);
 //               infoWindow['streetView'].getPanoramaByLocation(marker.position, radius, getStreetView);
 //                console.log(URL);
 //            }).fail(function (jqXHR, textStatus) {
 //                    alert("failed to load wikipedia");
 //               });

}

function initMarkers() {
	var defaultLocations = [
		{title: 'Inner Harbor', position: {lat: 39.285848, lng: -76.613111}},
		{title: 'National Aquarium', position: {lat: 39.285095, lng: -76.608287}},
		{title: 'Marriot Waterfront', position: {lat: 39.283137, lng: -76.602798}},
		{title: 'Federal Hill Park', position: {lat: 39.279721, lng: -76.608462}},
		{title: 'Star-Spangled Banner Historic Trail', position: {lat: 39.265293, lng: -76.579640}}
	];
	defaultLocations.forEach(function(location, i) {
		createMarker(location, i);
	});
	setBounds(MVVM.model.neighborhoodLocations());
}

function toggleInfoWindow(marker) {
	infoWindow = marker['infoWindow'];
	if (!infoWindow.getMap()) {
		infoWindow.open(map, marker);
	} else {
		infoWindow.close();
	}
}


function toggleBounce(marker) {
	if (marker.getAnimation() != null) {
		marker.setAnimation(null);
	} else {
		marker.setAnimation(google.maps.Animation.BOUNCE);
	}
}

function initMap() {
	var startingLocation = {
		center: {lat: 39.283629, lng: -76.609211},
		zoom: 16
	};
	map = new google.maps.Map(document.getElementById('map'), startingLocation);
	initMarkers();
	initAutocomplete('addSpot', function(autocomplete) {
		autocomplete.bindTo('bounds', map);
		google.maps.event.addListener(autocomplete, 'place_changed', function() {
			MVVM.model.latestLocationTitle($('#addSpot').val());
		});
	});
	initAutocomplete('locateNeighborhood', function(autocomplete) {
		google.maps.event.addListener(autocomplete, 'place_changed', function() {
			MVVM.model.neighborhood($('#locateNeighborhood').val());
		});
	});
}

function initAutocomplete(elementId, addOptions) {
	var autocomplete = new google.maps.places.Autocomplete(document.getElementById(elementId));
	addOptions(autocomplete);
}

function geocode(address, extraCallback) {
	var geocoder = new google.maps.Geocoder();
	var location;
	geocoder.geocode({
		address: address
     }, function(results, status) {
          if (status == google.maps.GeocoderStatus.OK) {
               	var lat = results[0].geometry.location.lat();
               	var lng = results[0].geometry.location.lng();
               	location = {
               		title: address,
               		position: {lat: lat, lng: lng}
               	}
               	extraCallback(location);
		}
	});
}

var MVVM = {

	model: {

		neighborhood: ko.observable('Baltimore'),
		neighborhoodCopy: 'Baltimore', // non-observable copy of variable
		neighborhoodLocations: ko.observableArray(),
		latestLocationTitle: ko.observable(),
		showNeighborhood: ko.observable(true),
		locationFilterString: ko.observable()

	},

	viewModel: {

		locateNeighborhood: function() {
			if(MVVM.model.neighborhood() != MVVM.model.neighborhoodCopy && confirm('Changing Locations deletes all saved spots. Are you sure?')) {
				geocode(MVVM.model.neighborhood(), function(location) {
					map.setCenter(location.position);
					map.setZoom(14);
					MVVM.model.showNeighborhood(true);
				});
				MVVM.viewModel.deleteSpots();
				MVVM.model.neighborhoodCopy = MVVM.model.neighborhood();
			} else {
				MVVM.model.neighborhood(MVVM.model.neighborhoodCopy);
			}
		},
		addLocation: function() {
			var location = geocode(MVVM.model.latestLocationTitle(), function(location) {
				var locationsArray = MVVM.model.neighborhoodLocations();
				if (locationsArray != 0) {
	               		var id = locationsArray[locationsArray.length - 1].id + 1;
	               	} else {
	               		id = 0;
	               	}
	               	createMarker(location, id);
	               	setBounds(MVVM.model.neighborhoodLocations());
	               	MVVM.viewModel.showMarkedSpots();
			});
		},
		checkLocation: function(location) {
			if ($('#location_' + location.id).hasClass('marked-spot-clicked')) {
				$('#location_' + location.id).removeClass('marked-spot-clicked');
			} else {
				$('#location_' + location.id).addClass('marked-spot-clicked');
			}
			toggleBounce(location);
			toggleInfoWindow(location);
		},
		showMarkedSpots: function() {
			setBounds(MVVM.model.neighborhoodLocations());
		},
		hideMarkedSpots: function() {
			MVVM.model.neighborhoodLocations().forEach(function(location) {
				location.setMap(null);
			});
		},
		deleteMarkedSpot: function(location) {
			location.setMap(null);
			MVVM.model.neighborhoodLocations.remove(location);
			MVVM.viewModel.showMarkedSpots();
		},
		deleteNeighborhood: function() {
			if (confirm('Deleting the neighborhood deletes all saved spots. Are you sure?')) {
				MVVM.model.neighborhood(null);
				MVVM.model.showNeighborhood(false);
				MVVM.viewModel.deleteSpots();
			}
		},
		deleteSpots: function() {
			MVVM.model.neighborhoodLocations().forEach(function(location) {
				location.setMap(null);
			});
			MVVM.model.neighborhoodLocations.removeAll();
		},
		filterLocations: function() {
			MVVM.model.neighborhoodLocations().forEach(function(location) {
				var filterString = MVVM.model.locationFilterString();
				if (filterString == '' || location.title.toUpperCase().includes(filterString.toUpperCase())) {
					location.setMap(map);
					$('#location_' + location.id).show();
				} else {
					location.setMap(null);
					$('#location_' + location.id).hide();
				}
			});
		},
		autocomplete: function(data, event) {
			// geocode(MVVM.model.neighborhood(), function(location) {
			// 	var options = {
			// 	location: location.position,
			// 	radius: 50
			// 	}
			// 	var autocomplete = new google.maps.places.Autocomplete(document.getElementById(event.target.id), options);
			// 	autocomplete.bindTo('bounds', map);
			// });
		},
		check: function() {
			console.log(MVVM.model.latestLocationTitle());
		}

	}

}
ko.applyBindings(MVVM);
