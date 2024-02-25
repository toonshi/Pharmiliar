window.addEventListener('DOMContentLoaded', function() {

    async function loadGoogleMaps() {
        // Load the Google Maps JavaScript API script dynamically
        await new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places";
    
            script.defer = true;
            script.async = true;
            script.onload = () => {
                // Once the library is loaded, call initMap
                initMap();
                resolve();
            };
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
    
    function initMap() {
        // Check if the google object is defined
        if (typeof google === 'undefined' || typeof google.maps === 'undefined') {
            console.error('Google Maps JavaScript API is not loaded.');
            return; // Do nothing if Google Maps API is not loaded
        }

        var institutionLng = parseFloat(document.getElementById('institution_lng').value);
        var institutionLat = parseFloat(document.getElementById('institution_lat').value);
       
        
        var directionsService = new google.maps.DirectionsService();
        var directionsDisplay = new google.maps.DirectionsRenderer();
        
        var map = new google.maps.Map(document.getElementById('map-route'), {
            zoom: 7,
            center: {
                lat: institutionLat,
                lng: institutionLng
            }
        });
        
        directionsDisplay.setMap(map);
        
        calculateAndDisplayRoute(directionsService, directionsDisplay, institutionLat, institutionLng);
    }

    function calculateAndDisplayRoute(directionsService, directionsDisplay, institutionLat, institutionLng) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var lat_a = position.coords.latitude; // User's latitude
                var long_a = position.coords.longitude; // User's longitude

                var origin = { lat: lat_a, lng: long_a };
                var destination = { lat: institutionLat, lng: institutionLng }; // Set destination to institution's location

                directionsService.route({
                    origin: origin,
                    destination: destination,
                    travelMode: google.maps.TravelMode.DRIVING,
                }, function(response, status) {
                    if (status === 'OK') {
                        directionsDisplay.setDirections(response);
                    } else {
                        alert('Directions request failed due to ' + status);
                        window.location.assign("/route");
                    }
                });
            }, function(error) {
                console.error('Error getting user location:', error);
                handleLocationError(error);
            });
        } else {
            console.error('Geolocation is not supported by this browser.');
            // Handle browser not supporting geolocation
        }
    }

    function handleLocationError(error) {
        console.error("Error getting user location:", error);
        alert("Error: Unable to get your location. Using default location.");
        // handleMapLoadError(); // You need to define this function
    }

    // Call loadGoogleMaps when the page is loaded
    loadGoogleMaps().catch(error => {
        console.error('Error loading Google Maps JavaScript API:', error);
        handleMapLoadError(error);
    });

    function handleMapLoadError(error) {
        // Define your error handling logic here
        console.error("Error loading Google Maps:", error);
        alert("Error: Failed to load Google Maps.");
        // Optionally, you can redirect or show an error message to the user
    }

});
