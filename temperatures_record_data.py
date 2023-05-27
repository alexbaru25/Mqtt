# -*- coding: utf-8 -*-

from paho.mqtt.client import Client

def on_message(mqttc, dato, msg):
    print ('on_message', msg.topic, msg.payload)
    n = len('temperature/')
    key = msg.topic[n:]
    if key in dato:
        dato[key].append(msg.payload)
    else:
        dato[key]=[msg.payload]
    print ('on_message', dato)

def main():
    mqttc = Client(userdato={})
    mqttc.on_message = on_message
    mqttc.connect("wild.mat.ucm.es")
    mqttc.subscribe('temperature/#')
    mqttc.loop_forever()

if __name__ == "__main__":
    main()
