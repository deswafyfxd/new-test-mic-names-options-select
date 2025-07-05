import random
import requests
from faker import Faker
import apprise
import time
import string
import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Get country from command-line argument
country = sys.argv[1] if len(sys.argv) > 1 else 'IN'
logging.info(f"Generating {country} names")

# Initialize Faker instances based on country
if country == 'US':
    name_faker = Faker('en_US')
    logging.info("Using US names")
else:  # Default to IN
    name_faker = Faker('en_IN')
    logging.info("Using Indian names")

# English Faker for other fields
fake_en = Faker('en_US')

def generate_unique_dobs(count):
    """Generate unique date of birth tuples (year, month, day)"""
    years = random.sample(range(1990, 2001), count)
    months = random.sample(range(1, 13), count)
    days = random.sample(range(1, 29), count)
    return [(years[i], months[i], days[i]) for i in range(count)]

def check_github_username_availability(username):
    """Check if GitHub username is available"""
    try:
        response = requests.get(f"https://api.github.com/users/{username}", timeout=10)
        return response.status_code == 404
    except requests.RequestException as e:
        logging.warning(f"GitHub API request failed: {e}")
        return False

def send_to_discord(webhook_url, account_number, details):
    """Send account details to Discord via webhook"""
    # FIXED: Proper Discord URL formatting
    notify = apprise.Apprise()
    notify.add(f"discord://{webhook_url.split('/')[-2]}/{webhook_url.split('/')[-1]}")
    
    message = (
        f"**Account {account_number} ({details['country']})**\n"
        f"First name: {details['first_name']}\n"
        f"Last name: {details['last_name']}\n"
        f"Email: {details['email']}\n"
        f"GitHub: {details['github_username']}\n"
        f"Bio: {details['bio']}\n"
        f"Location: {details['location']}\n"
        f"Company: {details['company']}\n"
        f"Website: {details['website']}\n"
        f"DOB: {details['dob']}\n"
        "--------------------------"
    )
    
    return notify.notify(body=message)

def generate_username(base, num_digits):
    """Generate username with random digits"""
    if num_digits > 0:
        return f"{base}{''.join(random.choices(string.digits, k=num_digits))}"
    return base

def generate_github_username(first, last, num_digits):
    """Generate GitHub username with availability fallback"""
    base = f"{first.lower()}{last.lower()}"
    username = generate_username(base, num_digits)
    
    # Add digits if initial username is taken
    if not check_github_username_availability(username) and num_digits == 0:
        return generate_username(base, 3)
    return username

# Generate random profile details
def generate_bio(): return fake_en.sentence(nb_words=10)
def generate_location(): return fake_en.city()
def generate_company(): return fake_en.company()
def generate_website(): return fake_en.url()

# ===== CONFIGURATION =====
# FIXED: Get webhook from environment variable
WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK')
if not WEBHOOK_URL:
    logging.error("Missing Discord webhook URL!")
    exit(1)
    
NUM_ACCOUNTS = 6
EMAIL_DIGITS = 3
GITHUB_DIGITS = 0
# =========================

if __name__ == "__main__":
    # Test Discord connection
    notify_test = apprise.Apprise()
    # FIXED: Proper URL formatting
    notify_test.add(f"discord://{WEBHOOK_URL.split('/')[-2]}/{WEBHOOK_URL.split('/')[-1]}")
    
    if notify_test.notify(body=f"🚀 Generating {NUM_ACCOUNTS} {country} accounts"):
        logging.info("Discord connection test successful")
    else:
        logging.error("Discord connection failed")
    
    # Generate accounts
    accounts_created = 0
    unique_dobs = generate_unique_dobs(NUM_ACCOUNTS)
    
    while accounts_created < NUM_ACCOUNTS:
        first_name = name_faker.first_name()
        last_name = name_faker.last_name()
        base_username = f"{first_name}{last_name}".lower()
        
        # Generate credentials
        email = f"{generate_username(base_username, EMAIL_DIGITS)}@outlook.com"
        github_user = generate_github_username(first_name, last_name, GITHUB_DIGITS)
        
        if check_github_username_availability(github_user):
            dob = unique_dobs[accounts_created]
            dob_str = f"{dob[0]}-{dob[1]:02d}-{dob[2]:02d}"
            
            account_details = {
                "country": country,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "github_username": github_user,
                "bio": generate_bio(),
                "location": generate_location(),
                "company": generate_company(),
                "website": generate_website(),
                "dob": dob_str
            }
            
            # Send to Discord
            if send_to_discord(WEBHOOK_URL, accounts_created + 1, account_details):
                logging.info(f"Sent {country} account {accounts_created + 1} to Discord")
                accounts_created += 1
            else:
                logging.error(f"Failed to send account {accounts_created + 1}")
        else:
            logging.warning(f"GitHub username {github_user} unavailable, retrying...")
        
        time.sleep(2)  # Respect GitHub API rate limits
