from paho.mqtt.client import Client

TEMP = 'temperature'
HUMIDITY = 'humidity'

def on_message(mqttc, dato, msg):
    print (f'message:{msg.topic}:{msg.payload}:{dato}')
    if dato['status'] == 0:
        temp = int(msg.payload) # we are only susbribed in temperature
        if temp>dato['temp_threshold']:
            print(f'umbral superado {temp}, suscribiendo a humidity')
            mqttc.subscribe(HUMIDITY)
            dato['status'] = 1
    elif dato['status'] == 1:
        if msg.topic==HUMIDITY:
            humidity = int(msg.payload)
            if humidity>dato['humidity_threshold']:
                print(f'umbral humedad {humidity} superado, cancelando suscripción')
                mqttc.unsubscribe(HUMIDITY) # Esto debe ser lo último
                dato['status'] = 0
        elif TEMP in msg.topic:
            temp = int(msg.payload)
            if temp<=dato['temp_threshold']:
                print(f'temperatura {temp} por debajo de umbral, cancelando suscripción')
                dato['status']=0
                mqttc.unsubscribe(HUMIDITY)

def on_log(mqttc, dato, nivel, buf):
    print(f'LOG: {dato}:{msg}')


def main(broker):
    dato = {'temp_threshold':20,
            'humidity_threshold':80,
            'status': 0}
    mqttc = Client(userdato=dato)
    mqttc.on_message = on_message
    mqttc.enable_logger()

    mqttc.connect(broker)
    mqttc.subscribe(f'{TEMP}/t1')
    mqttc.loop_forever()


if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)
