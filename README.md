# Weatherstation

In der folgenden Studienarbeit wird eine OTA Anbindung für eine Wetterstation entwickelt. 
Die Entwicklung wird über einen MQTT-Broker und ein ESP32 Modul umgesetzt. 
Die Daten werden alle 10 Sekunden vom ESP32 an den MQTT-Broker gesendet. 

Dazu werden die folgenden Programme benutzt:
- MQTT-Explorer: http://mqtt-explorer.com
- Eclipse Mosquitto: https://mosquitto.org
- PlatformIO: https://platformio.org
- Visual Studio Code: https://code.visualstudio.com
-  Digi-Key Scheme-it: https://www.digikey.de/schemeit/home/

Die verwendetet Hardware ist:
- ESP32: 
https://joy-it.net/de/products/SBC-NodeMCU-ESP32
- Raspberry Pi 3 B+: 
https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/
- Wetterstation einer vorherigen Studienarbeit

Zusätzlich wird ein neuer Schaltplan zur vorhanden Platine erstellt um den Anschluss und weitere Arbeiten an dem Projekt zu erleichtern, dazu wurde die Software Fusion360 von Autodesk (https://www.autodesk.de/products/fusion-360/overview) verwendet. 

Die Projektdatei in Digi-Key Scheme-it wird unterfolgendem Link bereit gestellt.
https://www.digikey.de/schemeit/project/studienarbeit-3b60e44e636847fb8b4f15b76554895c

In einer parallel laufenden Studienarbeit wird ein Smarthome-Controller mittels NodeRed entwickelt um die Daten der Wetterstation zu verarbeiten und visualisieren. 
Der Code zur NodeRed und Python Programmierung liegt in den entsprechenden Unterordnern.


////////////////////////////////////////////////////////////////////////////////////////////////////////////////


In the following student research project an OTA connection for a weather station is developed. 
The development is implemented using an MQTT broker and an ESP32 module. 
Data is sent from the ESP32 to the MQTT broker every 10 seconds.

The following programs are used for this purpose:
- MQTT Explorer: http://mqtt-explorer.com
- Eclipse Mosquitto: https://mosquitto.org
- PlatformIO: https://platformio.org
- Visual Studio Code: https://code.visualstudio.com
- Digi-Key Scheme-it: https://www.digikey.de/schemeit/home/

The used hardware is:
- ESP32: 
https://joy-it.net/de/products/SBC-NodeMCU-ESP32
- Raspberry Pi 3 B+: 
https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/
- Weather station from a previous student research project

In addition, a new schematic to the existing board is created to facilitate connection and further work on the project,
using Autodesk's Fusion360 software: https://www.autodesk.de/products/fusion-360/overview

The project file in Digi-Key Scheme-it is provided at the following link.
https://www.digikey.de/schemeit/project/studienarbeit-3b60e44e636847fb8b4f15b76554895c

In a parallel student research project a smarthome controller is developed using NodeRed to process and visualize the data of the weather station.
The code for NodeRed and Python programming is located in the corresponding subfolders.

