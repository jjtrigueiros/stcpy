STCP provides a variety of undocumented endpoints containing data for real time bus arrivals.

This project aims to create a simple and self-hostable REST API to facilitate integrating this data with other applications, in absence of an official solution.


## Usage
Application in early development. The API may change drastically on any given update.

### Running the app
1. Navigate to the project directory
2. Install the project dependencies
   - ex.: `poetry install && poetry shell`
   - alt.: `pip install -r requirements.txt`
3. Start the application using Uvicorn
   - ex.: `./scripts/entry.sh`

### Retrieving data
Basic functionality can be tested by sending requests to appropriate endpoints.

Ex. for stop with code `BCM2`:
```
http://localhost:8000/v0/timetables/stop/BCM2
```
or, equivalently, for line `704`, direction `0`, stop `1` after Terminus:
```
http://localhost:8000/v0/timetables/bus/704/0/1
```

We obtain a list of the current ETAs for all buses that will pass the chosen station:
```
[
    ["803 ","RIO TINTO ES","now","0min"],
    ["704 ","CODICEIRA -","18:08","4min"],
    ["203 ","MARQUÊS  -","18:13","9min"],
    ["903 ","C.MÚSICA MET","18:16","12min"],
    ["204 ","H.S.JOÃO","18:17","12min"]
]
```


## Planned features:
- Database caching
    - It is not expected that the bus lines or stops will change frequently. By caching this information in a local store, we can avoid needlessly calling the itinerarium endpoint.
- Comprehensive documentation
    - The OpenAPI schema can be consulted in the `/schema/` endpoint. However, the application functions must be adequately documented.