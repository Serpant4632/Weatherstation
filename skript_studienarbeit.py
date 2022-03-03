import paho.mqtt.client as mqtt
import time
import csv

def on_log(client, userdata, level, buf):
    print("log "+buf)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection Returned code", rc)
        
def on_disconnect(client, userdata, flags, rc=0):
    print("DisConnected result code ",+str(rc))
    
def on_message(client, userdata, message):
    global i
    print("Received message: ", str(message.payload.decode("utf-8")))
    with open('studienarbeitcsv.csv','a') as f:
        writer = csv.writer(f)
        if message.topic == "ESP32/Weatherstation/Temperature":
            temp_list.append(str(message.payload.decode("utf-8")))
            
        if message.topic == "ESP32/Weatherstation/Humidity":
            hum_list.append(str(message.payload.decode("utf-8")))
            
        if message.topic == "ESP32/Weatherstation/Pressure":
            pres_list.append(str(message.payload.decode("utf-8")))
            
        if message.topic == "ESP32/Weatherstation/Sealevel":
            sea_list.append(str(message.payload.decode("utf-8")))
            
        if message.topic == "ESP32/Weatherstation/Wind_Speed":
            wind_list.append(str(message.payload.decode("utf-8")))
        if message.topic == "ESP32/Weatherstation/Wind_Direction":
            wind_list.append(str(message.payload.decode("utf-8")))     
i=0           
temp_list = ["Temperature: "]
hum_list = ["Humidity: "]
pres_list = ["Airpressure: "]
sea_list = ["Sea_Level: "]
wind_list = ["Wind_Speed: "]
direct_list = ["Wind_Direction: "]

    
broker="192.168.178.112"
client=mqtt.Client("Testaufzeichnung")
client.username_pw_set(username="lukas", password="Test")

client.on_connect=on_connect
client.on_disconnect=on_disconnect
#client.on_log=on_log

print("Connecting to broker ", broker)

client.connect(broker)
client.loop_start()
client.subscribe("ESP32/Weatherstation/Temperature")
client.subscribe("ESP32/Weatherstation/Humidity")
client.subscribe("ESP32/Weatherstation/Pressure")
client.subscribe("ESP32/Weatherstation/Sealevel")
client.subscribe("ESP32/Weatherstation/Wind_Speed")
client.subscribe("ESP32/Weatherstation/Wind_Direction")
client.on_message = on_message
time.sleep(7200)
client.loop_stop()
i=1
#listoflists.append((temp_list,hum_list,pres_list))
#dictionary=dict(liste1,liste2)
#print(dictionary)
with open('studienarbeitcsv.csv','w') as f:
    writer = csv.writer(f)  
    if i == 1:
        writer.writerow(temp_list)
        writer.writerow(hum_list)
        writer.writerow(pres_list)
        writer.writerow(sea_list)
        writer.writerow(wind_list)
        writer.writerow(direct_list)
        
