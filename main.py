import json
import os
from datetime import datetime
import pandas as pd
import requests

HEADERS = {'birthday': 'Birthday Date'}

whatsappUrl = os.getenv('CALL_ME_BOT_URL')
apiKey = os.getenv('CALL_ME_BOT_API_KEY')


def send_message(data):
    message_image = data['message'] + '\n' + data['name'] + '\n' + data['dob'] + '\n\n' + data['image']
    resp = requests.get(f"{whatsappUrl}/whatsapp.php?phone=+{data['contact']}&text={message_image}&apikey={apiKey}")
    write_text(resp.text)


def load_google_sheet():
    google_sheet_url = os.getenv("GOOGLE_SHEET_URL")
    url = google_sheet_url.replace('/edit?usp=sharing', '/export?format=csv')
    df = pd.read_csv(url)
    print(url)
    return df


def split_date(date):
    return date.split('/')


def write_json(data):
    with open('birthday.json', 'w') as outfile:
        json.dump(data, outfile)


def write_text(data):
    with open('callmebot.txt', 'a') as outfile:
        outfile.write(str("\n" + data))


def find_today_birthday(input_date=None):
    if input_date is None:
        return False
    today = datetime.today().strftime('%m/%d/%Y')
    month, day, year = split_date(input_date)
    t_month, t_day, t_year = split_date(today)

    if int(month) == int(t_month):
        if int(day) == int(t_day):
            print('FOUND')
            return True
    print('NOT FOUND')
    return False


def load_offline():
    df = pd.read_csv('data.csv')
    return df


def load_birthday():
    df = load_google_sheet()
    df['is_birth_day'] = df[HEADERS['birthday']].apply(find_today_birthday)
    df2 = df.loc[df['is_birth_day'] == True]
    found = df2.values.tolist()
    keys = ['name', 'contact', 'message', 'dob', 'image']
    birthdays = [dict(zip(keys, value)) for value in found]
    write_json(birthdays)
    for birthday in birthdays:
        send_message(birthday)


if __name__ == '__main__':
    load_birthday()
