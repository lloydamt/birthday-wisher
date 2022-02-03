import pandas
import datetime as dt
import random
import smtplib
from decouple import config

# 1 - read birthdays
# 2 - loop through birthdays and check if any date is equal to the present date
# 3 - create an smtp connection
# 4 - select random mail from available mails and open file to read its contents
# 5 - replace letter name with recipient name
# 6 - send email to birthday-person

# Global variables
MY_EMAIL = config('email')
PASSWORD = config('password')

# replace name in mail
def change_name(name):
    letter_num = random.randint(1, 3)
    try:
        with open(f"letter_templates/letter_{letter_num}.txt") as letter_file:
            letter_content = letter_file.read()
    except FileNotFoundError:
        letter_content = "Hello [NAME],\nHappy Birthday!\nWish you all the best\nAMT"
        new_mail = letter_content.replace('[NAME]', name)
    else:
        new_mail = letter_content.replace('[NAME]', name)
    finally:
        return new_mail

# send email
def send_email(email_add, content):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=email_add,
                            msg=f"Subject:Happy Birthday!"
                                f"\n\n{content}"
                            )

# check present date
today = dt.datetime.now()
day = today.day
month = today.month

# read birthdays
data = pandas.read_csv("birthdays.csv")
friends_data = data.to_dict(orient="records")

# loop through friend data to check dates
for friend in friends_data:
    if friend['month'] == month and friend['day'] == day:
        birthday_email = change_name(friend['name'])
        send_email(email_add=friend['email'], content=birthday_email)
