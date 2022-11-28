#!/usr/bin/env python3
"""Provide Bluetooth functions."""
import logging
import shlex
import subprocess

import paho.mqtt.client as mqtt

from yamaha.const import MQTT_TOPIC_DEVICES
from zero_music.helpers import setup_arg_parser

logging.basicConfig()


class MQTTWatcher:
    """Watch for changes on MQTT"""

    def __init__(self, server, device_id, mac_addr, startup, shutdown, play) -> None:
        self.connected = None
        self.power = None
        self.device_id = device_id
        self.mac_addr = mac_addr
        self.startup = startup
        self.shutdown = shutdown
        self.play = play
        self.play_message = None
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(server)
        self.client.loop_forever()

    # pylint: disable=unused-argument
    def on_connect(self, client, userdata, flags, return_code):
        """MQTT on connect."""
        # self.client.subscribe(f"{MQTT_TOPIC_UPDATES}/#")
        self.client.subscribe(f"{MQTT_TOPIC_DEVICES}/{self.device_id}/#")

    # pylint: disable=unused-argument
    def on_message(self, client, userdata, msg):
        """MQTT on message."""
        payload = msg.payload.decode("utf-8")
        if msg.topic == f"{MQTT_TOPIC_DEVICES}/{self.device_id}/power":
            self.power = payload
            if self.power == "on":
                self.run_command(f"{self.startup} {self.mac_addr}")
            elif self.power == "standby":
                self.run_command(self.shutdown)
                self.connected = False
        elif msg.topic == f"{MQTT_TOPIC_DEVICES}/{self.device_id}/music/play":
            logging.debug((self.power, self.connected))
            if self.power == "standby":
                self.play_message = payload
                topic = f"{MQTT_TOPIC_DEVICES}/{self.device_id}/power/set"
                self.client.publish(topic, "on")
            elif not self.connected:
                self.play_message = payload
                self.run_command(f"{self.startup} {self.mac_addr}")
            elif self.power == "on" and self.connected:
                self.play_music(payload)
        elif msg.topic == f"{MQTT_TOPIC_DEVICES}/{self.device_id}/bluetooth":
            self.connected = bool(int(payload))
            logging.debug("Connected: %s", self.connected)
            if self.connected and self.play_message is not None:
                self.play_music(self.play_message)
                self.play_message = None
        elif msg.topic == f"{MQTT_TOPIC_DEVICES}/{self.device_id}/cmd":
            logging.debug(payload)
            cmd = payload[4:]
            if cmd in ["up", "down"]:
                topic = f"{MQTT_TOPIC_DEVICES}/{self.device_id}/volume/set"
                self.client.publish(topic, cmd)
            elif cmd in ["on", "standby", "toggle"]:
                topic = f"{MQTT_TOPIC_DEVICES}/{self.device_id}/power/set"
                self.client.publish(topic, cmd)
            elif cmd in ["play", "pause", "prev", "next"]:
                self.run_command(f"mpc {cmd}")

    def play_music(self, message):
        """Play music from message."""
        command = f'{self.play} "{message}"'
        self.run_command(command)

    def run_command(self, command):
        """Run a given shell command."""
        logging.debug("Running command: %s", command)
        if command is not None:
            cmd = shlex.split(command)
            subprocess.run(cmd, check=True)


def main():
    """Provide main routine."""
    parser = setup_arg_parser()
    parser.add_argument("--startup", type=str, help="Startup script")
    parser.add_argument("--shutdown", type=str, help="Shutdown script")
    parser.add_argument("--play", type=str, help="Play music script")
    args, _ = parser.parse_known_args()

    if getattr(args, "debug_mode"):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug Mode enabled")

    MQTTWatcher(
        getattr(args, "mqtt_host"),
        getattr(args, "device_id"),
        getattr(args, "mac_addr"),
        getattr(args, "startup"),
        getattr(args, "shutdown"),
        getattr(args, "play"),
    )


if __name__ == "__main__":
    main()
