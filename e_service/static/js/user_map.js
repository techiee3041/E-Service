document.addEventListener("DOMContentLoaded", function () {
    const mapContainer = document.getElementById('mapContainer');
    const latitudeInput = document.getElementById('latitude');
    const longitudeInput = document.getElementById('longitude');

    // Get the current trader's ID from the template
    const currentUserID = '{{ user_id }}';  // Assuming you pass this ID in the template
    console.log('Current User ID:', currentUserID);

    // Initialize Leaflet map
    const map = L.map(mapContainer).setView([0, 0], 12); // Initial center and zoom

    L.tileLayer(
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
            attribution: '© OpenStreetMap contributors'
        }
    ).addTo(map);

    // Get the user's location and save the coordinates
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
        map.setView([latitude, longitude], 12);
        L.marker([latitude, longitude]).addTo(map);
    });
});