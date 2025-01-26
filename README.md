Jak zmienić IP do wysyłania odczytów kart
Otwórz plik rfid_application.py w edytorze tekstowym:

nano rfid_application.py

Znajdź sekcję konfiguracji serwera:

Zmień API_HOST na nowe IP lub adres URL serwera, na który chcesz wysyłać dane:
```
API_HOST = 'http://10.10.0.72:8180'
API_ENDPOINT = '/card/'
API_HOST = 'http://192.168.0.100:8180'
```
Jeśli endpoint serwera się zmienił, zaktualizuj API_ENDPOINT:

API_ENDPOINT = '/new_endpoint/'  # Przykładowy nowy endpoint
Zapisz zmiany:

W edytorze nano użyj:

CTRL+O (zapisz plik),

CTRL+X (wyjdź z edytora).

Uruchom ponownie aplikację:

```sudo python3 rfid_application.py```

**Pinout**

RFID SDA             | 24 | GPIO 8	| SPI Chip Select

RFID SCK             | 23 |	GPIO 11 |	SPI Clock

RFID MOSI            | 19 |	GPIO 10	| SPI Master Out Slave In

RFID MISO	           | 21 | GPIO 9	| SPI Master In Slave Out

RFID RST	           | 22 |	GPIO 25	| Reset

RFID GND	           | 6  | GND     |	Masa

RFID 3.3V	           | 1  |	3.3V	  | Zasilanie

Dioda RGB R          | 12 |	GPIO 18	| Czerwony kolor diody RGB

Dioda RGB G	         | 16 |	GPIO 23 |	Zielony kolor diody RGB

Dioda RGB B	         | 18 |	GPIO 24	| Niebieski kolor diody RGB

Dioda RGB Anoda	     | 2	| 5V      | Wspólna anoda diody RGB

Czerwona dioda WiFi	 | 26 | GPIO 7	| Brak połączenia WiFi

Niebieska dioda WiFi | 13 | GPIO 27 | Aktywne połączenie WiFi

Buzzer               | 11 | GPIO 17 | Sygnał dźwiękowy

