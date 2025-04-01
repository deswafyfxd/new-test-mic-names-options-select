import random
import requests
from faker import Faker
import apprise
import time
import string
import logging

# Initialize Faker for English locale for bios and Indian locale for names
fake_en = Faker('en_US')
fake_in = Faker('en_IN')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to generate unique date of birth combinations
def generate_unique_dobs(count):
    years = random.sample(range(1990, 2001), count)  # Ensure unique years
    months = random.sample(range(1, 13), count)  # Ensure unique months
    days = random.sample(range(1, 29), count)  # Ensure unique days
    unique_dobs = [(years[i], months[i], days[i]) for i in range(count)]
    return unique_dobs

# Function to check username availability on GitHub
def check_github_username_availability(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 404:
        return True  # Username is available
    return False  # Username is taken

# Function to send details to Discord webhook using Apprise
def send_to_discord(webhook_url, account_number, details):
    discord_url = f"discord://{webhook_url}"
    notify = apprise.Apprise()
    notify.add(discord_url)
    result = notify.notify(
        body=f"(Account {account_number})\n"
             f"First name: {details['first_name']}\n"
             f"Last name: {details['last_name']}\n"
             f"Username: {details['username']}\n"
             f"GitHub Username: {details['github_username']}\n"
             f"Bio: {details['bio']}\n"
             f"Location: {details['location']}\n"
             f"Company: {details['company']}\n"
             f"Website: {details['website']}\n"
             f"Date of Birth: {details['dob']}\n"
             "----------------------------------"
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
    return username

# Function to generate a GitHub username with fallback to adding digits if initial username is unavailable
def generate_github_username(first_name, last_name, num_digits):
    github_username = generate_username(first_name, last_name, num_digits)
    if not check_github_username_availability(github_username) and num_digits == 0:
        # Add 3 random digits if the username is unavailable and num_digits is set to 0
        github_username = generate_username(first_name, last_name, 3)
    return github_username

# Function to generate a random bio in English
def generate_random_bio():
    return fake_en.sentence(nb_words=10)  # Customize the number of words as needed

# Function to generate a random location
def generate_random_location():
    return fake_en.city()

# Function to generate a random company
def generate_random_company():
    return fake_en.company()

# Function to generate a random website
def generate_random_website():
    return fake_en.url()

# Discord webhook URL
webhook_url = "1249221380491186276/6d2llfGXypQ7hsCBzaiZq4rX7LirwK98X6vRrewv8_NyQ9ypujss4Tj0ysCgJVzXpSH1"

# Test sending a simple message to Discord
simple_message = apprise.Apprise()
simple_message.add(f"discord://{webhook_url}")
if simple_message.notify(body="Test message to ensure Discord setup is working"):
    logging.info("Test message sent successfully!")
else:
    logging.error("Failed to send test message.")

# Number of accounts to generate
num_accounts = 6

# Number of random digits to append to the email and GitHub usernames
num_email_digits = 3  # Customize this as needed for email username
num_github_digits = 0  # Customize this as needed for GitHub username, 0 means no digits unless the username is taken

# Generate unique date of birth combinations
unique_dobs = generate_unique_dobs(num_accounts)

# Generate account details
account_count = 0
while account_count < num_accounts:
    first_name = fake_in.first_name()
    last_name = fake_in.last_name()
    
    # Generate email username
    email_username = generate_username(first_name, last_name, num_email_digits)
    email_username_full = f"{email_username}@outlook.com"
    
    # Generate GitHub username with fallback digits
    github_username = generate_github_username(first_name, last_name, num_github_digits)

    # Generate a random bio in English
    github_bio = generate_random_bio()
    
    # Generate random GitHub details
    github_location = generate_random_location()
    github_company = generate_random_company()
    github_website = generate_random_website()

    # Ensure we have a unique date of birth for each account
    dob = unique_dobs[account_count % len(unique_dobs)]
    dob_str = f"{dob[0]:04d}-{dob[1]:02d}-{dob[2]:02d}"

    # Check GitHub username availability
    if check_github_username_availability(github_username):
        account_details = {
            "first_name": first_name,
            "last_name": last_name,
            "username": email_username_full,
            "github_username": github_username,
            "bio": github_bio,
            "location": github_location,
            "company": github_company,
            "website": github_website,
            "dob": dob_str
        }
        send_to_discord(webhook_url, account_count + 1, account_details)
        account_count += 1
    else:
        logging.info(f"GitHub username {github_username} is not available. Trying again...")
        
    if account_count < num_accounts:
        unique_dobs = generate_unique_dobs(num_accounts - account_count)
    time.sleep(1)  # Delay to prevent rapid retrying
