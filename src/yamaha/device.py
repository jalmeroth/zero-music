#!/usr/bin/env python3
"""Representation of a MusicCast device."""

import json
import logging
import threading

import paho.mqtt.client as mqtt

from .const import API_ENDPOINTS, MAX_VOLUME, MQTT_TOPIC_DEVICES, MQTT_TOPIC_UPDATES
from .helpers import request, socket_worker
from .socket import SocketHandler


class MusicCastDevice:
    """MusicCast device representation."""

    def __init__(self, host) -> None:
        self._host = None
        self._port = None
        self._device_id = None
        self._power = None
        self._volume = None

        self.host = host
        self.sock = SocketHandler()
        self.port = self.sock.lport

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self._initialize()

    def _initialize(self):
        """Init MusicCast device."""
        self.thread = threading.Thread(
            name="SocketThread",
            target=socket_worker,
            args=[self.sock.socket, self.client],
        )
        self.thread.setDaemon(True)
        self.thread.start()
        # device info => device_id
        device_info = self.get_device_info()
        self._device_id = device_info.get("device_id")
        # refresh
        self.refresh()

    def refresh(self):
        """Refresh MusicCast device information."""
        logging.debug("Refreshing")
        status = self.get_status()
        self.power = status.get("power")
        self.volume = status.get("volume")
        # schedule next refresh
        timer = threading.Timer(300, self.refresh)  # every five minutes
        timer.setDaemon(True)
        timer.start()

    def get_device_info(self):
        """Get Device information."""
        url = API_ENDPOINTS["getDeviceInfo"].format(self.host)
        return request(url, headers=self.headers())

    def get_status(self):
        """Get MusicCast status."""
        url = API_ENDPOINTS["getStatus"].format(self.host)
        return request(url, headers=self.headers())

    def headers(self):
        """Add HTTP Headers."""
        if self.port:
            headers = {
                "X-AppName": "MusicCast/0.1(python)",
                "X-AppPort": str(self.port),
            }
        else:
            headers = {}
        return headers

    def set_power(self, state):
        """Set power state."""
        url = API_ENDPOINTS["setPower"].format(self.host)
        params = {"power": state}
        return request(url, headers=self.headers(), params=params)

    def set_volume(self, volume):
        """Set volume."""
        if self.volume >= MAX_VOLUME and volume == "up":  # protect some ears
            logging.debug("Volume: ignore up command")
            return
        url = API_ENDPOINTS["setVolume"].format(self.host)
        params = {"volume": volume}
        return request(url, headers=self.headers(), params=params)

    # The callback for when the client receives a CONNACK response from the server.
    # pylint: disable=unused-argument
    def on_connect(self, client, userdata, flags, return_code):
        """MQTT on connect."""
        # logging.debug((client, userdata, flags, return_code))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(f"{MQTT_TOPIC_UPDATES}/#")
        client.subscribe(f"{MQTT_TOPIC_DEVICES}/{self.device_id}/+/set")

    # The callback for when a PUBLISH message is received from the server.
    # pylint: disable=unused-argument
    def on_message(self, client, userdata, msg):
        """MQTT on message."""
        # logging.debug((client, userdata, msg))
        self.handle_message(msg)

    def handle_message(self, msg):
        """MQTT handle message."""
        try:
            message = json.loads(msg.payload)
        except json.JSONDecodeError:
            message = msg.payload.decode("utf-8")

        if msg.topic.startswith(MQTT_TOPIC_DEVICES):
            self.handle_command(msg.topic, message)
        elif msg.topic.startswith(MQTT_TOPIC_UPDATES):
            self.handle_update(message)
        else:
            logging.debug("meow")

    def handle_command(self, topic, message):
        """MQTT handle command message."""
        if topic.startswith(f"{MQTT_TOPIC_DEVICES}/{self.device_id}"):
            if topic == f"{MQTT_TOPIC_DEVICES}/{self.device_id}/power/set":
                self.set_power(message)
            elif topic == f"{MQTT_TOPIC_DEVICES}/{self.device_id}/volume/set":
                self.set_volume(message)
            else:
                logging.warning("Ignoring: %s => %s", topic, message)

    def handle_update(self, message):
        """MQTT handle update message."""
        if message.get("device_id") == self.device_id:
            if "main" in message and message["main"].get("power"):
                self.power = message["main"].get("power")
            elif "main" in message and message["main"].get("volume"):
                self.volume = message["main"].get("volume")
            else:
                # logging.warning("Ignoring: %s", message)
                pass

    @property
    def host(self):
        """Returns host."""
        return self._host

    @host.setter
    def host(self, host):
        """Sets host"""
        self._host = host

    @property
    def port(self):
        """Returns port."""
        return self._port

    @port.setter
    def port(self, port):
        """Sets port"""
        self._port = port

    @property
    def device_id(self):
        """Returns device_id."""
        return self._device_id

    @property
    def power(self):
        """Returns power."""
        return self._power

    @power.setter
    def power(self, power):
        """Sets power"""
        logging.debug("Power: %s", power)
        self.client.publish(
            f"{MQTT_TOPIC_DEVICES}/{self.device_id}/power", power, retain=True
        )
        self._power = power

    @property
    def volume(self):
        """Returns volume."""
        return self._volume

    @volume.setter
    def volume(self, volume):
        """Sets volume"""
        logging.debug("Volume: %s", volume)
        self.client.publish(
            f"{MQTT_TOPIC_DEVICES}/{self.device_id}/volume", volume, retain=True
        )
        self._volume = volume

    def __repr__(self) -> str:
        return str(self.__dict__)
