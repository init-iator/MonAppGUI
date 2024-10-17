from monitor import Monitor
from alarm import AlarmManager
from logger import Logger
from textdecor import textdec
from email_alert import create_or_update_env_file
import time, os, psutil

# Initiera övervakning, larmhantering och loggning
monitor = Monitor()
alarm_manager = AlarmManager()
logger = Logger()
txdec = textdec()

# Logga att applikationen startas och rensa terminalfönstret
logger.log("Applikationen startad")
os.system("cls" if os.name == "nt" else "clear")

# Huvudmenyn för applikationen
def main_menu():
    while True:
        # Visa menyalternativ
        print(f"\n{txdec.GREEN}*** Övervakningsapplikation ***{txdec.END}\n")
        print(f"{txdec.BLUE}1.{txdec.END} Starta övervakning")
        print(f"{txdec.BLUE}2.{txdec.END} Lista aktiv övervakning")
        print(f"{txdec.BLUE}3.{txdec.END} Skapa larm")
        print(f"{txdec.BLUE}4.{txdec.END} Visa larm")
        print(f"{txdec.BLUE}5.{txdec.END} Starta övervakningsläge")
        print(f"{txdec.BLUE}6.{txdec.END} Ta bort larm")
        print(f"{txdec.BLUE}7.{txdec.END} Realtidsövervakning (Prestanda)")
        print(f"{txdec.BLUE}8.{txdec.END} Kontrollera .env filen för email utskick")
        print(f"{txdec.RED}0.{txdec.END} Avsluta programmet")

        # Ta emot användarens val
        choice = input(f"\nVälj ett alternativ: {txdec.YELLOW}")
        print(txdec.END)

        if choice.isdigit():  # Kontrollera om valet är ett nummer
            choice = int(choice)
            if choice >= 0 and choice <= 8:  # Kontrollera om valet är inom giltigt intervall
                logger.log(f"Användaren har gjort val {choice} från huvudmenun")  # Logga valet

                # Hantera olika val
                if choice == 1:
                    monitor.start_monitoring()  # Starta övervakning
                elif choice == 2:
                    monitor.display_status()  # Visa status på aktiv övervakning
                elif choice == 3:
                    os.system("cls" if os.name == "nt" else "clear")  # Rensa terminalfönstret
                    alarm_manager.configure_alarm()  # Konfigurera ett nytt larm
                elif choice == 4:
                    alarm_manager.display_alarms()  # Visa befintliga larm
                elif choice == 5:
                    start_monitoring_mode()  # Starta övervakningsläge
                elif choice == 6:
                    alarm_manager.remove_alarm()  # Ta bort ett larm
                elif choice == 7:
                    os.system("cls" if os.name == "nt" else "clear")  # Rensa terminalfönstret
                    logger.log("Läge för realtidsövervakning startad")
                    try:
                        while True:
                            # Kör realtidsövervakning för CPU, minne och disk
                            monitor.start_realtimemonitor(
                                psutil.cpu_percent(),
                                psutil.virtual_memory().percent,
                                psutil.disk_usage("/").percent,
                                30
                                )
                            time.sleep(0.6)  # Vänta 0.6 sekunder mellan uppdateringar
                            os.system("cls" if os.name == "nt" else "clear")  # Rensa skärmen
                    except KeyboardInterrupt:
                        os.system("cls" if os.name == "nt" else "clear")  # Avsluta övervakningen vid Ctrl+C
                        print(f"{txdec.YELLOW}Realtidsövervakning avslutad.{txdec.END}")
                        logger.log("Läge för realtidsövervakning avslutad")
                        pass
                elif choice == 8:
                    os.system("cls" if os.name == "nt" else "clear")  # Rensa skärmen
                    create_or_update_env_file()
                    time.sleep(2)
                    logger.log("Användaren har inspekterat kongifuration för e-post utskick")
                    os.system("cls" if os.name == "nt" else "clear")  # Rensa skärmen
                elif choice == 0:
                    os.system("cls" if os.name == "nt" else "clear")  # Rensa skärmen
                    print(f"\n{txdec.BOLD}{txdec.CYAN}Hej-då................................{txdec.END}\n")
                    logger.log("Applikationen avslutad")  # Logga att applikationen avslutats                                       
                    break  # Avsluta programmet
            else:
                os.system("cls" if os.name == "nt" else "clear")  # Rensa skärmen vid felaktigt val
                print(f"{txdec.RED}Felaktigt val, försök igen.{txdec.END}")
                logger.log("Användaren har gjort felaktig val")  # Logga felaktigt val
        else:
            os.system("cls" if os.name == "nt" else "clear")  # Rensa skärmen vid ogiltig inmatning
            print(f"{txdec.RED}Ogiltig inmatning, vänligen ange ett nummer.{txdec.END}")
            logger.log("Användaren har matat in ogiltig inmatning.")  # Logga ogiltig inmatning

# Starta övervakningsläge om en övervakning är aktiv
def start_monitoring_mode():
    mon = monitor
    if not mon.active:  # Kontrollera om övervakning är aktiv
        os.system("cls" if os.name == "nt" else "clear")  # Rensa skärmen
        print(f"{txdec.YELLOW}Ingen övervakning är aktiv. Aktivera alternativ \"1\" från huvudmenyn först!{txdec.END}")
    else:
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
            pass

# Kör programmet om det körs direkt
if __name__ == "__main__":
    main_menu()
