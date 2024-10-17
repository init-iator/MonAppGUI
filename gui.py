# import tkinter as tk
# from tkinter import messagebox, simpledialog
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# from dotenv import load_dotenv, find_dotenv, set_key
# import psutil
# import time
# import os
# import datetime
# import json


# class Monitor:
#     def __init__(self):
#         self.active = False

#     def start_monitoring(self):
#         self.active = True
#         logformon.log("Övervakning startad.")

#     def display_status(self):
#         if not self.active:
#             return "Ingen övervakning är aktiv. Aktivera alternativ \"1\" från huvudmenyn först!"

#         cpu_usage = psutil.cpu_percent(interval=0)
#         memory_info = psutil.virtual_memory()
#         disk_usage = psutil.disk_usage('/')

#         status = (
#             f"CPU Användning:\t\t{cpu_usage}%\n"
#             f"Minnesanvändning:\t{memory_info.percent}% ({memory_info.used / (1024 ** 3):.2f} GB of {memory_info.total / (1024 ** 3):.2f} GB used)\n"
#             f"Diskanvändning:\t\t{disk_usage.percent}% ({disk_usage.used / (1024 ** 3):.2f} GB out of {disk_usage.total / (1024 ** 3):.2f} GB used)\n"
#         )

#         logformon.log(
#             f"Användaren har hämtat ögonblicksbild av resursanvändningen:\n"
#             f"CPU Användning: {cpu_usage}%\n"
#             f"Minnessanvändning: {memory_info.percent}% ({memory_info.used / (1024 ** 3):.2f} GB of {memory_info.total / (1024 ** 3):.2f} GB used)\n"
#             f"Diskanvändning: {disk_usage.percent}% ({disk_usage.used / (1024 ** 3):.2f} GB out of {disk_usage.total / (1024 ** 3):.2f} GB used)"
#         )

#         return status

#     def check_status(self, alarm_manager):
#         cpu_usage = psutil.cpu_percent(interval=0)
#         memory_usage = psutil.virtual_memory().percent
#         disk_usage = psutil.disk_usage('/').percent
#         alarm_manager.check_alarm(cpu_usage, memory_usage, disk_usage)


# class AlarmManager:
#     def __init__(self):
#         self.alarms = {"CPU": [], "Memory": [], "Disk": []}
#         self.load_alarms()

#     def configure_alarm(self):
#         category = simpledialog.askstring("Larm Konfiguration", "Ange kategori (CPU, Memory, Disk):")
#         if category in self.alarms.keys():
#             level_input = simpledialog.askinteger("Ställ in larm", f"Ställ in {category} nivå mellan 1-100:")
#             if level_input and 1 <= level_input <= 100:
#                 self.alarms[category].append(level_input)
#                 self.save_alarms()
#                 return f"{category} larm satt till {level_input}%"
#             else:
#                 return "Felaktig nivå."
#         return "Ogiltig kategori."

#     def display_alarms(self):
#         alarms_list = []
#         for category in ["CPU", "Memory", "Disk"]:
#             for level in sorted(self.alarms[category]):
#                 alarms_list.append(f"{category} larm {level}%")
#         return "\n".join(alarms_list) if alarms_list else "Inga larm att visa."

#     def check_alarm(self, cpu, memory, disk):
#         for category, usage in zip(["CPU", "Memory", "Disk"], [cpu, memory, disk]):
#             for level in sorted(self.alarms[category], reverse=True):
#                 if usage > level:
#                     message = f"*** VARNING, {category} ANVÄNDNING ÖVERSTIGER {level}% ***"
#                     logformon.log(f"Larm AKTIVERAD {message}")
#                     send_email_alert(message)
#                     return


#     def save_alarms(self):
#         with open('alarms.json', 'w') as f:
#             json.dump(self.alarms, f)

#     def load_alarms(self):
#         try:
#             with open('alarms.json', 'r') as f:
#                 self.alarms = json.load(f)
#         except FileNotFoundError:
#             logformon.log("Kunde inte ladda lagrade larm")


# class Logger:
#     def __init__(self):
#         os.makedirs('logs', exist_ok=True)
#         self.filename = os.path.join('logs', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log"))

#     def log(self, message):
#         with open(self.filename, 'a') as f:
#             f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} - {message}\n")


# logger = Logger()
# logformon = Logger()
# alarm_manager = AlarmManager()

# SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
# RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
# SENDER_EMAIL = os.getenv("SENDER_EMAIL")


# def send_email_alert(message):
#     try:
#         email = Mail(
#             from_email=SENDER_EMAIL,
#             to_emails=RECIPIENT_EMAIL,
#             subject="Larm aktiverat i övervakningsapplikationen",
#             plain_text_content=message,
#         )
#         sg = SendGridAPIClient(SENDGRID_API_KEY)
#         response = sg.send(email)
#         print(f"E-post skickat med statuskod {response.status_code}")
#     except Exception as e:
#         print(f"Misslyckades med att skicka e-post: {str(e)}")


# class App:
#     def __init__(self, master):
#         self.master = master
#         master.title("Övervakningsapplikation")
#         self.monitor = Monitor()

#         # Skapa en ram för att hålla knapparna horisontellt
#         button_frame = tk.Frame(master)
#         button_frame.pack(pady=10)

#         # Definiera knapparna
#         button_texts = [
#             "Starta övervakning",
#             "Lista aktiv övervakning",
#             "Skapa larm",
#             "Visa larm",
#             "Starta övervakningsläge",
#             "Ta bort larm",
#             "Realtidsövervakning (Prestanda)",
#             "Kontrollera .env filen för email utskick",
#             "Avsluta programmet"
#         ]

#         # Skapa knappar med tillhörande funktioner
#         self.buttons = {}
#         for text in button_texts:
#             self.buttons[text] = tk.Button(button_frame, text=text, command=lambda t=text: self.button_action(t))
#             self.buttons[text].pack(side=tk.LEFT, padx=5)

#     def button_action(self, button_text):
#         if button_text == "Starta övervakning":
#             self.monitor.start_monitoring()
#             messagebox.showinfo("Information", "Övervakning har startat!")
#         elif button_text == "Lista aktiv övervakning":
#             status = self.monitor.display_status()
#             messagebox.showinfo("Aktiv övervakning", status)
#         elif button_text == "Skapa larm":
#             result = alarm_manager.configure_alarm()
#             messagebox.showinfo("Konfigurera Larm", result)
#         elif button_text == "Visa larm":
#             alarms = alarm_manager.display_alarms()
#             messagebox.showinfo("Larm", alarms)
#         elif button_text == "Starta övervakningsläge":
#             messagebox.showinfo("Information", "Funktion för övervakningsläge är ännu inte implementerad.")
#         elif button_text == "Ta bort larm":
#             messagebox.showinfo("Information", "Funktion för att ta bort larm är ännu inte implementerad.")
#         elif button_text == "Realtidsövervakning (Prestanda)":
#             messagebox.showinfo("Information", "Funktion för realtidsövervakning är ännu inte implementerad.")
#         elif button_text == "Kontrollera .env filen för email utskick":
#             messagebox.showinfo("Information", ".env filen är kontrollerad. Se loggar för mer information.")
#         elif button_text == "Avsluta programmet":
#             self.master.quit()


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = App(root)
#     root.mainloop()



import tkinter as tk
from tkinter import messagebox, simpledialog
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv, find_dotenv, set_key
import psutil
import time
import os
import datetime
import json
import threading


class Monitor:
    def __init__(self):
        self.active = False

    def start_monitoring(self):
        self.active = True
        logformon.log("Övervakning startad.")

    def display_status(self):
        if not self.active:
            return "Ingen övervakning är aktiv. Aktivera alternativ \"1\" från huvudmenyn först!"

        cpu_usage = psutil.cpu_percent(interval=0)
        memory_info = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')

        status = (
            f"CPU Användning:\t\t{cpu_usage}%\n"
            f"Minnesanvändning:\t{memory_info.percent}% ({memory_info.used / (1024 ** 3):.2f} GB of {memory_info.total / (1024 ** 3):.2f} GB used)\n"
            f"Diskanvändning:\t\t{disk_usage.percent}% ({disk_usage.used / (1024 ** 3):.2f} GB out of {disk_usage.total / (1024 ** 3):.2f} GB used)\n"
        )

        logformon.log(
            f"Användaren har hämtat ögonblicksbild av resursanvändningen:\n"
            f"CPU Användning: {cpu_usage}%\n"
            f"Minnessanvändning: {memory_info.percent}% ({memory_info.used / (1024 ** 3):.2f} GB of {memory_info.total / (1024 ** 3):.2f} GB used)\n"
            f"Diskanvändning: {disk_usage.percent}% ({disk_usage.used / (1024 ** 3):.2f} GB out of {disk_usage.total / (1024 ** 3):.2f} GB used)"
        )

        return status

    def check_status(self, alarm_manager):
        cpu_usage = psutil.cpu_percent(interval=0)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        alarm_manager.check_alarm(cpu_usage, memory_usage, disk_usage)


class AlarmManager:
    def __init__(self):
        self.alarms = {"CPU": [], "Memory": [], "Disk": []}
        self.load_alarms()

    def configure_alarm(self):
        category = simpledialog.askstring("Larm Konfiguration", "Ange kategori (CPU, Memory, Disk):")
        if category in self.alarms.keys():
            level_input = simpledialog.askinteger("Ställ in larm", f"Ställ in {category} nivå mellan 1-100:")
            if level_input and 1 <= level_input <= 100:
                self.alarms[category].append(level_input)
                self.save_alarms()
                return f"{category} larm satt till {level_input}%"
            else:
                return "Felaktig nivå."
        return "Ogiltig kategori."

    def display_alarms(self):
        alarms_list = []
        for category in ["CPU", "Memory", "Disk"]:
            for level in sorted(self.alarms[category]):
                alarms_list.append(f"{category} larm {level}%")
        return "\n".join(alarms_list) if alarms_list else "Inga larm att visa."

    def check_alarm(self, cpu, memory, disk):
        for category, usage in zip(["CPU", "Memory", "Disk"], [cpu, memory, disk]):
            for level in sorted(self.alarms[category], reverse=True):
                if usage > level:
                    message = f"*** VARNING, {category} ANVÄNDNING ÖVERSTIGER {level}% ***"
                    logformon.log(f"Larm AKTIVERAD {message}")
                    send_email_alert(message)
                    return

    def save_alarms(self):
        with open('alarms.json', 'w') as f:
            json.dump(self.alarms, f)

    def load_alarms(self):
        try:
            with open('alarms.json', 'r') as f:
                self.alarms = json.load(f)
        except FileNotFoundError:
            logformon.log("Kunde inte ladda lagrade larm")


class Logger:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.filename = os.path.join('logs', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log"))

    def log(self, message):
        with open(self.filename, 'a') as f:
            f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} - {message}\n")


logger = Logger()
logformon = Logger()
alarm_manager = AlarmManager()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")


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
    except Exception as e:
        print(f"Misslyckades med att skicka e-post: {str(e)}")


class App:
    def __init__(self, master):
        self.master = master
        master.title("Övervakningsapplikation")
        self.monitor = Monitor()

        # Skapa en ram för att hålla knapparna horisontellt
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        # Skapa en text widget för att visa övervakningsinformation
        self.text_widget = tk.Text(master, height=15, width=70)
        self.text_widget.pack(pady=10)

        # Definiera knapparna
        button_texts = [
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

        # Skapa knappar med tillhörande funktioner
        self.buttons = {}
        for text in button_texts:
            self.buttons[text] = tk.Button(button_frame, text=text, command=lambda t=text: self.button_action(t))
            self.buttons[text].pack(side=tk.LEFT, padx=5)

    def button_action(self, button_text):
        if button_text == "Starta övervakning":
            self.monitor.start_monitoring()
            messagebox.showinfo("Information", "Övervakning har startat!")
        elif button_text == "Lista aktiv övervakning":
            status = self.monitor.display_status()
            messagebox.showinfo("Aktiv övervakning", status)
        elif button_text == "Skapa larm":
            result = alarm_manager.configure_alarm()
            messagebox.showinfo("Konfigurera Larm", result)
        elif button_text == "Visa larm":
            alarms = alarm_manager.display_alarms()
            messagebox.showinfo("Larm", alarms)
        elif button_text == "Starta övervakningsläge":
            self.start_monitoring_mode()
        elif button_text == "Ta bort larm":
            messagebox.showinfo("Information", "Funktion för att ta bort larm är ännu inte implementerad.")
        elif button_text == "Realtidsövervakning (Prestanda)":
            messagebox.showinfo("Information", "Funktion för realtidsövervakning är ännu inte implementerad.")
        elif button_text == "Kontrollera .env filen för email utskick":
            messagebox.showinfo("Information", ".env filen är kontrollerad. Se loggar för mer information.")
        elif button_text == "Avsluta programmet":
            self.master.quit()

    def start_monitoring_mode(self):
        self.text_widget.delete(1.0, tk.END)  # Rensa textwidget
        self.monitor.start_monitoring()
        self.update_monitoring()

    def update_monitoring(self):
        status = self.monitor.display_status()
        self.text_widget.insert(tk.END, status + "\n")
        alarm_manager.check_status(self.monitor)  # Kontrollera larm
        self.master.after(1000, self.update_monitoring)  # Uppdatera var 1 sekund


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    root = tk.Tk()
    app = App(root)
    root.mainloop()
