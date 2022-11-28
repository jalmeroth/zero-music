#!/usr/bin/env python3
"""Provide socket functions."""

import logging
import socket


class SocketHandler:
    """Handler for Sockets."""

    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logging.debug("Trying to open socket.")
        self.socket.bind(("", 0))
        logging.debug(self)

    @property
    def lport(self):
        """Return local port."""
        _, port = self.socket.getsockname()
        return port

    @property
    def laddr(self):
        """Return local addr."""
        addr, _ = self.socket.getsockname()
        return addr

    def __repr__(self) -> str:
        return f"Socket bound to {self.laddr} on port {self.lport}"

    def __del__(self):
        """Object deconstruction."""
        logging.debug("Closing socket.")
        self.socket.close()
