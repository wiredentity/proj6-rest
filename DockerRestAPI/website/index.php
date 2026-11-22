<html>
    <head>
        <title>Brevet API Consumer</title>
    </head>

    <body>
        <h1>Brevet API Consumer</h1>

        <form method="GET">

            <label>Format:</label>
            <select name="format">
                <option value="json">JSON</option>
                <option value="csv">CSV</option>
            </select>

            <label>Top K:</label>
            <input type="number" name="top" min="1">

            <br><br>

            <button name="endpoint" value="listAll">
                List All
            </button>

            <button name="endpoint" value="listOpenOnly">
                Open Only
            </button>

            <button name="endpoint" value="listCloseOnly">
                Close Only
            </button>

        </form>

        <h2>Results</h2>

        <?php
        if (isset($_GET["endpoint"])) {

            $endpoint = $_GET["endpoint"];
            $format = $_GET["format"];
            $top = $_GET["top"];
            
            // Make sure the requested endpoint and format are valid
            if (!in_array($endpoint, ["listAll", "listOpenOnly", "listCloseOnly"]) ||
                !in_array($format, ["json", "csv"])) {
                exit("Invalid API request");
            }

            // Build the API URL
            $url = "http://brevet-service:5000/" . $endpoint . "/" . $format;

            // Add top K for open and close endpoints
            if ($top != "" && $endpoint != "listAll") {
                $url = $url . "?top=" . $top;
            }

            // Request data from the API
            $response = file_get_contents($url);

            // Display the response
            if ($response === false) {
                echo "Error retrieving control times";
            } else {
                echo "<pre>" . htmlspecialchars($response) . "</pre>";
            }
        }
        ?>

    </body>
</html>
