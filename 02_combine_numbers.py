from paho.mqtt.client import Client
from multiprocessing import Process, Manager
from time import sleep
import random

NUMBERS = 'numbers'
CLIENTS = 'clients'
TIMER_STOP = f'{CLIENTS}/timerstop'
HUMIDITY = 'humidity'


def is_prime(n):
    i = 2
    while i*i < n and n % i != 0:
        i += 1
    return i*i > n


def timer(time, dato):
    mqttc = Client()
    mqttc.connect(dato['broker'])
    msg = f'timer working. timeout: {time}'
    print(msg)
    mqttc.publish(TIMER_STOP, msg)
    sleep(time)
    msg = f'timer working. timeout: {time}'
    mqttc.publish(TIMER_STOP, msg)
    print('timer end working')
    mqttc.disconnect()


def on_mensaje(mqttc, dato, msg):
    print(f"mensaje:dato:{dato}, msg.topic:{msg.topic}, payload:{msg.payload}")
    try:
        #if is_prime(int(msg.payload)):
        if int(msg.payload) % 2 == 0:
            worker = Process(target=timer,
                             args=(random.random()*20, dato))
            worker.start()
    except ValueError as e:
        print(e)
        pass


def on_log(mqttc, userdato, level, string):
    print("LOG", userdato, level, string)


def main(broker):
    dato = {'client':None,
            'broker': broker}
    mqttc = Client(client_id="combine_numbers", userdato=dato)
    dato['client'] = mqttc
    mqttc.enable_logger()
    mqttc.on_mensaje = on_mensaje
    mqttc.on_log = on_log
    mqttc.connect(broker)
    mqttc.subscribe(NUMBERS)
    mqttc.loop_forever()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)
