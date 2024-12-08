# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import requests
import sqlite3
import threading

# Server configuration
API_HOST = 'http://10.10.0.72:8180'
API_ENDPOINT = '/card/'

# Database configuration
DATABASE_FILE = 'rfid_data.db'

# GPIO setup
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
GPIO.setwarnings(False)

# WiFi LEDs
RED_WIFI_PIN = 26  # Physical Pin 26 (Red LED: No WiFi)
BLUE_WIFI_PIN = 13  # Physical Pin 13 (Blue LED: Connected to WiFi)
GPIO.setup(RED_WIFI_PIN, GPIO.OUT)
GPIO.setup(BLUE_WIFI_PIN, GPIO.OUT)

# Buzzer and RGB LED
BUZZER_PIN = 11  # Physical Pin 11
RED_PIN = 12  # Physical Pin 12
GREEN_PIN = 16  # Physical Pin 16
BLUE_PIN = 18  # Physical Pin 18
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# RFID reader
reader = SimpleMFRC522()

# Functions for WiFi LED
def wifi_status():
    """Check if WiFi is connected."""
    try:
        response = os.system("ping -c 1 8.8.8.8 > /dev/null 2>&1")
        return response == 0
    except Exception:
        return False

def update_wifi_led():
    """Update LEDs based on WiFi status."""
    if wifi_status():
        GPIO.output(RED_WIFI_PIN, GPIO.LOW)  # Turn off red LED
        GPIO.output(BLUE_WIFI_PIN, GPIO.HIGH)  # Turn on blue LED
    else:
        GPIO.output(RED_WIFI_PIN, GPIO.HIGH)  # Turn on red LED
        GPIO.output(BLUE_WIFI_PIN, GPIO.LOW)  # Turn off blue LED

# Database setup and functions
def create_database():
    """Create the database and table if they don't exist."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rfid_reads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            sent INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def save_rfid_to_db(card_id, timestamp):
    """Save RFID data to the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO rfid_reads (card_id, timestamp, sent) VALUES (?, ?, 0)', (card_id, timestamp))
    conn.commit()
    conn.close()

def mark_rfid_as_sent(card_id, timestamp):
    """Mark an RFID record as sent in the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE rfid_reads SET sent = 1 WHERE card_id = ? AND timestamp = ?', (card_id, timestamp))
    conn.commit()
    conn.close()

# Retry unsent data
def retry_unsent_data():
    while True:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT card_id, timestamp FROM rfid_reads WHERE sent = 0 LIMIT 1')
        unsent_data = cursor.fetchone()
        conn.close()

        if unsent_data:
            card_id, timestamp = unsent_data
            send_rfid_data(card_id, timestamp)
        
        time.sleep(60)

# Send RFID data to server
def send_rfid_data(card_id, timestamp):
    """Send RFID data to the server."""
    try:
        url = f"{API_HOST}{API_ENDPOINT}{card_id}"
        data = {"datetime": timestamp}
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 200:
            print(f"Data successfully sent for card number: {card_id}")
            mark_rfid_as_sent(card_id, timestamp)
        else:
            print(f"Failed to send data for card number: {card_id}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data for card number {card_id}: {e}")

# Main function
def main():
    create_database()  # Ensure database and table exist

    retry_thread = threading.Thread(target=retry_unsent_data, daemon=True)
    retry_thread.start()

    try:
        while True:
            update_wifi_led()  # Update WiFi LED status

            print("Place your RFID card near the reader")
            id, text = reader.read()
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")  # ISO 8601 format

            # Beep when the card is successfully read
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.2)  # Short beep
            GPIO.output(BUZZER_PIN, GPIO.LOW)

            save_rfid_to_db(id, timestamp)  # Save to database
            threading.Thread(target=send_rfid_data, args=(id, timestamp), daemon=True).start()  # Send to server

            time.sleep(1)

    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        GPIO.cleanup()  # Clean up all GPIO pins

if __name__ == '__main__':
    main()
