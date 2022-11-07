#include <ESP8266WiFi.h> //library for wifi esp8266
#include <PubSubClient.h>
const char* ssid = "Plezz9";
const char* password = "adgjm1922";
const char* mqttServer = "broker.emqx.io";
int port = 1883;
char clientId[50];

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

#define pinRed D0
#define pinYellow D3
#define pinBlue D5
#define pinPurple D6
#define pinGreen D4

void setup() {
  pinMode(pinRed, OUTPUT);
  pinMode(pinYellow, OUTPUT);
  pinMode(pinBlue, OUTPUT);
  pinMode(pinPurple, OUTPUT);
  pinMode(pinGreen, OUTPUT);
  Serial.begin(115200);
  randomSeed(analogRead(0));

  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  wifiConnect();
  client.setServer(mqttServer, port);
  client.setCallback(callback);
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("MAC Address: ");
 Serial.println(WiFi.macAddress());
 WiFi.setAutoReconnect(true);
 WiFi.persistent(true);
  
}

void wifiConnect() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  };

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    long r = random(1000);
    sprintf(clientId, "clientId-%ld", r);
    if (client.connect(clientId)) {
      Serial.print(clientId);
      Serial.println(" connected");
      client.subscribe("PKL/OpenCV/MQTT");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void callback(char* topic, byte* message, unsigned int length) {
  
    if((char)message[0] == '1'){
      digitalWrite(pinRed, HIGH);
    }
    else{
      digitalWrite(pinRed, LOW);
    }
    if((char)message[1] == '1'){
      digitalWrite(pinYellow, HIGH);
    }
    else{
      digitalWrite(pinYellow, LOW);
    }
    if((char)message[2] == '1'){
      digitalWrite(pinBlue, HIGH);
    }
    else{
      digitalWrite(pinBlue, LOW);
    }
    if((char)message[3] == '1'){
      digitalWrite(pinPurple, HIGH);
    }
    else{
      digitalWrite(pinPurple, LOW);
    }
    if((char)message[4] == '1'){
      digitalWrite(pinGreen, HIGH);
    }
    else{
      digitalWrite(pinGreen, LOW);
    }
}

void loop() {
  delay(10);
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
