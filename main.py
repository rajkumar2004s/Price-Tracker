import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
import re
from config import *

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_price(url):
    try:
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("Failed to fetch page")
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        price_element = soup.select_one(".a-price-whole")

        if price_element:
            price_text = price_element.text.strip()
            price_number = re.findall(r"[\d,]+", price_text)

            if price_number:
                return float(price_number[0].replace(",", ""))

        return None

    except Exception as e:
        print("Error fetching price:", e)
        return None


def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = FROM_EMAIL
        msg["To"] = TO_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(FROM_EMAIL, FROM_PASSWORD)
            server.send_message(msg)

        print("📧 Email sent successfully!")

    except Exception as e:
        print("Email error:", e)


def track_price():
    print("Starting price tracking 🚀...")

    # price = get_price(URL)
    price = 55000

    if price:
        print(f"Current Price: ₹{price}")

        if price <= TARGET_PRICE:
            send_email(
                "Price Dropped!",
                f"Price is now ₹{price}\nCheck here: {URL}"
            )
        else:
            print("Price not yet low enough.")
    else:
        print("Could not fetch price.")


if __name__ == "__main__":
    track_price()