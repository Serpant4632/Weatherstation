// Standard Librarys
#include <Arduino.h>
#include <string.h>

// Librarys for BME280
#include <Wire.h>
#include <Adafruit_BME280.h>
#include <Adafruit_Sensor.h>

// Librarys for MQTT
// https : // github.com/plapointe6/EspMQTTClient
#include <EspMQTTClient.h>

// Wifi Setup ESP32
const char *wifiSsid = "Stachel3";
const char *wifiPassword = "dhbw_kueck_thieser";

// MQTT Broker Setup
const char *mqttServerIp = "192.168.178.112";
const char *mqttUsername = "lukas";
const char *mqttPassword = "Test";
const char *mqttClientName = "ESP32-Client";
const short mqttServerPort = 1883;

EspMQTTClient client(
    wifiSsid,
    wifiPassword,
    mqttServerIp,
    mqttUsername,
    mqttPassword,
    mqttClientName,
    mqttServerPort);

uint32_t lastMsg = 0;

// Activate BME280 for I2C
Adafruit_BME280 bme;

//float temperature = 0;
//float humidity = 0;
float pressure = 0;
//float altitude = 0;

// Sealevel norm Pressure in hpa
#define SEALEVELPRESSURE_HPA (1013.25)

// pin definitions for Weatherstation;
#define Pin1 25 // alt 5
#define Pin2 26 // alt 6
#define Pin3 27 // alt 13
#define Pin4 14 // alt 19
#define Pin5 12 // alt 26

float U = 0;
float V = 0;
bool S = 1;
int Errors = 1;


String speedString;
String tempString;
String humiString;
String pressString;
String altiString;
String direction;

// Function to detect BME errors and reset sensor
void Error(String x);
// If error detected, the BME value of this section will be set to "-3"

void setup()
{
  // Setup Communication
  // setup_wifi();
  Serial.begin(115200);

  client.enableDebuggingMessages();
  client.enableHTTPWebUpdater();
  client.enableOTA();
  client.enableLastWillMessage("ESP32/Weatherstation/Lastwill", "Something went wrong!");

  // Pin declaration for weatherstation
  pinMode(Pin1, INPUT_PULLDOWN);
  pinMode(Pin2, INPUT_PULLDOWN);
  pinMode(Pin3, INPUT_PULLDOWN);
  pinMode(Pin4, INPUT_PULLDOWN);
  pinMode(Pin5, INPUT_PULLDOWN);

  // I2C begin adress from Daniel Funkte
  if (!bme.begin(0x77))
  { // GPIO 21 = SDA / GPIO 22 = SCL / I2C-Bus
    Serial.printf("Can't find any BME280 sensor. \nPlease check your wiring!");
    while (true)
      ;
  }
}

void onConnectionEstablished()
{
  // Subscribe to "mytopic/test" and display received message to Serial
  // client.subscribe("mytopic/test", [](const String &payload)
  //                 { Serial.println(payload); });

  // Publish a message to "mytopic/test"
  client.publish("ESP32/Weatherstation/Initial", "Weatherstation initial message!"); // You can activate the retain flag by setting the third parameter to true

  // Execute delayed instructions
  // client.executeDelayed(5 * 1000, []()
  // { client.publish("ESP32/Weatherstation/Test2", "This is a message sent 5 seconds later"); });
}

void loop()
{
  
  client.loop();

  // Meassurement of wind speed
  while ((millis() - lastMsg) < 10000)
  {

    if ((1 == S) && (0 == digitalRead(Pin1)))
    {
      S = 0;
    }

    if ((0 == S) && (1 == digitalRead(Pin1)))
    {
      S = 1;
      U += 1;
    }
  }

  // 10 seconds interval for data update
  lastMsg = millis();

  // Calculation of Speed in m/s
  V = (U / 10) * 0.97;

  // Convert meassurement to String
  speedString = String(V);
  speedString = speedString + " m/s";
  // Serial.printf("Wind speed:\t%s m/s\n", speedString);

  // Tempratur in °C
  // Convert the value to String 
  tempString = String(bme.readTemperature());
  // Temprature in F, please uncomment next line
  // temperature = 1.8 * bme.readTemperature() + 32;
  Error(tempString);
  tempString = tempString + " °C";
  // Serial.printf("Temperature:\t%s\n", tempString);

  // Humidity in %
  // Convert the value to String
  humiString = String(bme.readHumidity());
  Error(humiString);
  humiString = humiString + " %";
  // Serial.printf("Humidity:\t%s °C\n", humiString);

  // Preassure in hPa
  // Convert the value to String
  pressure = bme.readPressure() / 100.0F;
  pressString = String(pressure);
  Error(pressString);
  pressString = pressString + " hPa";
  // Serial.printf("Pressure:\t%s hPa\n", pressString);

  // Altitude in m
  // Convert the value to String
  altiString = String(bme.readAltitude(SEALEVELPRESSURE_HPA));
  Error(altiString);
  altiString = altiString + " m";
  // Serial.printf("Sealevel:\t%s m\n", altiString);
  /*
  The altitude in meters can be calculated with the international barometric formula :
      H = 44330 * [1 - (P / p0) ^ (1 / 5.255)]
      H = altitude(m)
      P = measured pressure(Pa) from the sensor
      p0 = reference pressure at sea level (e.g.1013.25hPa)
  */

  // Meassurement of wind direction
  if (digitalRead(Pin4) && (!digitalRead(Pin5)) && (!digitalRead(Pin3)))
  {
    direction = "S";
  }
  if (digitalRead(Pin4) && (digitalRead(Pin3)))
  {
    direction = "SW";
  }
  if (!digitalRead(Pin4) && (!digitalRead(Pin2)) && (digitalRead(Pin3)))
  {
    direction = "W";
  }
  if (digitalRead(Pin2) && (digitalRead(Pin3)))
  {
    direction = "NW";
  }
  if (digitalRead(Pin2) && (!digitalRead(Pin5)) && (!digitalRead(Pin3)))
  {
    direction = "N";
  }
  if (digitalRead(Pin2) && (digitalRead(Pin5)))
  {
    direction = "NO";
  }
  if (!digitalRead(Pin4) && (digitalRead(Pin5)) && (!digitalRead(Pin2)))
  {
    direction = "O";
  }
  if (digitalRead(Pin4) && (digitalRead(Pin5)))
  {
    direction = "SO";
  }
  if (0 == V)
  {
    direction = "Windstill";
  }
  // Serial.printf("Wind_Direction:\t%s\n",direction);

  // Publish data
  if (tempString == "nan °C"){}
  else{
    client.publish("ESP32/Weatherstation/Temperature", tempString);
  }

  if (pressString == "nan hPa"){}
  else{
    client.publish("ESP32/Weatherstation/Pressure", pressString);
  }

  if (humiString == "nan %"){}
  else{
    client.publish("ESP32/Weatherstation/Humidity", humiString);
  }

  if (altiString == "nan m"){}
  else{
    client.publish("ESP32/Weatherstation/Sealevel", altiString);
  }

  client.publish("ESP32/Weatherstation/Wind_Direction", direction);
  client.publish("ESP32/Weatherstation/Wind_Speed", speedString);

  // Reset speed value 
  V = 0;
  U = 0;
}


void Error (String x){
  String payload;
  payload = "BME280 error occured!!!";
  if (x == "nan"){
    client.publish("ESP32/Weatherstation/Error", payload);
    bme.begin(0x77); // Softreset BME280
    delay(100);
    Errors++; // Error counter
  }
}