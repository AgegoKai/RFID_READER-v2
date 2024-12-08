Jak zmienić IP do wysyłania odczytów kart
Otwórz plik rfid_application.py w edytorze tekstowym:

nano rfid_application.py

Znajdź sekcję konfiguracji serwera:

Zmień API_HOST na nowe IP lub adres URL serwera, na który chcesz wysyłać dane:
```
API_HOST = 'http://10.10.0.72:8180'
API_ENDPOINT = '/card/'
Zmień API_HOST na nowe IP lub adres URL serwera, na który chcesz wysyłać dane:
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
