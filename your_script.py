import random
import requests
from faker import Faker

# Initialize Faker
fake = Faker('en_IN')

# Function to generate random date of birth between 1990 and 2000
def generate_random_dob():
    year = random.randint(1990, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Simplified to avoid dealing with different month lengths
    return f"{year:04d}-{month:02d}-{day:02d}"

# Function to check username availability (stub function, replace with actual API call if available)
def check_username_availability(username):
    # Example response simulating availability check
    available = random.choice([True, False])
    return available

# Function to send details to Discord webhook
def send_to_discord(webhook_url, details):
    payload = {
        "content": f"First name: {details['first_name']}\n"
                   f"Last name: {details['last_name']}\n"
                   f"Username: {details['username']}\n"
                   f"Date of Birth: {details['dob']}"
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

# Discord webhook URL (replace with your actual webhook URL)
webhook_url = "https://discord.com/api/webhooks/1249221380491186276/6d2llfGXypQ7hsCBzaiZq4rX7LirwK98X6vRrewv8_NyQ9ypujss4Tj0ysCgJVzXpSH1"

# Generate 3 account details
for _ in range(3):
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = first_name.lower() + last_name.lower() + "@outlook.com"
    dob = generate_random_dob()

    # Check username availability
    if check_username_availability(username):
        account_details = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "dob": dob
        }
        send_to_discord(webhook_url, account_details)
    else:
        print(f"Username {username} is not available. Trying again...")
