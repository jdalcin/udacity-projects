																		/* Global variables */
var map;
																		/* Initialize Map Functions */
// Checks for Error in Requesting Map
function mapError() {
	setTimeout(function() {
		alert("Map unable to load. Error requesting Google Maps API. Check Javascript console for error.");
	}, 500);
}

// Initializes Google Map
function initMap() {
	var startingLocation = {
		center: {lat: 39.283629, lng: -76.609211},
		zoom: 16
	};
	map = new google.maps.Map(document.getElementById('map'), startingLocation);
	initMarkers();
	var addSpotAutocomplete = new google.maps.places.Autocomplete(document.getElementById('addSpot'));
	addSpotAutocomplete.bindTo('bounds', map);
	google.maps.event.addListener(addSpotAutocomplete, 'place_changed', function() {
		ko.utils.triggerEvent(document.getElementById('addSpot'), 'change');
	});
	var locateNeighborhoodAutocomplete = new google.maps.places.Autocomplete(document.getElementById('locateNeighborhood'));
	google.maps.event.addListener(locateNeighborhoodAutocomplete, 'place_changed', function() {
		ko.utils.triggerEvent(document.getElementById('locateNeighborhood'), 'change');
	});
}

// Initializes Location Markers
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

// Creates a Location Marker
function createMarker(location, id) {
	var marker = new google.maps.Marker({
			position: location.position,
			title: location.title,
			animation: google.maps.Animation.DROP,
			id: id
		});
	marker['infoWindow'] = new google.maps.InfoWindow();
	marker['infoWindowHasMap'] = ko.observable(false);
	// adds a listener to a marker and the info window associated with it
	marker.addListener('click', function() {
		toggleBounce(this);
		toggleInfoWindow(this);
	});
	marker['infoWindow'].addListener('closeclick', function() {
		toggleBounce(marker);
		marker['infoWindowHasMap'](false);
	});
	MVVM.model.neighborhoodLocations.push(marker);
}

// Sets Map Bounds Around Location Markers
function setBounds(locations) {
	var bounds = new google.maps.LatLngBounds();
	locations.forEach(function(location) {
		location.setMap(map);
		bounds.extend(location.position);
	});
	map.fitBounds(bounds);
	google.maps.event.addDomListener(window, 'resize', function() {
  		map.fitBounds(bounds);
	});
}
																				/* Toggle Functions */
// Toggles Info Window on and off
function toggleInfoWindow(marker) {
	infoWindow = marker['infoWindow'];
	if (!infoWindow.getMap()) {
		populateInfoWindow(infoWindow, marker);
		infoWindow.open(map, marker);
		marker['infoWindowHasMap'](true);
	} else {
		infoWindow.close();
		marker['infoWindowHasMap'](false);
	}
}

// Toggles Marker's Bounce Animation on and off
function toggleBounce(marker) {
	if (marker.getAnimation()) {
		marker.setAnimation(null);
	} else {
		marker.setAnimation(google.maps.Animation.BOUNCE);
	}
}
																		/* Info Window Functions */
// Populates Information in Info Window
function populateInfoWindow(infoWindow, marker) {
	var streetView = new google.maps.StreetViewService();
	var radius = 50;
	var marker_title = marker.title.split(',')[0];
	var infoWindowHTML = '';
	infoWindow.setContent(infoWindowHTML);

	// Adds Google Street View of Marker Location to Info Window
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

    // Adds Wiki Information of Marker Location to Info Window
    $.ajax({
          url: 'https://en.wikipedia.org/w/api.php?origin=*&action=query&format=json&prop=extracts&exintro=&explaintext=&titles=' + marker_title,
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
	        	infoWindowHTML += '<div><h3>' + marker_title + '</h3></div><div class="center"><p>' + wikiHTML + '</p></div><div class="center"><p>Disclaimer: Information obtained from Wikipedia.</p></div>';
	        	streetView.getPanoramaByLocation(marker.position, radius, getStreetView);
          },
          error: function(error) {
          	alert("Wikipedia request failed. Check the Javascript console (Ctrl + Shift + i) for error.");
          }
     });

}
																			/* Search Functions */
// Gets Longitude and Latitude Coordinates of an Address
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
               	};
               	extraCallback(location);
		} else {
			alert("Failed to find address. Google Geocode API failing request. Check Javascript console for error.");
		}
	});
}
																			/* Code Organized by Model View ViewModel Paradigm */
var MVVM = {

	// Data
	model: {
		neighborhood: ko.observable('Baltimore'),
		neighborhoodCopy: ko.observable('Baltimore'), // copy only updated once neighborhood change is confirmed
		neighborhoodLocations: ko.observableArray(),
		latestLocationTitle: ko.observable(), // latest Marker Location Title Added to the Location List
		showNeighborhood: ko.observable(true), // tells whether neighborhood box is displayed in DOM
		locationFilterString: ko.observable('')
	},

	// Functions to manipulate data in the model
	viewModel: {
		locateNeighborhood: function() { // centers on a neighborhood and deletes all markers
			if(MVVM.model.neighborhood() != MVVM.model.neighborhoodCopy() && (MVVM.model.neighborhoodLocations().length == 0 || confirm('Changing Locations deletes all saved spots. Are you sure?'))) {
				geocode(MVVM.model.neighborhood(), function(location) {
					map.setCenter(location.position);
					map.setZoom(14);
					MVVM.model.showNeighborhood(true);
				});
				MVVM.viewModel.deleteSpots();
				MVVM.model.neighborhoodCopy(MVVM.model.neighborhood());
			}
		},
		addLocation: function() { // adds a marker
			if (MVVM.model.latestLocationTitle() != undefined) {
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
			}
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
		deleteNeighborhood: function() { // deletes a neighborhood and all its markers
			if (MVVM.model.neighborhoodLocations().length == 0 || confirm('Deleting the neighborhood deletes all saved spots. Are you sure?')) {
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
		filterLocations: function(location) { // filters markers in real time based on what is typed in the filter box
			var filterString = MVVM.model.locationFilterString();
			if (filterString == '' || location.title.toUpperCase().includes(filterString.toUpperCase())) {
				location.setMap(map);
				return true;
			} else {
				location.setMap(null);
				return false;
			}
		}
	}

};

// Binds DOM Variables to Javascript Variables in the MVVM
ko.applyBindings(MVVM);


