import json, os, time  # Importerar nödvändiga bibliotek för JSON-hantering, systemkommandon och tidskontroll
from logger import Logger  # Importerar Logger-klassen för loggning av händelser
from email_alert import send_email_alert  # Importerar funktionen för att skicka e-postalarmer

alarmlogger = Logger()  # Skapar en instans av Logger

class AlarmManager:
    def __init__(self):
        # Initierar larm som en dictionary för CPU, minne och disk
        self.alarms = {"CPU": [], "Memory": [], "Disk": []}
        self.load_alarms()  # Laddar befintliga larm från fil

    def configure_alarm(self):
        while True:
            # Visar alternativ för larmkonfiguration
            print("\n1. CPU användning")
            print("2. Minnesanvändning")
            print("3. Diskanvändning")
            print("4. Tillbaka till huvudmeny")

            choice = input("Välj larmtyp (1-3) eller 4 för att återgå: ")  # Tar emot användarens val

            # Loopar igenom val för att bestämma vilken typ av larm som konfigureras
            for i in choice:
                if choice == "1":
                    i = "cpu"  # Sätter i till "cpu" för CPU-larm
                elif choice == "2":
                    i = "minnes"  # Sätter i till "minnes" för minneslarm
                elif choice == "3":
                    i = "disk"  # Sätter i till "disk" för disklarm

            if choice == '4':  # Om användaren vill återgå
                os.system("cls" if os.name == "nt" else "clear")  # Rensar skärmen
                print("\nÅtergår till huvudmenyn...")  # Bekräftar återgång
                time.sleep(0.4)  # Väntar en kort stund
                os.system("cls" if os.name == "nt" else "clear")  # Rensar skärmen igen
                break
            
            if choice in ['1', '2', '3']:  # Om valet är giltigt
                while True:
                    # Ber användaren att ställa in larmnivå
                    level = input(f"\nStäll in nivå för {i} alarm mellan 0-100:\nEller '<' för att gå tillbaka\nVäntar på input: ")
                    
                    if level == "<":  # Om användaren vill gå tillbaka
                        os.system("cls" if os.name == "nt" else "clear")
                        print("Går tillbaka till val av larmtyp...")  # Bekräftar återgång
                        time.sleep(0.4)  # Väntar en kort stund
                        break

                    try:
                        level = int(level)  # Konverterar inmatningen till ett heltal
                        
                        if 0 < level <= 100:  # Kontrollerar att nivån är inom det giltiga intervallet
                            if choice == '1':
                                self.alarms["CPU"].append(level)  # Lägger till larmnivå för CPU
                            elif choice == '2':
                                self.alarms["Memory"].append(level)  # Lägger till larmnivå för minne
                            elif choice == '3':
                                self.alarms["Disk"].append(level)  # Lägger till larmnivå för disk
                            
                            os.system("cls" if os.name == "nt" else "clear")  # Rensar skärmen
                            print(f"{i.capitalize()} larm satt till {level}%")  # Bekräftar larminställningen
                            self.save_alarms()  # Sparar aktuella larm
                            alarmlogger.log(f"{i.capitalize()} larm är konfigurerat och satt till {level} %")
                            break
                        
                        else:
                            os.system("cls" if os.name == "nt" else "clear")
                            print("Felaktig nivå. Ange en siffra mellan 1-100.")  # Felmeddelande

                    except ValueError:
                        os.system("cls" if os.name == "nt" else "clear")
                        print("Felaktig input. Ange en siffra mellan 1-100.")  # Felmeddelande för ogiltig inmatning

            else:
                os.system("cls" if os.name == "nt" else "clear")
                print("Felaktigt val. Välj ett alternativ mellan 1 och 4.")  # Felmeddelande för ogiltigt val

    def display_alarms(self):
        os.system("cls" if os.name == "nt" else "clear")  # Rensar skärmen
        
        # Visar en lista över lagrade larm
        print("Lista: lagrade larm.\n")  
        
        for category in ["CPU", "Memory", "Disk"]:  # Loopar igenom larmkategorier
            for level in sorted(self.alarms[category]):  # Sorterar och visar larmnivåer
                print(f"{category} larm {level}%")
        
        input("\nTryck 'Enter' för att gå tillbaka till huvudmenyn.")  # Väntar på användarinmatning
        os.system("cls" if os.name == "nt" else "clear")  # Rensar skärmen
        alarmlogger.log("Lista med lagrade larm har visats i skärmen")

    def remove_alarm(self):
        os.system("cls" if os.name == "nt" else "clear")  # Rensar skärmen
        
        while True:
            try:
                alarm_list = []  # Lista för att lagra larm
                index = 1  # Räknare för larm
                
                # Visar en lista över lagrade larm
                print("Lista: Lagrade larm.\n")  
                
                for category in ["CPU", "Memory", "Disk"]:  # Loopar igenom larmkategorier
                    for level in sorted(self.alarms[category]):  # Sorterar och visar larmnivåer
                        alarm_list.append((category, level))  # Lägger till larm i listan
                        print(f"{index}. {category} larm {level}%")  # Visar larm med index
                        index += 1
                
                if not alarm_list:  # Om inga larm finns
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Inga larm att ta bort.")  # Meddelande om tom larmlista
                    return

                # Tar emot användarens val för vilket larm som ska tas bort
                choice = int(input("\nVälj ett larm att ta bort (ange siffra)\neller välj '0' för att återgå till huvudmenyn: "))  
                
                if 1 <= choice <= len(alarm_list):  # Kontrollerar giltigt val
                    category, level = alarm_list[choice - 1]  # Hämta larmkategori och nivå
                    self.alarms[category].remove(level)  # Tar bort larm från kategorin
                    
                    os.system("cls" if os.name == "nt" else "clear")  # Rensar skärmen
                    print(f"\nLarm {category} {level}% borttaget. Återgår till huvudmenyn...")  # Bekräftar borttagning
                    self.save_alarms()  # Sparar ändrade larm
                    alarmlogger.log(f"Larm för {category} {level} % är borttaget")
                    break
                
                elif choice == 0:  # Om användaren vill återgå
                    os.system("cls" if os.name == "nt" else "clear")  # Rensar skärmen
                    break
                
                else:
                    os.system("cls" if os.name == "nt" else "clear")  # Rensar skärmen
                    print("\nOgiltigt val, försök igen.")  # Felmeddelande

            except ValueError:  # Hantering av ogiltig inmatning
                os.system("cls" if os.name == "nt" else "clear")  # Rensar skärmen
                print("\nFelaktig input, försök igen.")  # Felmeddelande

    def check_alarm(self, cpu, memory, disk):
        triggered = []  # Lista för att lagra utlösta larm
        
        # Loopar igenom CPU-larm och kontrollerar om användningen överskrider nivån
        for level in sorted(self.alarms["CPU"], reverse=True):  
            if cpu > level:  # Kontrollerar om CPU-användningen överskrider nivån
                triggered.append(f"*** VARNING, CPU ANVÄNDNING ÖVERSTIGER\t\t\t{level}% ***")  # Lägger till varning
                break  # Avbryter loopen efter att första varningen har lagts till
        
        # Loopar igenom minneslarm och kontrollerar om användningen överskrider nivån
        for level in sorted(self.alarms["Memory"], reverse=True):  
            if memory > level:  # Kontrollerar om minnesanvändningen överskrider nivån
                triggered.append(f"*** VARNING, MINNESANVÄNDNING ÖVERSTIGER\t\t{level}% ***")  # Lägger till varning
                break  # Avbryter loopen efter att första varningen har lagts till
        
        # Loopar igenom disklarm och kontrollerar om användningen överskrider nivån
        for level in sorted(self.alarms["Disk"], reverse=True):  
            if disk > level:  # Kontrollerar om diskanvändningen överskrider nivån
                triggered.append(f"*** VARNING, DISKANVÄNDNING ÖVERSTIGER\t\t\t{level}% ***")  # Lägger till varning
                break  # Avbryter loopen efter att första varningen har lagts till
        
        for message in triggered:  # Loopar igenom utlösta larm
            print(message)  # Visar varning på skärmen
            alarmlogger.log(f"Larm AKTIVERAD {message}")  # Loggar varningen
            send_email_alert(message)  # Skickar e-postvarning
            #alarmlogger.log(message)  # Loggar varningen med Logger

    def save_alarms(self):
        # Öppnar (eller skapar) en fil för att spara larm
        with open('alarms.json', 'w') as f:  
            json.dump(self.alarms, f)  # Sparar larmen i JSON-format

    def load_alarms(self):
        try:
            # Försöker öppna filen med larm
            with open('alarms.json', 'r') as f:  
                self.alarms = json.load(f)  # Laddar larm från fil
        except FileNotFoundError:  # Hantering av fel om filen inte finns
            alarmlogger.log("Kunde inte ladda filen med lagrade larm")
            pass  # Inga åtgärder vid fil inte hittades
