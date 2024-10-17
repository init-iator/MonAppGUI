import os
import datetime


class Logger:
    def __init__(self):
        # Skapa logs-mappen om den inte finns
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Filnamn med full sökväg till logs-mappen
        self.filename = os.path.join(
            'logs', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log"))

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Öppna loggfilen i append-läge och skriv meddelandet
        with open(self.filename, 'a') as f:
            f.write(f"{timestamp} - {message}\n")
