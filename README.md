STCP provides a variety of undocumented endpoints containing data for real time bus arrivals.

The goal is to create a simple and self-hostable REST API for integration with other applications, since the operator does not provide one themselves.


## Usage
This app is in a very early stage. The API may change drastically on any given update.

### Running the app
1. Navigate to the project directory
2. Install the project dependencies (recommended: `poetry install && poetry shell`)
3. Start Uvicorn (recommended: `./scripts/entry.sh`)

### Retrieving data
Basic functionality can be tested by sending requests to appropriate endpoints.

Ex. for stop with code `BCM2`:
`http://localhost:8000/v0/timetables/stop/HSJ12`

or, equivalently, for line 704, direction 0, first stop after Terminus:
`http://localhost:8000/v0/timetables/bus/704/0/1`

We obtain a list of the current ETAs for all buses that will pass the chosen station, ex.:
`[["803 ","RIO TINTO ES","now","0min"],["704 ","CODICEIRA -","18:08","4min"],["203 ","MARQUÊS  -","18:13","9min"],["903 ","C.MÚSICA MET","18:16","12min"],["204 ","H.S.JOÃO","18:17","12min"]]`


## Planned features:
- Database caching
    - It is not expected that the bus lines or stops will change frequently. By caching this information in a local store, we can be spared from calling the itinerarium endpoint.
