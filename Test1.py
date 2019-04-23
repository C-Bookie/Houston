#testing phue and mqtt for motion sensing lights

import phue
import time
import random

import paho.mqtt.client as paho


def test1():
    b = phue.Bridge('192.168.1.211')
    b.connect()
    print(b.get_api())

    state = False
    for i in range(100):
        state = not state
        command = {
            'transitiontime': 1,
#            'on': state,
#            'bri': 255,
            'hue':random.randint(0, 255)
        }
        b.set_light('cal', command)
        time.sleep(0.1)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def test2():
    client = paho.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("127.0.0.1", 1883, 60)

    client.loop_forever()

if __name__ == "__main__":
    test2()


