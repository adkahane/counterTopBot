from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import date
import os
from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv

# Setup logging
import logging
logging.basicConfig(format="%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] - %(message)s",
                    datefmt="%h %dth - %I:%M:%S %p",
                    filename="log.log",
                    filemode="w",
                    level=logging.DEBUG)

# Variables
clear = lambda: os.system('clear')
start_time = time.time()
target_price = '57'

# Webdriver setup
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Load Environment Variables from .env
dotenv_path = find_dotenv('twilio.env')
load_dotenv(dotenv_path)

# The Banner
def banner():
    the_banner = """
      _____                  _            _                ____        _   
     / ____|                | |          | |              |  _ \      | |  
    | |     ___  _   _ _ __ | |_ ___ _ __| |_ ___  _ __   | |_) | ___ | |_ 
    | |    / _ \| | | | '_ \| __/ _ \ '__| __/ _ \| '_ \  |  _ < / _ \| __|
    | |___| (_) | |_| | | | | ||  __/ |  | || (_) | |_) | | |_) | (_) | |_ 
     \_____\___/ \__,_|_| |_|\__\___|_|   \__\___/| .__/  |____/ \___/ \__|
                                                  | |                      
                                                  |_|    \n\n                  
    """
    print(the_banner)

# Send SMS
def send_sms():
    # Set up Twilio auth with environment variables
    print(os.getenv('TWILIO_ACCOUNT_SID'))
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
   
    # SMS message to send
    msg ="""
                        
    Hey, go check IKEA.
    Your countertops are on sale. 
        Love,
        CounterTop Bot
        """
    print(msg)
    print("Sending sms")

    message = client.messages \
                    .create(
                        body=msg,
                        from_='+16614664274',
                        to='+16094577472'
                    )
    logging.info(message.sid)

# Main loop
def main():
    found = False
    banner()
    print("Finding countertops for my beautiful wife")
    print("Let's check IKEA")
    driver.get("https://www.ikea.com/us/en/p/kasker-custom-countertop-light-gray-beige-marble-effect-quartz-80395007/#content")
    driver.implicitly_wait(1)

    while found == False:
        clear()
        now = time.localtime()
        curDate = date.today()
        current_time = time.strftime("%H:%M:%S", now)
        print("\nStats:")
        print("Last time price checked --> ", curDate, current_time)
        print(f"Checking if Current price is below {target_price}\n")
        cur_price = driver.find_element(By.CLASS_NAME, "pip-temp-price__integer")

        # Check the price of the countertop
        if cur_price.text <= target_price:
            print(f"Awesome! the price is currently ==> {cur_price.text}")
            send_sms()
            break
        else:
            print(f"The Countertop is still too expensive.\n    ==> Target Price: {target_price}\n    ==> Current price: {cur_price.text}")
            print("\n\nSearching again tomorrow...")
            # Sleep for 1 day
            time.sleep(86400)
            driver.refresh()
            continue

    logging.info("Thanks goodbye I love you!")
    print("We're all done. Bye.")
    driver.close()

if __name__ == "__main__":
    main()