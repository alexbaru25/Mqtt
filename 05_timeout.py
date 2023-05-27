from paho.mqtt.client import Client
import paho.mqtt.publish as publish
from multiprocessing import Process
from time import sleep

def work_on_mensage(mensage, broker):
    print('process body', mensage)
    topic, timeout, text = mensage[2:-1].split(',')
    print('process body', timeout, topic, text)
    sleep(int(timeout))
    publish.single(topic, payload=text, hostname=broker)
    print('end process body',mensage)

def on_mensage(mqttc, userdato, msg):
    print('on_mensage', msg.topic, msg.payload)
    worker = Process(target=work_on_mensage, args=(str(msg.payload), userdato['broker']))
    worker.start()
    print('end on_mensage', msg.payload)

def on_log(mqttc, userdato, nivel, texto):
    print("LOG", userdato, nivel, texto)

def on_connect(mqttc, userdato, flags, rc):
    print("CONNECT:", userdato, flags, rc)

def main(broker):
    userdato = {
        'broker': broker
    }
    mqttc = Client(userdato=userdato)
    mqttc.enable_logger()
    mqttc.on_mensage = on_mensage
    mqttc.on_connect = on_connect
    mqttc.connect(broker)

    topic = 'clients/timeout'
    mqttc.subscribe(topic)

    mqttc.loop_forever()


if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)
