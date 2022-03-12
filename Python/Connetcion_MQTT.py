import paho.mqtt.client as mqtt             # pip install paho-mqtt
import time
import csv

def on_log(client, userdata, level, buf):                              #Wird aufgerufen, wenn der Client Protokollinformationen hat. Definieren um Debugging zu ermöglichen.
    print("log "+buf)
def on_connect(client, userdata, flags, rc):                           # Bestätigt den erfolgreichen connect mit dem Broker. rc ungleich 0 bedeutet fehlerhafte Ausführung des Protokoll
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code", rc)
        
def on_disconnect(client, userdata, flags, rc=0):                      #bestätigt den erfolgreichen disconnect. Bei erfolgreichem disconnect wird der return-call (rc) auf 0 gesetzt
    print("DisConnected result code ",+str(rc))
    
def on_message(client, userdata, message):                             #empfängt client="clientnoah" und message mit dem entsprechenden payload des Sensors.
                                                                       #Parameter "userdata" enthält unter Umständen Daten für eine Callbackfunktion. In diesem Fall nicht verwendet.
    print("Received message: ", str(message.payload.decode("utf-8")))  #Gibt die empfangenen daten aus und formt sie in einen String um nach UTF-8
    
    if message.topic == "ESP32/Weatherstation/Temperature":     # vergleicht die Bezeichnung der Topic
        temp_list.append(str(message.payload.decode("utf-8")))  # Durch die If-Bedingungen werden mittels der append Methode in jedem
            
    if message.topic == "ESP32/Weatherstation/Humidity":
        hum_list.append(str(message.payload.decode("utf-8")))   # Zyklus die empfangenen Daten in die jeweilige Liste geschrieben
            
    if message.topic == "ESP32/Weatherstation/Pressure":
        pres_list.append(str(message.payload.decode("utf-8")))
            
    if message.topic == "ESP32/Weatherstation/Sealevel":
        sea_list.append(str(message.payload.decode("utf-8")))
            
    if message.topic == "ESP32/Weatherstation/Wind_Speed":
        wind_list.append(str(message.payload.decode("utf-8")))    
          
temp_list = ["Temperature: "] #Erstellung der Listen um die entsprechenden Daten zwischenzuspeichern 
hum_list = ["Humidity: "]
pres_list = ["Windpressure: "]
sea_list = ["Sea_Level: "]
wind_list = ["Wind_Speed: "]

    
broker="192.168.178.112" #IP-Adresse des Brokers mit dem die Verbindung hergestellt werden soll
client=mqtt.Client("clientnoah") #Erstellung Objekt auf der MQTT Klasse. beinhaltet die userdata "clientnoah"
client.username_pw_set(username="lukas", password="Test") #Übergabe des Benutzernamen und Passwort um sich an den Broker anzukoppeln

client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_log=on_log

print("Connecting to broker: ", broker)

client.connect(broker)
client.loop_start()                                  #startet die Messwerterfassung indem es die Loop startet
client.subscribe("ESP32/Weatherstation/Temperature") #Über die Methode "subscribe" werden die entsprechenden Topic abonniert
client.subscribe("ESP32/Weatherstation/Humidity")    #übergibt die Parameter "topic" und qos=0 by default
client.subscribe("ESP32/Weatherstation/Pressure")
client.subscribe("ESP32/Weatherstation/Sealevel")
client.subscribe("ESP32/Weatherstation/Wind_Speed")
client.on_message = on_message                       # Übergabe an die Funktion "on_message" mittels der Methode "on_message". Parameter client und message werden übergeben.
time.sleep(80)                                       # Zeitverzögerung zwischen loop_start und loop_stop. Bestimmt die Zeit in Sekunden, in der Daten empfangen werden können.
client.loop_stop()                                   #Stoppt die Messwerterfassung, indem es die Loop beendet

with open('studienarbeitcsv.csv','w') as f:          #Öffnet das CSV-File und benennt es nach f um
    writer = csv.writer(f)                           #erstellt Objekt der Klasse csv.writer
    
    writer.writerow(temp_list)                       #Schreibt die Listen mit den Daten in die CSV-Datei
    writer.writerow("\n")                            #Dadurch werden Umbrüche erzeugt, da sonst alle Daten in eine Zeile in der Datei geschrieben würden
    writer.writerow(hum_list)                       
    writer.writerow("\n")
    writer.writerow(pres_list)
    writer.writerow("\n")
    writer.writerow(sea_list)
    writer.writerow("\n")
    writer.writerow(wind_list)
        
        
        

