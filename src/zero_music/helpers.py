#!/usr/bin/env python3
"""Provide helper functions."""
import argparse
from os import getenv


def setup_arg_parser():
    """Setup argparser."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", dest="debug_mode", action="store_true", help="Enable Debugging"
    )
    parser.add_argument(
        "--mqtt-host",
        default=getenv("MQTT_HOST", "localhost"),
        dest="mqtt_host",
        type=str,
        help="MQTT Host",
    )
    parser.add_argument(
        "--device-id",
        default=getenv("DEVICE_ID"),
        dest="device_id",
        type=str,
        help="Device ID",
    )
    parser.add_argument(
        "--mac-addr",
        default=getenv("MAC_ADDR"),
        dest="mac_addr",
        type=str,
        help="Device MAC Address",
    )
    return parser


def main():
    """Provide main routine."""
    parser = setup_arg_parser()
    args, _ = parser.parse_known_args()
    print(getattr(args, "mqtt_host"))
    print(getattr(args, "device_id"))
    print(getattr(args, "mac_addr"))


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("Quitting.")
