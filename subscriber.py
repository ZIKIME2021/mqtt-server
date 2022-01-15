from collections import defaultdict

import paho.mqtt.client as mqtt
import redis
import json

state_info_dict = defaultdict(str)

rd = redis.StrictRedis(host='localhost', port=6379, db=0)

def on_message(client, userdata, message):
    decode_msg = str(message.payload.decode("utf-8"))

    device, serial, state = message.topic.split('/')
    print("serial:", serial)
    
    state_info = {
        "power": True,
        "latitude": '',
        "longitude": '',
        "mode": ''
    }
    
    state_info_dict[serial] = state_info
    
    json_already_state = rd.get(serial).decode('utf-8')
    already_state = dict(json.loads(json_already_state))
    
    if "mode" in already_state.keys():
        state_info_dict[serial]["mode"] = already_state["mode"]
    if "latitude" in already_state.keys():
        state_info_dict[serial]["latitude"] = already_state["latitude"]
        state_info_dict[serial]["longitude"] = already_state["longitude"]
        
    if message.topic == "device/+/connect":
        pass
    elif message.topic == "device/+/register":
        pass
    elif state == "position":
        latitude, longitude = map(float, decode_msg.split(','))
        state_info_dict[serial]["latitude"] = latitude
        state_info_dict[serial]["longitude"] = longitude
        
        print("latitude:", latitude, '  ', "longitude:", longitude)
        
    elif state == "mode":
        state_info_dict[serial]["mode"] = decode_msg
        print("mode:", decode_msg)
        
    json_state_info = json.dumps(state_info_dict[serial], ensure_ascii=False).encode('utf-8')
    rd.set(serial, json_state_info)
    
    print(state_info_dict[serial])

broker_address = "localhost"
client1 = mqtt.Client("client1")
client1.connect(broker_address, 1883)
client1.subscribe("device/+/#")
client1.on_message = on_message

client1.loop_forever()

