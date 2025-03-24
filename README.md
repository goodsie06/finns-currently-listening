<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currently Playing</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background-color:rgb(138, 120, 162);
        }
        .track-info {
            font-size: 24px;
        }
        .progress-info {
            font-size: 20px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Currently Playing: </h1>
    <div class="track-info" id="track-info">
        Loading...
    </div>

    <div class="progress-info" id="progress-info">
        Progress: Loading...
    </div>

    <script>
        async function fetchCurrentTrack() {
            try {
                const response = await fetch('http://127.0.0.1:5000/currently-playing');
                const data = await response.json();

                if (data.track) {
                    document.getElementById('track-info').innerHTML = `Currently playing: <strong>${data.track}</strong> by <strong>${data.artist}</strong>`;
                    document.getElementById('progress-info').innerHTML = `Progress: <strong>${data.progress}</strong>`;
                } else {
                    document.getElementById('track-info').innerHTML = data.message || "No track is currently playing.";
                    document.getElementById('progress-info').innerHTML = "Progress: N/A";
                }
            } catch (error) {
                document.getElementById('track-info').innerHTML = "Error fetching data.";
                document.getElementById('progress-info').innerHTML = "Progress: N/A";
            }
        }

        // Fetch track info when the page loads
        window.onload = fetchCurrentTrack;

        // Set an interval to refresh the track info every 1 second
        setInterval(fetchCurrentTrack, 1000); // 1000 ms = 1 second
    </script>
</body>
</html>
