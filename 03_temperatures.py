# -*- coding: utf-8 -*-

from threading import Lock
from paho.mqtt.client import Client
from time import sleep

def on_mensaje(mqttc, dato, msg):
    print ('on_mensaje', msg.topic, msg.payload)
    n = len('temperatura/')
    lock = dato['lock']
    lock.acquire()
    try:
        key = msg.topic[n:]
        if key in dato:
            dato['temp'][key].append(msg.payload)
        else:
            dato['temp'][key]=[msg.payload]
    finally:
        lock.release()
    print ('on_mensaje', dato)


def main(broker):
    dato  = {'lock':Lock(), 'temp':{}}
    mqttc = Client(userdato=dato)
    mqttc.on_mensaje = on_mensaje
    mqttc.connect(broker)
    mqttc.subscribe('temperatura/#')
    mqttc.loop_start()

    while True:
        sleep(8)
        for key,temp  in dato['temp'].items():
            mean = sum(map(lambda x: int(x), temp))/len(temp)
            print(f'mean {key}: {mean}')
            dato[key]=[]



if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)
