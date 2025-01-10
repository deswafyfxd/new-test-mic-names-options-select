import random
import requests
from faker import Faker

# Initialize Faker
fake = Faker('en_IN')

# Generate unique date of birth combinations
def generate_unique_dobs(count):
    unique_dobs = set()
    while len(unique_dobs) < count:
        year = random.randint(1990, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Simplified to avoid dealing with different month lengths
        dob = (year, month, day)
        unique_dobs.add(dob)
    return list(unique_dobs)

# Function to check username availability (stub function, replace with actual API call if available)
def check_username_availability(username):
    # Example response simulating availability check
    available = random.choice([True, False])
    return available

# Function to send details to Discord webhook
def send_to_discord(webhook_url, account_number, details):
    payload = {
        "content": f"(Account {account_number})\n"
                   f"First name: {details['first_name']}\n"
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

# Number of accounts to generate
num_accounts = 3

# Generate unique date of birth combinations
unique_dobs = generate_unique_dobs(num_accounts)

# Generate account details
for i, dob in enumerate(unique_dobs, start=1):
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = first_name.lower() + last_name.lower() + "@outlook.com"
    dob_str = f"{dob[0]:04d}-{dob[1]:02d}-{dob[2]:02d}"

    # Check username availability
    if check_username_availability(username):
        account_details = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "dob": dob_str
        }
        send_to_discord(webhook_url, i, account_details)
    else:
        print(f"Username {username} is not available. Trying again...")
