# ACP Brevet Time Calculator

**Author:** Willow Sack  
**Email:** willow0@uoregon.edu

This project is a Flask application that calculates the opening and closing times for controls during an ACP brevet. It uses AJAX to automatically update control times and MongoDB to store them.

Included is a REST API to retrieve saved control times in JSON and CSV formats, as well as a PHP consumer to interact with the API.

The calculator is based on the [RUSA brevet time calculator](https://rusa.org/octime_acp.html).

## Running the Project

> Make sure `credentials.ini` is located in laptop folder before running

From the `DockerRestAPI` directory, run:

```bash
docker compose up --build
```

- Calculator: http://localhost:5001
- PHP Consumer: http://localhost:5000

The project runs in three separate Docker containers: Flask, MongoDB, and PHP. The containers communicate using their Docker service names.

To stop the containers:

```bash
docker compose down
```

## How to Use

1. Select the brevet distance and enter the start date and time.
2. Enter control distances in miles or kilometers.
3. Opening and closing times will automatically populate.
4. Click **Submit** to save the controls to MongoDB.
5. Click **Display** to view saved controls.
6. Click **Clear Saved** to clear the database.

Control times are stored as ISO 8601 timestamps so they can be sorted chronologically. Saved data persists between container restarts.

## REST API

The REST API retrieves saved control times from MongoDB using the following GET endpoints:

| Endpoint | Description |
| --- | --- |
| `/listAll` | All opening and closing times |
| `/listOpenOnly` | Only opening times |
| `/listCloseOnly` | Only closing times |

All three endpoints support `/json` and `/csv`. JSON is returned by default.

The opening-only and closing-only endpoints also support the optional `?top=k` parameter, which returns the earliest K times.

## PHP Consumer

The PHP consumer runs in a separate container and makes HTTP requests to the Flask REST API.

Select JSON or CSV, optionally enter a Top K value, and click List All, Open Only, or Close Only to display the results.

Top K only applies to Open Only and Close Only.

## Testing

After saving some control times using the calculator, the API can be tested using curl:

```bash
curl http://localhost:5001/listAll
curl http://localhost:5001/listAll/json
curl http://localhost:5001/listAll/csv
curl http://localhost:5001/listOpenOnly
curl http://localhost:5001/listCloseOnly
```

Top K filtering can be tested with:

```bash
curl 'http://localhost:5001/listOpenOnly/json?top=3'
curl 'http://localhost:5001/listCloseOnly/csv?top=3'
```

The consumer can also be tested directly in the browser by trying each button with both response formats.

## MongoDB

Saved documents can be checked directly using:

```bash
docker compose exec db mongosh
```

```javascript
use brevets
db.controls.find()
```

Each document contains the control distance in kilometers, opening time, and closing time.