import requests
import re
from bs4 import BeautifulSoup
from config import WEBSITE_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_BOT_CHAT_ID


def find_table_in_response(date):
    url = WEBSITE_URL + date

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    # Send a GET request
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table
        table = soup.find("table", class_="kalendarz_rez")
        return table
    else:
        return -1


def find_available_dates(table):
    available_dates_table = []
    for row in table.find_all("tr"):
        for cell in row.find_all("td"):
            available_date_found = cell.find("a")
            if available_date_found:
                available_date_link = available_date_found.get("href")  # IMPORTANT
                date = re.search(r"\d{4}-\d{2}-\d{2}", available_date_link)
                available_dates_table.append(date.group())
    return available_dates_table


def send_telegram_message(message):
    bot_token = TELEGRAM_BOT_TOKEN
    url = url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": TELEGRAM_BOT_CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Telegram message sent!")
    else:
        print(f"Failed to send message: {response.text}")


if __name__ == "__main__":
    dates = ["2024-11-18", "2024-11-25"]
    for start_date in dates:
        table = find_table_in_response(start_date)
        available_dates = find_available_dates(table)
        if available_dates:
            message = f"JEST TERMIN KURWA\nW TYGODNIU: {start_date}"
            send_telegram_message(message)
        print(available_dates)
