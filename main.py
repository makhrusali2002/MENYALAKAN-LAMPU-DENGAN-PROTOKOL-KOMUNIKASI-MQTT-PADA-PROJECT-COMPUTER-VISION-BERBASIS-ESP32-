import cv2
from cvzone.HandTrackingModule import HandDetector
import paho.mqtt.client as mqtt #pemanggilan library
import json
#import time

broker = "broker.emqx.io"
topic = "PKL/OpenCV/MQTT"
Client = mqtt.Client()
Client.connect(broker) #connect ke broker

cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.8, maxHands=1) #deteksi maksimum 1 jari

fingerTip = [4, 8, 12, 16, 20] #tipe data list, menyimpan angka, data dari hand landmark, titik2 ujung jari
fingerVal = [0, 0, 0, 0, 0] #menyimpan data hasil pembacaan jari

red = (0,0,255)
yellow = (0,255,255)
blue = (255,0,0)
green = (0,255,0)
purple = (255,0,255)

color = [red, yellow, blue, green, purple] #rgb range 0 - 255, tipe data list

while cap.isOpened(): #selama perintah dijalankan akan bernilai true
    sucess, img = cap.read() #pembacaan gambar
    img = detector.findHands(img, draw = False) #mendeteksi ada atau tidaknya tangan di kamera , draw false menghilangkan titik-titik
    lmList, bbbox = detector.findPosition(img, draw = False) #mentracking posisi tangan, draw false menghilangkan kotak

    if lmList:
        # Thumb , ibu jari berdasarkan sumbu x  deteksi dulu mana tangan kanan atau kiri
        handType = detector.handType() #mendeteksi tangan kanan atau tangan kiri
        if handType == "Right":
            if lmList[fingerTip[0]][0] > lmList[fingerTip[0] - 1][0]: #tangan kanan
                fingerVal[0] = 1 #index 0 untuk ibu jari

            else:
                fingerVal[0] = 0

        else:
            if lmList[fingerTip[0]][0] < lmList[fingerTip[0] - 1][0]: #tangan kiri
                fingerVal[0] = 1

            else:
                fingerVal[0] = 0


        # 4 fingers / 4 jari
        for i in range(1, 5): #looping dari index ke 1 sampai 4, 5 sebagai pembatas
            if lmList[fingerTip[i]][1] < lmList[fingerTip[i] - 2][1]:
                fingerVal[i] = 1

            else:
                fingerVal[i] = 0


            # Draw mark , buat titik-titik warna warni
        for i in range(0, 5):
            if fingerVal[i] == 1:
                cv2.circle(img, (lmList[fingerTip[i]][0], lmList[fingerTip[i]][1]), 15,
                           color[i], cv2.FILLED)

        #strVal = str(fingerVal[0]) + str(fingerVal[1]) + str(fingerVal[2]) + str(fingerVal[3]) + str(fingerVal[4])
        #ubah data angka ke string
        #print(strVal)
        x = {
            "jempol": str(fingerVal[0]),
            "telunjuk": str(fingerVal[1]),
            "tengah": str(fingerVal[2]),
            "manis": str(fingerVal[3]),
           "kelingking": str(fingerVal[4])
        }

        # convert into JSON:
        y = json.dumps(x)

        # the result is a JSON string:
        print(y)

        Client.publish(topic, y)
        #time.sleep(0.5)

        cv2.imshow("Image", img)  # menampilkan gambar
        cv2.waitKey(1)  # jeda menunggu


