# sikulix
An example project to test sikulix capabilities on multiple applications on different screens

The folder will contains two applications, client and server, that communicate one with the other using a TCP connections.
They will contain buttons and textboxes that will be updated through the actions of the opposite aplication.

## How to run

### Server
From the root folder, run the server application using `python3 src/server.py`. Once started the app, start the server by clicking "Start Server"

### Client
From the root folder, run the client application using `python3 src/client.py`. Once started the app, connect to the server by clicking "Connect"

You should see both the applications displaying green messages telling "connection accepted"

### Sikulix
The sikulix IDE can be started by typing `java -jar sx.jar`

Then, you have to load the script `client_server_1` and start it using the IDE.
