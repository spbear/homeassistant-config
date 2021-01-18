#!/usr/bin/python3
import json
replacement = {
    "민준이방 스위치 Temperature Measurement" : {
        "name" : "Minjun's Room Temperature",
        "entity_id" : "sensor.minjun_room_temperature",
        "icon" : "mdi:thermometer"
    },
    "민준이방 스위치 Relative Humidity Measurement" : {
        "name" : "Minjun's Room Humidity",
        "entity_id" : "sensor.minjun_room_humidity",
        "icon" : "mdi:water-percent"
    },
    "현준이방 스위치 Temperature Measurement" : {
        "name" : "Hyunjun's Room Temperature",
        "entity_id" : "sensor.hyunjun_room_temperature",
        "icon" : "mdi:thermometer"
    },
    "현준이방 스위치 Relative Humidity Measurement" : {
        "name" : "Hyunjun's Room Humidity",
        "entity_id" : "sensor.hyunjun_room_humidity",
        "icon" : "mdi:water-percent"
    },
    "현준이방 조도 Illuminance" : {
        "name" : "Hyunjun's Room Illuminance",
        "entity_id" : "sensor.hyunjun_room_illuminance",
        "icon" : "mdi:brightness-5"
    },
    "민준이방 조도 Illuminance" : {
        "name" : "Minjun's Room Illuminance",
        "entity_id" : "sensor.minjun_room_illuminance",
        "icon" : "mdi:brightness-5"
    },
    "화장실 스위치 Temperature Measurement" : {
        "name" : "Passage Temperature",
        "entity_id" : "sensor.passage_temperature",
        "icon" : "mdi:thermometer"
    },
    "화장실 스위치 Relative Humidity Measurement" : {
        "name" : "Passage Humidity",
        "entity_id" : "sensor.passage_humidity",
        "icon" : "mdi:water-percent"
    },
    "주방 온습도 Temperature Measurement" : {
        "name" : "Kitchen Temperature",
        "entity_id" : "sensor.kitchen_temperature",
        "icon" : "mdi:thermometer"
    },
    "주방 온습도 Relative Humidity Measurement" : {
        "name" : "Kitchen Humidity",
        "entity_id" : "sensor.kitchen_humidity",
        "icon" : "mdi:water-percent"
    },
    "PC 모니터" : {
        "name" : "PC Monitor",
        "entity_id" : "switch.pc_monitor",
        "icon" : "mdi:monitor"
    },
    "내 방 양키 캔들" : {
        "name" : "My Room Yankee Candle",
        "entity_id" : "switch.my_room_yankee_candle",
        "icon" : "mdi:flower"
    },
    "주방 양키캔들" : {
        "name" : "Kitchen Yankee Candle",
        "entity_id" : "switch.kitchen_yankee_candle",
        "icon" : "mdi:flower"
    },
    "현준이방 모기향" : {
        "name" : "Hyunjun's Room Mosquitto Protector",
        "entity_id" : "switch.hyunjun_mosquitto_protector",
        "icon" : "mdi:bug"
    },
    "거실 모션 motion" : {
        "name" : "Livingroom Motion",
        "entity_id" : "binary_sensor.livingroom_motion",
        "icon" : "mdi:walk"
    },
    "복도 센서 motion" : {
        "name" : "Passage Motion",
        "entity_id" : "binary_sensor.passage_motion",
        "icon" : "mdi:walk"
    },
    "주방 센서 motion" : {
        "name" : "Kitchen Motion",
        "entity_id" : "binary_sensor.kitchen_motion",
        "icon" : "mdi:walk"
    },
    "화장실 멀티센서 motion" : {
        "name" : "Restroom Motion",
        "entity_id" : "binary_sensor.restroom_motion",
        "icon" : "mdi:walk"
    },
    "세탁실 문 contact" : {
        "name" : "Washing Room Door",
        "entity_id" : "binary_sensor.washing_room_door",
        "icon" : "mdi:door-closed"
    },
    "주방 창문 contact" : {
        "name" : "Kitchen Window",
        "entity_id" : "binary_sensor.kitchen_window",
        "icon" : "mdi:door-closed"
    },
    "거실 창문 contact" : {
        "name" : "Livingroom Window",
        "entity_id" : "binary_sensor.livingroom_window",
        "icon" : "mdi:door-closed"
    },
    "Entrance Door contact" : {
        "name" : "Entrace Door",
        "entity_id" : "binary_sensor.entrance_door",
        "icon" : "mdi:door-closed"
    },
    "현준이방 창문 contact" : {
        "name" : "Hyunjun's Room Window",
        "entity_id" : "binary_sensor.hyunjun_window",
        "icon" : "mdi:window-open-variant"
    },
    "민준이방 창문 contact" : {
        "name" : "Minjun's Room Window",
        "entity_id" : "binary_sensor.minjun_window",
        "icon" : "mdi:window-open-variant"
    },
    "아이들방 입구 센서 motion" : {
        "name" : "Kids Room Entrance Motion",
        "entity_id" : "binary_sensor.kids_room_entrance_motion",
        "icon" : "mdi:walk"
    },
    "My Room Motion Sensor motion" : {
        "name" : "My Room Motion",
        "entity_id" : "binary_sensor.room_door_motion",
        "icon" : "mdi:walk"
    },
    "내 방 전등" : {
        "name" : "My Room Light",
        "entity_id" : "switch.my_room_light",
        "icon" : "mdi:ceiling-light"
    },
    "복도 전등" : {
        "name" : "Passage Light",
        "entity_id" : "switch.passage_light",
        "icon" : "mdi:ceiling-light"
    },
    "거실 전등" : {
        "name" : "Livingroom Light",
        "entity_id" : "switch.livingroom_light",
        "icon" : "mdi:ceiling-light"
    },
    "거실 보조등" : {
        "name" : "Livingroom Sub Light",
        "entity_id" : "switch.livingroom_sub_light",
        "icon" : "mdi:ceiling-light"
    },
    "화장실 전등" : {
        "name" : "Restroom Light",
        "entity_id" : "switch.restroom_light",
        "icon" : "mdi:ceiling-light"
    },
    "화장실 팬" : {
        "name" : "Restroom Fan",
        "entity_id" : "switch.restroom_fan",
        "icon" : "mdi:fan"
    },
    "현준이방 전등" : {
        "name" : "Hyunjun's Room Light",
        "entity_id" : "switch.hyunjun_room_light",
        "icon" : "mdi:ceiling-light"
    },
    "민준이방 전등" : {
        "name" : "Minjun's Room Light",
        "entity_id" : "switch.minjun_room_light",
        "icon" : "mdi:ceiling-light"
    },
    "현준이방 창고 전등" : {
        "name" : "Hyunjun's Garage Light",
        "entity_id" : "switch.hyunjun_garage_light",
        "icon" : "mdi:ceiling-light"
    },
    "민준이방 스탠드 조명" : {
        "name" : "Minjun's Stand Lamp",
        "entity_id" : "light.minjun_stand_lamp",
        "icon" : "mdi:floor-lamp"
    },
    "현준이방 스텐드 조명" : {
        "name" : "Hyunjun's Stand Lamp",
        "entity_id" : "light.hyunjun_stand_lamp",
        "icon" : "mdi:floor-lamp"
    },
    "주방 전등" : {
        "name" : "Kitchen Light",
        "entity_id" : "switch.kitchen_light",
        "icon" : "mdi:ceiling-light"
    },
    "주방 보조등" : {
        "name" : "Kitchen Sub Light",
        "entity_id" : "switch.kitchen_sub_light",
        "icon" : "mdi:ceiling-light"
    },
    "식탁 전등" : {
        "name" : "Kitchen Table Light",
        "entity_id" : "switch.table_light",
        "icon" : "mdi:ceiling-light"
    },
    "세탁기" : {
        "name" : "Washing Machine",
        "entity_id" : "switch.washing_machine",
        "icon" : "mdi:washing-machine"
    },
    "주방 후드" : {
        "name" : "Kitchen Hood",
        "entity_id" : "switch.kitchen_hood",
        "icon" : "mdi:home-roof"
    },
    "현준이방 선풍기" : {
        "name" : "Hyunjun's Fan",
        "entity_id" : "switch.hyunjun_fan",
        "icon" : "mdi:fan"
    },
    "민준이방 선풍기" : {
        "name" : "Minjun's Fan",
        "entity_id" : "switch.minjun_fan",
        "icon" : "mdi:fan"
    },
    "거실 TV 컨트롤" : {
        "name" : "Livingroom TV Control",
        "entity_id" : "switch.livingroom_tv_control",
        "icon" : "mdi:television-classic"
    },
    "플러그 거실 TV" : {
        "name" : "Livingroom TV Plug",
        "entity_id" : "switch.livingroom_tv_plug",
        "icon" : "mdi:television-classic"
    },
    "에어콘" : {
        "name" : "Livingroom Airconditioner",
        "entity_id" : "switch.livingroom_airconditioner",
        "icon" : "mdi:air-conditioner"
    },
    "거실 에어콘 컨트롤" : {
        "name" : "Livingroom Airconditioner Control",
        "entity_id" : "switch.livingroom_airconditioner_control",
        "icon" : "mdi:air-conditioner"
    },
    "플러그 거실 에어콘" : {
        "name" : "Livingroom Airconditioner Plug",
        "entity_id" : "switch.livingroom_airconditioner_plug",
        "icon" : "mdi:air-conditioner"
    },
    "주방 조도 Illuminance" : {
        "name" : "Kitchen Illuminance",
        "entity_id" : "sensor.kitchen_illuminance",
        "icon" : "mdi:brightness-5"
    },
    "거실 조도 Illuminance" : {
        "name" : "Livingroom Illuminance",
        "entity_id" : "sensor.livingroom_illuminance",
        "icon" : "mdi:brightness-5"
    },
    "아이들방 입구 센서 Illuminance" : {
        "name" : "Passage Illuminance",
        "entity_id" : "sensor.passage_illuminance",
        "icon" : "mdi:brightness-5"
    },
    "메인 모니터" : {
        "name" : "Main PC Monitor",
        "entity_id" : "switch.main_pc_monitor",
        "icon" : "mdi:monitor"
    },
    "보조 모니터" : {
        "name" : "Sub PC Monitor",
        "entity_id" : "switch.sub_pc_monitor",
        "icon" : "mdi:monitor"
    },
    "모니터 조명" : {
        "name" : "Monitor Light",
        "entity_id" : "switch.monitor_light",
        "icon" : "mdi:ceiling-light"
    },
    "방송용 조명" : {
        "name" : "Broadcast Light",
        "entity_id" : "switch.broadcast_light",
        "icon" : "mdi:spotlight"
    },
    "내방 LED 조명" : {
        "name" : "Room LED Light",
        "entity_id" : "light.room_led_light",
        "icon" : "mdi:lightbulb-multiple"
    },
    "거실식물등" : {
        "name" : "Livingroom Gardening Light",
        "entity_id" : "switch.livingroom_gardening_light",
        "icon" : "mdi:pine-tree"
    },
    "거실식물등조도 Illuminance" : {
        "name" : "Livingroom Gardening Illuminance",
        "entity_id" : "sensor.livingroom_gardening_illuminance",
        "icon" : "mdi:brightness-5"
    },
}

with open(".storage/core.entity_registry", "r") as json_file:
    json_data = json.load(json_file)

entities = json_data['data']['entities']

idx = 0
count = 0
for entity in entities:
    print('-------------[ %s ]-------------' % entity['original_name'])
    print(entity['device_id'])
    print(entity['platform'])
    print('--------------')
    print(entity['name'])
    print(entity['entity_id'])
    print(entity['icon'])

    original_name = entity['original_name']
    if original_name in replacement.keys():
        data = replacement[original_name]
        print("@@@@@@@@@@@@@@ GOTTT")
        json_data['data']['entities'][idx]['name'] = data['name']
        json_data['data']['entities'][idx]['entity_id'] = data['entity_id']
        json_data['data']['entities'][idx]['icon'] = data['icon']
        count = count+1
    idx = idx + 1

with open(".storage/core.entity_registry", "w") as json_file:
    json.dump(json_data, json_file, indent = 4)

print("%d entities are changed" % count)
