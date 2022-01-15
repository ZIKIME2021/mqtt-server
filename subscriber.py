import paho.mqtt.client as mqtt
import redis

rd = redis.StrictRedis(host='www.zikime.com', port=6379, db=0)

# subscriber callback
def on_message(client, userdata, message):
    decode_msg = str(message.payload.decode("utf-8"))
    #print("message received ", decode_msg)
    #print("message topic=", message.topic)
    #print("message qos=", message.qos)
    #print("message retain flag=", message.retain)

    device, serial, state = message.topic.split('/')
    print("serial:", serial)

    if message.topic == "device/connect":
        pass
    elif message.topic == "device/register":
        pass
    elif state == "position":
        latitude, longitude = map(float, decode_msg.split(','))
        print("latitude:", latitude, '  ', "longitude:", longitude)
    elif state == "power":
        print("power:", decode_msg)
    elif state == "mode":
        print("mode:", decode_msg)

broker_address = "0.0.0.0"
client1 = mqtt.Client("client1")
client1.connect(broker_address, 8080)
client1.subscribe("device/+/#")
client1.on_message = on_message

client1.loop_forever()

