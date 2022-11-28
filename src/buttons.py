#!/usr/bin/env python3
"""Provide Button functions"""
import logging

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library

from yamaha.const import MQTT_TOPIC_DEVICES
from zero_music.helpers import setup_arg_parser

logging.basicConfig(level=logging.INFO)


def button_callback(channel):
    """Callback function."""
    logging.info("Button was pushed! %d", channel)
    topic = f"{MQTT_TOPIC_DEVICES}/{DEVICE_ID}/cmd"
    if channel == 11:  # green
        client.publish(topic, "cmd:play")
    elif channel == 13:  # white
        client.publish(topic, "cmd:prev")
    elif channel == 15:  # blue
        client.publish(topic, "cmd:next")
    elif channel == 16:  # red
        client.publish(topic, "cmd:pause")


def main():
    """Provide main routine."""
    if getattr(args, "debug_mode"):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug Mode enabled")

    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

    pins = [11, 13, 15, 16]
    for pin in pins:
        GPIO.setup(
            pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN
        )  # Set pin to be an input pin and set initial value to be pulled low (off)

        GPIO.add_event_detect(
            pin, GPIO.RISING, callback=button_callback, bouncetime=200
        )  # Setup event on pin rising edge

    # MQTT let stay connected
    client.loop_forever()


if __name__ == "__main__":
    parser = setup_arg_parser()
    args, _ = parser.parse_known_args()
    DEVICE_ID = getattr(args, "device_id")
    client = mqtt.Client()
    client.connect(getattr(args, "mqtt_host"))
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")
    finally:
        GPIO.cleanup()  # Clean up
