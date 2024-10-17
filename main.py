from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv, find_dotenv, set_key
import time, os, psutil, datetime, json

class Monitor:
    def __init__(self):
        self.active = False

    def start_monitoring(self):
        self.active = True
        self.clear_screen()
        input("Övervakning startad! Tryck 'Enter' för att återgå till huvudmenyn ")
        self.clear_screen(); print("\nBekräftelse mottagen! Återgår till huvudmenyn..."); time.sleep(0.6); self.clear_screen()
        logformon.log("Övervakning startad.")

    def display_status(self):
        if not self.active:
            self.clear_screen(); print("Ingen övervakning är aktiv. Aktivera alternativ \"1\" från huvudmenyn först!")
            return

        cpu_usage = psutil.cpu_percent(interval=0)
        memory_info = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')

        self.clear_screen()
        print("Snapshot av resursanvändningen:")
        print(f"CPU Användning:\t\t{cpu_usage}%")
        print(f"Minnesanvändning:\t{memory_info.percent}% ({memory_info.used / (1024 ** 3):.2f} GB of {memory_info.total / (1024 ** 3):.2f} GB used)")
        print(f"Diskanvändning:\t\t{disk_usage.percent}% ({disk_usage.used / (1024 ** 3):.2f} GB out of {disk_usage.total / (1024 ** 3):.2f} GB used)\n")

        logformon.log(
            f"Användaren har hämtat ögonblicksbild av resursanvändningen:\n"
            f"CPU Användning: {cpu_usage}%\n"
            f"Minnessanvändning: {memory_info.percent}% ({memory_info.used / (1024 ** 3):.2f} GB of {memory_info.total / (1024 ** 3):.2f} GB used)\n"
            f"Diskanvändning: {disk_usage.percent}% ({disk_usage.used / (1024 ** 3):.2f} GB out of {disk_usage.total / (1024 ** 3):.2f} GB used)"
        )

        input("Tryck endast på 'Enter' för att fortsätta: ")
        self.clear_screen(); print("\nBekräftelse mottagen! Återgår till huvudmenyn..."); time.sleep(0.6); self.clear_screen()

    def check_status(self, alarm_manager):
        cpu_usage = psutil.cpu_percent(interval=0)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        alarm_manager.check_alarm(cpu_usage, memory_usage, disk_usage)

    def start_realtimemonitor(self, cpu_usage, mem_usage, disk_usage, bars=50):
        def create_bar(percent):
            return '█' * int(percent * bars) + '-' * (bars - int(percent * bars))
        
        print(
            f"\n\nCPU Usage:  |{create_bar(cpu_usage / 100.0)}| {cpu_usage:.2f}%\n\n"
            f"MEM Usage:  |{create_bar(mem_usage / 100.0)}| {mem_usage:.2f}%\n\n"
            f"DISK Usage: |{create_bar(disk_usage / 100.0)}| {disk_usage:.2f}%"
        )
        print(f"\nPress \"Ctrl+c\" to interrupt the performance monitor & go back to head menu: ", end="\n")

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

class AlarmManager:
    def __init__(self):
        self.alarms = {"CPU": [], "Memory": [], "Disk": []}
        self.load_alarms()

    def configure_alarm(self):
        while True:
            self.clear_screen()
            choice = input("\n1. CPU\n2. Memory\n3. Disk\n4. Tillbaka\nVälj: ")
            if choice in ['1', '2', '3']:
                self.set_alarm_level(["CPU", "Memory", "Disk"][int(choice) - 1])
            elif choice == '4':
                self.clear_screen(); print("\nÅtergår till huvudmenyn..."); time.sleep(0.4); break
            else:
                self.clear_screen(); print("Ogiltigt val.")

    def set_alarm_level(self, category):
        while True:
            level_input = input(f"\nStäll in {category} nivå mellan 1-100, eller '<' för att gå tillbaka: ")
            if level_input == "<":
                self.clear_screen(); break
            try:
                level = int(level_input)
                if 1 <= level <= 100:
                    self.alarms[category].append(level)
                    self.clear_screen(); print(f"{category} larm satt till {level}%"); self.save_alarms()
                    alarmlogger.log(f"{category} larm konfigurerat till {level}%"); break
                else:
                    self.clear_screen(); print("Felaktig nivå.")
            except ValueError:
                self.clear_screen(); print("Ogiltig inmatning.")

    def display_alarms(self):
        self.clear_screen(); print("Lagrade larm:\n")
        for category in ["CPU", "Memory", "Disk"]:
            for level in sorted(self.alarms[category]):
                print(f"{category} larm {level}%")
        input("\nTryck 'Enter' för att återgå."); self.clear_screen()
        alarmlogger.log("Visade lagrade larm")

    def remove_alarm(self):
        while True:
            self.clear_screen()
            alarm_list = [(f"{category} larm {level}%", category, level) for category in ["CPU", "Memory", "Disk"] for level in sorted(self.alarms[category])]
            if not alarm_list: 
                print("Inga larm att ta bort."); return
            print("Lagrade larm:\n" + "\n".join(f"{i+1}. {display}" for i, (display, _, _) in enumerate(alarm_list)))
            choice = input("\nVälj ett larm att ta bort, eller '0' för att återgå: ")
            if choice == '0': self.clear_screen(); break
            try:
                category, level = alarm_list[int(choice) - 1][1:3]
                self.alarms[category].remove(level); self.save_alarms()
                self.clear_screen(); print(f"{category} {level}% borttaget."); alarmlogger.log(f"Borttagit {category} {level}%"); break
            except (IndexError, ValueError): self.clear_screen(); print("Ogiltigt val.")

    def check_alarm(self, cpu, memory, disk):
        for category, usage in zip(["CPU", "Memory", "Disk"], [cpu, memory, disk]):
            for level in sorted(self.alarms[category], reverse=True):
                if usage > level:
                    message = f"*** VARNING, {category} ANVÄNDNING ÖVERSTIGER {level}% ***"
                    print(message); alarmlogger.log(f"Larm AKTIVERAD {message}"); send_email_alert(message); break

    def save_alarms(self):
        with open('alarms.json', 'w') as f: json.dump(self.alarms, f)

    def load_alarms(self):
        try:
            with open('alarms.json', 'r') as f: self.alarms = json.load(f)
        except FileNotFoundError:
            alarmlogger.log("Kunde inte ladda lagrade larm")

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

class Logger:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.filename = os.path.join('logs', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log"))

    def log(self, message):
        with open(self.filename, 'a') as f:
            f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} - {message}\n")

class textdec:
    BGWHITE = '\033[107m'
    BGCYAN = '\033[106m'
    BGPURPLE = '\033[105m'
    BGBLUE = '\033[104m'
    BGYELLOW = '\033[103m'
    BGGREEN = '\033[102m'
    BGRED = '\033[101m'
    BGGRAY = '\033[100m'
    BGBLACK = '\033[40m'
    
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    GRAY = '\033[90m'

    STRIKETHROUGH = '\033[28m'
    UNDERLINE = '\033[4m'
    ITALICS = '\033[3m'
    BOLD = '\033[1m'
    END = '\033[0m'


load_dotenv(".env", override=True)
alarm_manager = AlarmManager()
txd = textdec()
txdec = textdec()
logger = Logger()
logformon = Logger()
alarmlogger = Logger()
email_logger = Logger()
monitor = Monitor()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

logger.log("Applikationen startad")
os.system("cls" if os.name == "nt" else "clear")

def main_menu():
    options = [
        "Starta övervakning",
        "Lista aktiv övervakning",
        "Skapa larm",
        "Visa larm",
        "Starta övervakningsläge",
        "Ta bort larm",
        "Realtidsövervakning (Prestanda)",
        "Kontrollera .env filen för email utskick",
        "Avsluta programmet"
    ]
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\n{txdec.GREEN}*** Övervakningsapplikation ***{txdec.END}\n")
        for idx, option in enumerate(options, start=1):
            print(f"{txdec.BLUE}{idx}.{txdec.END} {option}")
        print(f"{txdec.RED}0.{txdec.END} Avsluta programmet")

        choice = input(f"\nVälj ett alternativ: {txdec.YELLOW}")
        print(txdec.END)

        if choice.isdigit() and (0 <= (choice := int(choice)) <= len(options)):
            logger.log(f"Användaren har gjort val {choice} från huvudmenyn")
            actions = [
                monitor.start_monitoring,
                monitor.display_status,
                lambda: (os.system("cls" if os.name == "nt" else "clear"), alarm_manager.configure_alarm()),
                alarm_manager.display_alarms,
                start_monitoring_mode,
                alarm_manager.remove_alarm,
                lambda: (os.system("cls" if os.name == "nt" else "clear"), start_realtime_monitoring()),
                lambda: (os.system("cls" if os.name == "nt" else "clear"), create_or_update_env_file(), time.sleep(2)),
                lambda: (os.system("cls" if os.name == "nt" else "clear"), print(f"\n{txdec.BOLD}{txdec.CYAN}Hej-då................................{txdec.END}\n"), logger.log("Applikationen avslutad"), exit())
            ]
            actions[choice - 1]()
        else:
            print(f"{txdec.RED}Ogiltig inmatning, vänligen ange ett nummer.{txdec.END}")
            logger.log("Användaren har matat in ogiltig inmatning.")

def start_realtime_monitoring():
    logger.log("Läge för realtidsövervakning startad")
    try:
        while True:
            monitor.start_realtimemonitor(
                psutil.cpu_percent(),
                psutil.virtual_memory().percent,
                psutil.disk_usage("/").percent,
                30
            )
            time.sleep(0.6)
            os.system("cls" if os.name == "nt" else "clear")
    except KeyboardInterrupt:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{txdec.YELLOW}Realtidsövervakning avslutad.{txdec.END}")
        logger.log("Läge för realtidsövervakning avslutad")

def start_monitoring_mode():
    if not monitor.active:  # Kontrollera om övervakning är aktiv
        os.system("cls" if os.name == "nt" else "clear")  # Rensa skärmen
        print(f"{txdec.YELLOW}Ingen övervakning är aktiv. Aktivera alternativ \"1\" från huvudmenyn först!{txdec.END}")
        return

    os.system("cls" if os.name == "nt" else "clear")  # Rensa skärmen
    print(f"{txdec.RED}Övervakningen är aktiv. Tryck på \"Ctrl+C\" för att återgå till huvudmenyn.\n{txdec.END}")
    logger.log("Övervakningsläge startat")  # Logga att övervakningsläget startat
    
    try:
        while True:
            monitor.check_status(alarm_manager)  # Kontrollera status på övervakningen
            time.sleep(1)  # Vänta 1 sekund mellan kontroller
    except KeyboardInterrupt:
        os.system("cls" if os.name == "nt" else "clear")  # Rensa skärmen vid avbrott
        print(f"{txdec.RED}Övervakningsläge avslutad\n{txdec.END}")
        logger.log("Övervakningsläge avslutad")  # Logga att övervakningsläget avslutats

def send_email_alert(message):
    try:
        email = Mail(
            from_email=SENDER_EMAIL,
            to_emails=RECIPIENT_EMAIL,
            subject="Larm aktiverat i övervakningsapplikationen",
            plain_text_content=message,
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(email)
        print(f"E-post skickat med statuskod {response.status_code}")
        email_logger.log(f"E-post skickat med statuskod {response.status_code}")
    except Exception as e:
        print(f"Misslyckades med att skicka e-post: {str(e)}")
        email_logger.log(f"Misslyckades med att skicka e-post: {str(e)}")

def create_or_update_env_file():
    dotenv_path = find_dotenv()

    if dotenv_path:
        load_dotenv(dotenv_path)
        print(f"{txd.GREEN}Hittade en befintlig .env-fil:{txd.END}")
        print(f"{txd.BLUE}SENDGRID_API_KEY{txd.END}={os.getenv('SENDGRID_API_KEY')}")
        print(f"{txd.BLUE}RECIPIENT_EMAIL{txd.END}={os.getenv('RECIPIENT_EMAIL')}")
        print(f"{txd.BLUE}SENDER_EMAIL{txd.END}={os.getenv('SENDER_EMAIL')}")

        if input(f"Stämmer informationen? ({txd.GREEN}ja{txd.END}/{txd.RED}nej{txd.END}): ").lower() == "ja":
            print(f"{txd.BOLD}{txd.YELLOW}.env-filen har lästs in.{txd.END}")
        else:
            sendgrid_api_key = input("Ange SendGrid API-nyckel: ")
            recipient_email = input("Ange mottagarens e-postadress: ")
            sender_email = input("Ange avsändarens e-postadress: ")

            for key, value in zip(["SENDGRID_API_KEY", "RECIPIENT_EMAIL", "SENDER_EMAIL"], 
                                  [sendgrid_api_key, recipient_email, sender_email]):
                set_key(dotenv_path, key, value)
            print(f"{txd.BOLD}{txd.YELLOW}.env-filen har uppdaterats. {txd.RED}STARTA OM PROGRAMMET!{txd.END}")
    else:
        print(f"{txd.BOLD}{txd.YELLOW}.env-fil hittades inte, skapa en ny{txd.END}")
        sendgrid_api_key = input("Ange SendGrid API-nyckel: ")
        recipient_email = input("Ange mottagarens e-postadress: ")
        sender_email = input("Ange avsändarens e-postadress: ")

        with open('.env', 'w') as f:
            f.writelines([f"SENDGRID_API_KEY={sendgrid_api_key}\n", 
                           f"RECIPIENT_EMAIL={recipient_email}\n", 
                           f"SENDER_EMAIL={sender_email}\n"])
        print(f"{txd.BOLD}{txd.YELLOW}.env-filen har skapats. {txd.RED}STARTA OM PROGRAMMET!{txd.END}")

if __name__ == "__main__":
    main_menu()
