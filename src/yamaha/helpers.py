#!/usr/bin/env python3
"""Provides helper functions."""
import logging
import time

import requests

from .const import MQTT_TOPIC_UPDATES


def request(url, *args, **kwargs):
    """Do the HTTP Request and return data"""
    method = kwargs.get("method", "GET")
    timeout = kwargs.pop("timeout", 10)  # default timeout
    response = requests.request(method, url, *args, timeout=timeout, **kwargs)
    try:
        result = response.json()
    except requests.exceptions.JSONDecodeError:
        result = response.text
    logging.debug(result)
    return result


def socket_worker(sock, client):
    """Socket Loop that fills message queue"""
    logging.debug("Starting Socket Thread.")
    while True:
        try:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        except OSError as err:
            logging.error(err)
        else:
            logging.debug("received message: %s from %s", data, addr)
            client.publish(MQTT_TOPIC_UPDATES, data)
        time.sleep(0.2)
