#!/usr/bin/env python3
"""Provide constant values."""
API_ENDPOINTS = {
    "getDeviceInfo": "http://{}/YamahaExtendedControl/v1/system/getDeviceInfo",
    "getStatus": "http://{}/YamahaExtendedControl/v1/main/getStatus",
    "setPower": "http://{}/YamahaExtendedControl/v1/main/setPower",
    "setVolume": "http://{}/YamahaExtendedControl/v1/main/setVolume",
}
MQTT_TOPIC_UPDATES = "mc_messages"
MQTT_TOPIC_DEVICES = "devices"
