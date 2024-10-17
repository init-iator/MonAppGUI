import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from logger import Logger
from dotenv import load_dotenv, find_dotenv, set_key
from textdecor import textdec

txd = textdec()

# Ladda miljövariabler från .env-filen
load_dotenv(".env", override=True)

email_logger = Logger()

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
        email_logger.log(f"E-post skickat med statuskod {response.status_code}")
    except Exception as e:
        print(f"Misslyckades med att skicka e-post: {str(e)}")
        email_logger.log(f"Misslyckades med att skicka e-post: {str(e)}")

def create_or_update_env_file():
    """
    Prompts the user to create or update a .env file.
    """

    dotenv_path = find_dotenv()

    if dotenv_path:
        # .env-fil hittades, ladda innehållet
        load_dotenv(dotenv_path)
        print(f"{txd.GREEN}Hittade en befintlig .env-fil med följande innehåll:{txd.END}")
        print(f"{txd.BLUE}SENDGRID_API_KEY{txd.END}={os.getenv('SENDGRID_API_KEY')}")
        print(f"{txd.BLUE}RECIPIENT_EMAIL{txd.END}={os.getenv('RECIPIENT_EMAIL')}")
        print(f"{txd.BLUE}SENDER_EMAIL{txd.END}={os.getenv('SENDER_EMAIL')}")

        # Fråga användaren om informationen stämmer
        confirm = input(f"Stämmer ovanstående information? ({txd.GREEN}ja{txd.END}/{txd.RED}nej{txd.END}): ")
        if confirm.lower() == "ja":
            print(f"{txd.BOLD}{txd.YELLOW}.env-filen har lästs in.{txd.END}{txd.END}")

        elif confirm.lower() != "ja":
            
            # Om användaren svarar nej, prompt för nya värden
            sendgrid_api_key = input("Ange SendGrid API-nyckel: ")
            recipient_email = input("Ange mottagarens e-postadress: ")
            sender_email = input("Ange avsändarens e-postadress: ")

            # Uppdatera värdena i .env-filen
            set_key(dotenv_path, "SENDGRID_API_KEY", sendgrid_api_key)
            set_key(dotenv_path, "RECIPIENT_EMAIL", recipient_email)
            set_key(dotenv_path, "SENDER_EMAIL", sender_email)
            print(f"{txd.BOLD}{txd.YELLOW}.env-filen har uppdaterats. {txd.RED}STARTA OM PROGRAMMET!{txd.END}{txd.END}{txd.END}")
    else:
        # .env-fil hittades inte, skapa en ny
        print(f"{txd.BOLD}{txd.YELLOW}.env-fil hittades inte, skapa en ny{txd.END}{txd.END}")
        sendgrid_api_key = input("Ange SendGrid API-nyckel: ")
        recipient_email = input("Ange mottagarens e-postadress: ")
        sender_email = input("Ange avsändarens e-postadress: ")
        print(f"{txd.BOLD}{txd.YELLOW}.env-filen har uppdaterats. {txd.RED}STARTA OM PROGRAMMET!{txd.END}{txd.END}{txd.END}")

        with open('.env', 'w') as f:
            f.write(f"SENDGRID_API_KEY={sendgrid_api_key}\n")
            f.write(f"RECIPIENT_EMAIL={recipient_email}\n")
            f.write(f"SENDER_EMAIL={sender_email}\n")