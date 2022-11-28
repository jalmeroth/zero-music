#!/usr/bin/env python3
"""Provide RFID Functions."""
import logging
import time

import paho.mqtt.client as mqtt
from pirc522 import RFID

from yamaha.const import MQTT_TOPIC_DEVICES
from zero_music.helpers import setup_arg_parser


def main():
    """Provide main routine."""
    if getattr(args, "debug_mode"):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug Mode enabled")

    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

    client.connect(getattr(args, "mqtt_host"))
    client.loop_start()

    print("Ready. Waiting for tag.")
    last_text = None
    last_time = None
    tag_text = None

    while True:
        reader.wait_for_tag()
        (error, _) = reader.request()
        if not error:
            logging.debug("Tag detected")
            (error, uid) = reader.anticoll()
            if not error:
                logging.debug("UID: %s", str(uid))
                if not reader.select_tag(uid):
                    if (
                        last_time is not None and (time.time() - last_time) >= 60
                    ):  # a minute has passed since we has last seen this tag
                        last_text = None
                    tag_text = []
                    for blk in range(8, 11):
                        if not reader.card_auth(reader.auth_a, blk, key, uid):
                            err, data = reader.read(blk)
                            if not err:
                                tag_text += data
                            else:
                                logging.error("Error reading block %d", blk)
                    tag_text = "".join([chr(x) for x in tag_text]).strip()
                    if len(tag_text) > 0:
                        print(tag_text)
                        if tag_text.startswith("cmd:"):
                            client.publish(MQTT_TOPIC_CMD, tag_text)
                        elif last_text != tag_text:
                            client.publish(MQTT_TOPIC_PLAY, tag_text)
                            last_text = tag_text
                            last_time = time.time()
                        else:
                            logging.debug("Ignoring: %s", tag_text)
                    reader.stop_crypto()

        if tag_text in ["cmd:up", "cmd:down"]:
            time.sleep(0.1)  # faster volume up/down
        else:
            time.sleep(1)
        tag_text = None


if __name__ == "__main__":
    parser = setup_arg_parser()
    args, _ = parser.parse_known_args()
    DEVICE_ID = getattr(args, "device_id")
    MQTT_TOPIC_PLAY = f"{MQTT_TOPIC_DEVICES}/{DEVICE_ID}/music/play"
    MQTT_TOPIC_CMD = f"{MQTT_TOPIC_DEVICES}/{DEVICE_ID}/cmd"
    client = mqtt.Client()
    reader = RFID()
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")
    finally:
        client.loop_stop()
        reader.cleanup()
