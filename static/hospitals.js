// const DEFAULT_LOCATION = { lat: 40.7128, lng: -74.0060 };
// const DEFAULT_ZOOM = 10;

// let map;
// let userLocation;
// let institutions = []; // Changed from const to let

// Function to initialize Google Map
// function initMap() {
//     if (!google || !google.maps) {
//         handleMapLoadError();
//         return;
//     }

//     getUserLocation()
//         .then(location => {
//             userLocation = location;
//             initializeMap(userLocation);
//             fetchInstitutionsData(); // Fetch institutions data from Django backend
//         })
//         .catch(handleLocationError);
// }

// Function to handle error when Google Maps fails to load
// function handleMapLoadError() {
//     console.error("Google Maps failed to load.");
//     alert("Error: Google Maps failed to load. Using fallback mechanism.");

//     initializeMap(DEFAULT_LOCATION);
// }

// Function to get user's current location
// function getUserLocation() {
//     return new Promise((resolve, reject) => {
//         if (navigator.geolocation) {
//             navigator.geolocation.getCurrentPosition(
//                 position => resolve({ lat: position.coords.latitude, lng: position.coords.longitude }),
//                 reject
//             );
//         } else {
//             reject("Geolocation not supported");
//         }
//     });
// }

// Function to initialize the map
// function initializeMap(location) {
//     map = new google.maps.Map(document.getElementById('map'), {
//         center: location,
//         zoom: DEFAULT_ZOOM
//     });
// }

// Function to handle error in getting user's location
// function handleLocationError(error) {
//     console.error("Error getting user location:", error);
//     alert("Error: Unable to get your location. Using default location.");
//     handleMapLoadError();
// }

// Function to create markers for sample institutions
// function createMarkersForInstitutions() {
//     institutions.forEach(institution => {
//         const marker = new google.maps.Marker({
//             position: institution.location,
//             map: map,
//             title: institution.name
//         });

//         marker.addListener('click', () => {
//             showReviews(institution.reviews);
//         });
//     });
// }

// Function to render the list of institutions
// function renderInstitutionsList() {
//     const listContainer = $('#institutionsList');
//     listContainer.empty(); // Clear previous content

//     institutions.forEach(institution => {
//         const listItem = $('<div class="institution"></div>').text(institution.name);
//         listItem.data('id', institution.id);
//         listContainer.append(listItem);
//     });
// }

// Function to show reviews for an institution
function showReviews(reviews) {
    const reviewsContainer = $('#reviewsContainer');
    reviewsContainer.empty(); // Clear previous content

    reviews.forEach(review => {
        const reviewItem = $('<div></div>').text(review);
        reviewsContainer.append(reviewItem);
    });

    $('#reviewsSection').fadeIn();
}

// Fetch institutions data from Django backend
function fetchInstitutionsData() {
    fetch('/hospitals/institutions/') // Replace '/hospitals/institutions/' with your actual URL endpoint
        .then(response => response.json())
        .then(data => {
            institutions = data;
            createMarkersForInstitutions();
            renderInstitutionsList();
        })
        .catch(error => {
            console.error('Error fetching institutions data:', error);
            alert('Error fetching institutions data. Please try again later.');
        });
}

// Event listener for clicking on institutions
$(document).on('click', '.institution', function() {
    const id = $(this).data('id');
    const institution = institutions.find(inst => inst.id === id);
    showReviews(institution.reviews);
});

// Event listener for review form submission
$(document).ready(function() {
    $('#review-form').submit(function(event) {
        event.preventDefault();

        $.ajax({
            type: 'POST',
            url: window.location.pathname,
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    alert('Review submitted successfully!');
                    // Optionally, you can reload the page or do something else after success
                } else {
                    // Handle form errors
                    alert('Review submission failed!');
                }
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});

