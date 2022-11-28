#!/usr/bin/env python3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
try:
    text = input("Enter tag data:")
    print("Hold tag to module")
    reader.write(text)
    print("Done...")
finally:
    GPIO.cleanup()
