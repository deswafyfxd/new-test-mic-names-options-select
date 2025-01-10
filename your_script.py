import random
import requests
from faker import Faker
import apprise
import time
import string  # Import the string module
import logging

# Initialize Faker
fake = Faker('en_IN')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to generate unique date of birth combinations
def generate_unique_dobs(count):
    unique_dobs = set()
    while len(unique_dobs) < count:
        year = random.randint(1990, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Simplified to avoid dealing with different month lengths
        dob = (year, month, day)
        unique_dobs.add(dob)
    return list(unique_dobs)

# Function to check username availability (default to True)
def check_username_availability(username):
    return True  # Always return True to indicate availability

# Function to send details to Discord webhook using Apprise
def send_to_discord(webhook_url, account_number, details):
    discord_url = f"discord://{webhook_url}"
    notify = apprise.Apprise(discord_url)
    result = notify.notify(
        body=f"(Account {account_number})\n"
             f"First name: {details['first_name']}\n"
             f"Last name: {details['last_name']}\n"
             f"Username: {details['username']}\n"
             f"Date of Birth: {details['dob']}"
    )
    if result:
        logging.info(f"Message sent successfully for Account {account_number}")
    else:
        logging.error(f"Failed to send message for Account {account_number}")

# Function to generate a random username with a specified number of random digits
def generate_username(first_name, last_name, num_digits):
    username = f"{first_name.lower()}{last_name.lower()}"
    if num_digits > 0:
        random_digits = ''.join(random.choices(string.digits, k=num_digits))
        username += random_digits
    return f"{username}@outlook.com"

# Discord webhook URL (replace with your actual webhook URL)
webhook_url = "discord://1249221380491186276/6d2llfGXypQ7hsCBzaiZq4rX7LirwK98X6vRrewv8_NyQ9ypujss4Tj0ysCgJVzXpSH1"

# Test sending a simple message to Discord
simple_message = apprise.Apprise()
simple_message.add(f"discord://{webhook_url}")
if simple_message.notify(body="Test message to ensure Discord setup is working"):
    logging.info("Test message sent successfully!")
else:
    logging.error("Failed to send test message.")

# Number of accounts to generate
num_accounts = 3

# Number of random digits to append to the username
num_random_digits = 3  # Customize this as needed

# Generate unique date of birth combinations
unique_dobs = generate_unique_dobs(num_accounts)

# Generate account details
account_count = 0
while account_count < num_accounts:
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = generate_username(first_name, last_name, num_random_digits)

    # Ensure we have a unique date of birth for each account
    dob = unique_dobs[account_count % len(unique_dobs)]
    dob_str = f"{dob[0]:04d}-{dob[1]:02d}-{dob[2]:02d}"

    # Check username availability
    if check_username_availability(username):
        account_details = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "dob": dob_str
        }
        send_to_discord(webhook_url, account_count + 1, account_details)
        account_count += 1
    else:
        print(f"Username {username} is not available. Trying again...")
        
    if account_count < num_accounts:
        unique_dobs = generate_unique_dobs(num_accounts - account_count)
    time.sleep(1)  # Delay to prevent rapid retrying
