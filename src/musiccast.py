#!/usr/bin/env python3
"""Connect to Yamaha MusicCast device and issue commands."""
import logging

import yamaha
from zero_music.helpers import setup_arg_parser

logging.basicConfig()


def main():
    """Provide main routine."""
    parser = setup_arg_parser()
    parser.add_argument("host", type=str, help="Yamaha MusicCast Host")
    args, _ = parser.parse_known_args()

    if getattr(args, "debug_mode"):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug Mode enabled")

    # pylint: disable=no-member
    device = yamaha.MusicCastDevice(getattr(args, "host"))
    device.client.connect(getattr(args, "mqtt_host"))
    device.client.loop_forever()


if __name__ == "__main__":
    main()
