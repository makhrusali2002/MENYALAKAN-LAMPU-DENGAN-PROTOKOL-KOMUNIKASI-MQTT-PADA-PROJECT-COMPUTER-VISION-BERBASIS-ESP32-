import paho.mqtt.client as mqtt #pemanggilan library

broker = "broker.emqx.io"
topic = "PKL/OpenCV/MQTT"
Client = mqtt.Client()
Client.connect(broker) #connect ke broker

#buat looping

while True :
    data = input("Masukkan data: ") #input data
    Client.publish(topic, data)
    print(f'Publish Data {data}')