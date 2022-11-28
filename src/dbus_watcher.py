#!/usr/bin/env python3
"""Provide dbus functions."""
import logging
import sys

import dbus
import paho.mqtt.client as mqtt
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from yamaha.const import MQTT_TOPIC_DEVICES
from zero_music.helpers import setup_arg_parser

logging.basicConfig()


def publish_state(state):
    """MQTT: Publish state."""
    logging.debug(state)
    client.publish(MQTT_TOPIC_BLUETOOTH, state, retain=True)


def properties_changed(interface, changed, invalidated, path):
    """callback when properties changed."""
    if interface == "org.bluez.Device1":
        logging.debug((interface, changed, invalidated, path))
        if "Connected" in changed:
            state = "1" if changed["Connected"] else "0"
            publish_state(state)


def main():
    """Provide main routine."""
    if getattr(args, "debug_mode"):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug Mode enabled")

    client.connect(getattr(args, "mqtt_host"))
    client.loop_start()

    mac_addr = getattr(args, "mac_addr").replace(":", "_")
    device = bus.get_object("org.bluez", f"/org/bluez/hci0/dev_{mac_addr}")
    props = dbus.Interface(device, "org.freedesktop.DBus.Properties")
    publish_state(props.Get("org.bluez.Device1", "Connected"))

    bus.add_signal_receiver(
        properties_changed,
        bus_name="org.bluez",
        dbus_interface="org.freedesktop.DBus.Properties",
        signal_name="PropertiesChanged",
        path_keyword="path",
    )

    loop.run()


if __name__ == "__main__":
    parser = setup_arg_parser()
    args, _ = parser.parse_known_args()
    DEVICE_ID = getattr(args, "device_id")
    MQTT_TOPIC_BLUETOOTH = f"{MQTT_TOPIC_DEVICES}/{DEVICE_ID}/bluetooth"
    client = mqtt.Client()
    client.will_set(MQTT_TOPIC_BLUETOOTH, "0", qos=0, retain=True)
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    loop = GLib.MainLoop()
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")
        client.loop_stop()
        loop.quit()
        sys.exit(0)
