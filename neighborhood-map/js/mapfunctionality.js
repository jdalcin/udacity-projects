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
	marker.addListener('click', function() {
		toggleBounce(this);
		toggleInfoWindow(this);
	});
	console.log(marker['infoWindow']);
	marker['infoWindow'].addListener('closeclick', function() {
		toggleBounce(marker);
		toggleInfoWindow(marker);
	});
	MVVM.model.neighborhoodLocations.push(marker);
}

function populateInfoWindow(infoWindow, marker) {
	var streetView = new google.maps.StreetViewService();
	var radius = 50;
	var infoWindowHTML = '';
	infoWindow.setContent(infoWindowHTML);

	function getStreetView(data, status) {
		var streetViewHTML;
	     if (status == google.maps.StreetViewStatus.OK) {
	          var streetViewPosition = data.location.latLng;
	          var heading = google.maps.geometry.spherical.computeHeading(streetViewPosition, marker.position);
	          streetViewHTML = '<div id="pano_' + marker.id + '" class="center"></div>';
	          var panoramaOptions = {
	               position: streetViewPosition,
	               pov: {heading: heading, pitch: 30}
	          };
	          infoWindowHTML += streetViewHTML;
	     		infoWindow.setContent(infoWindowHTML);
	          	new google.maps.StreetViewPanorama(document.getElementById('pano_' + marker.id), panoramaOptions);
	     } else {
	     		streetViewHTML = '<div>Street View not Found</div>';
	     		infoWindowHTML += streetViewHTML;
	     		infoWindow.setContent(infoWindowHTML);
	     }
	}

    $.ajax({
          url: 'http://en.wikipedia.org/w/api.php?origin=*&action=query&format=json&prop=extracts&exintro=&explaintext=&titles=' + marker.title,
          dataType: "json",
          success: function(results, status) {
	        	if (status === 'success') {
	        		var pages = results.query.pages;
	        		var keys = Object.keys(pages);
	        		var wikiHTML;
	        		if (pages[keys[0]].extract !==  undefined) {
	        			wikiHTML = pages[keys[0]].extract;
	        		} else {
	        			wikiHTML = 'No Wiki Information Found';
	        		}
	        	} else {
	        		wikiHTML = 'Wiki Information Failed to Load';
	        	}
	        	infoWindowHTML += '<div><h3>' + marker.title + '</h3></div><div class="center"><p>' + wikiHTML + '</p></div>';
	        	streetView.getPanoramaByLocation(marker.position, radius, getStreetView);
          }
     });

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
	console.log(marker['infoWindow']);
	infoWindow = marker['infoWindow'];
	if ($('#location_' + marker.id).hasClass('marked-spot-clicked')) {
		$('#location_' + marker.id).removeClass('marked-spot-clicked');
	} else {
		$('#location_' + marker.id).addClass('marked-spot-clicked');
	}
	if (!infoWindow.getMap()) {
		populateInfoWindow(infoWindow, marker);
		infoWindow.open(map, marker);
	} else {
		infoWindow.close();
	}
}


function toggleBounce(marker) {
	if (marker.getAnimation()) {
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
		check: function() {
			console.log(MVVM.model.latestLocationTitle());
		}

	}

}
ko.applyBindings(MVVM);
(function() {
    if ( typeof Object.id == "undefined" ) {
        var id = 0;

        Object.id = function(o) {
            if ( typeof o.__uniqueid == "undefined" ) {
                Object.defineProperty(o, "__uniqueid", {
                    value: ++id,
                    enumerable: false,
                    // This could go either way, depending on your
                    // interpretation of what an "id" is
                    writable: false
                });
            }

            return o.__uniqueid;
        };
    }
})();

