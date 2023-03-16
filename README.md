STCP provides a variety of undocumented endpoints containing data for real time bus arrivals.
The goal is to create a simple and self-hostable REST API for integration with other applications, since the operator does not provide one themselves.

#### Usage
This app is in a very early stage.
Install the requirements, then start the application (default port 8000) by running `uvicorn app:app` (or run `. ./scripts/entry.sh`).
Basic functionality can be tested by sending a request with line code and stop number.
Ex. for line 704, stop 1:
`http://localhost:8000/704/1`
We should get a response similar to:
`[["203 ","MARQUÊS  -","now","0min"],["903 ","C.MÚSICA MET","12:43","1min"],["204 ","H.S.JOÃO","12:50","8min"],["204 ","H.S.JOÃO","12:57","15min"],["203 ","MARQUÊS  -","13:00","18min"]]`