Jak zmienić IP do wysyłania odczytów kart
Otwórz plik rfid_application.py w edytorze tekstowym:

bash
Skopiuj kod
nano rfid_application.py
Znajdź sekcję konfiguracji serwera:

python
Skopiuj kod
API_HOST = 'http://10.10.0.72:8180'
API_ENDPOINT = '/card/'
Zmień API_HOST na nowe IP lub adres URL serwera, na który chcesz wysyłać dane:

python
Skopiuj kod
API_HOST = 'http://192.168.0.100:8180'  # Przykładowy nowy adres serwera
Jeśli endpoint serwera się zmienił, zaktualizuj API_ENDPOINT:

python
Skopiuj kod
API_ENDPOINT = '/new_endpoint/'  # Przykładowy nowy endpoint
Zapisz zmiany:

W edytorze nano użyj:
CTRL+O (zapisz plik),
CTRL+X (wyjdź z edytora).
Uruchom ponownie aplikację:

bash
Skopiuj kod
sudo python3 rfid_application.py
