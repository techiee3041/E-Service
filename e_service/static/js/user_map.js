document.addEventListener("DOMContentLoaded", function () {
    const pinLocationButton = document.getElementById('pinLocationButton');
    const mapContainer = document.getElementById('mapContainer');
    const latitudeInput = document.getElementById('latitude');
    const longitudeInput = document.getElementById('longitude');
    
    // Get the current trader's ID from the template
    const currentUserID = '{{ user_id }}';  // Assuming you pass this ID in the templateconsole.log('Current User ID:', currentUserID);
    console.log('Current User ID:', currentUserID);



    // Initialize Mapbox map
    mapboxgl.accessToken = 'pk.eyJ1IjoiZG9yZWVuMzAiLCJhIjoiY2xvOW10Nmg3MGRqZTJrcXFpMTZjaThpbyJ9.ZjtZO_sTrQyLIS8STM9x_g';
    const map = new mapboxgl.Map({
        container: 'mapContainer',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [0, 0], // Initial center (update when location is obtained)
        zoom: 12, // Initial zoom level
    });

    pinLocationButton.addEventListener('click', function () {
        // Get the user's location
        navigator.geolocation.getCurrentPosition(function (position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            // Update the hidden input fields with coordinates
            latitudeInput.value = latitude;
            longitudeInput.value = longitude;

            // Send the coordinates and user's ID to the server using an AJAX request
            const data = {
                latitude: latitude,
                longitude: longitude,
                userID: currentUserID,
            };

            $.ajax({
                url: '/api/save_coordinates',
                type: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json',
                success: function (response) {
                    // Handle the response from the server
                    console.log(response); // Log the response to the console
            
                    // Check if the coordinates were saved successfully
                    if (response && response.message === 'Coordinates saved successfully') {
                        // Do something on success, like updating UI or showing a success message
                        alert('Coordinates saved successfully');
                    } else {
                        // Handle other cases, such as an error response from the server
                        alert('Failed to save coordinates. Please try again.');
                    }
                },
                error: function (error) {
                    // Handle errors that may occur during the AJAX request
                    console.error('Error:', error);
                    alert('An error occurred. Please try again later.');
                }
            });
            

            // Update the map's center and add a marker
            map.setCenter([longitude, latitude]);
            new mapboxgl.Marker().setLngLat([longitude, latitude]).addTo(map);
        });
    });
});