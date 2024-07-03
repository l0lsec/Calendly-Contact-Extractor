import requests
import json
import csv
import time
import urllib.parse
from datetime import datetime

# Calendly session cookie
calendly_session = "HkyT9UKkpKLu4%2F3pm2thC5NkBzMF1N4Aosgu%2Bwe%2B3zt%2Fww7Nj0jTvEr30Id0ahlpqHMmPju6k2O0LZ0XqZJOEtRkTyOu1MeubWKuAqxqB627bVtQan4Xe%2FklQMMU03UsPoxf3HmhjYYnZ7qW3Ml83rds5tpTk6Tz0aDXp9dTLCIXQwQoKowhM6oTmMDgr4ps0ydxVLsqn13mtx9ewG90FhMh8wCSeONyRqZlBD2Xhf9DTe8HcgX3ae6Z0cDMN8ZqV0qDR12z9he45QozL4WnZQuaMFX6EpFIskKELcJjw%2F5%2Bw6LplfIEqDZVOxVXMI5srfpECRqeJSQONKbmczL6nXVaKprjlyTd4qdq9j56fmIOw59hyqXxNBYRe0mj1Uz9xUcxOE8YKdVQC3EUDVGvq6sWcSBtWDYO8B%2FZ3KS7vzDGSOETr%2Ff1sk1%2Fk3IGa9yH%2BYDw%2FLFaJoMnIeSOO0Ia1p2Eu7xmyoncaVwp0LEbynlQmozcCoTdHJVIF5y2i8MYI9gdAqPY4Z8iTckD5jM8sHFftrvp7AuhezdeR0ugoKvnoRMQatC5eK7k6JgN%2B0ZM6bb4UyhbVSDxJQDqTCmo4LxakzEOsZoU6BSppn4ezgpy%2FwCjAU2Qa7bl7Ev6s2GOmMyLVA88ZDgJBPCBM%2BKnyDI0Fnaz5PWR9n8TvHB%2BSbkpIOXB2Uqzub1inQ1W19CZMz7ks16GyEwmvP%2F7kLXLSRHYRMdlavP7ANNddEcOOObAmbjbsBr8VIDe5KOtLd12nj%2B%2BjT8xaKKvuOr7tpGswxlqAlGGR6HiE93Jix6M%2BXnMBJJp0VHXrVaircx%2B%2FlV3Erynej2Kr6d8y17GjTW0clNkYkZvL7Ybywebci%2Fi1p9LkHFdgpZqiq%2FT5x3ro79d5G8OSsijMgBo7XJhJFcygtEPozrsG53%2FG35q%2FX7wkcYuzWcaJnxm%2FwVB5X8AndNCZCiPTGxLHfg8uL3kTeOuCVxwtYiT6%2F%2FIkPtHPK%2BjizyDCnp4JR2b7QyWQFSWOtzzBbIynwt7fA%3D%3D--Wdf9rGnx860YzBJF--aUlFiZMXoTLU5EfEWt5ZuA%3D%3D"

# Base URL for the API
base_url = "https://calendly.com/api/dashboard/contacts/?contact%5Bfavorite%5D=false&contact%5Bpage_path%5D="

# Headers for the HTTP request
headers = {
    "Cookie": f"_calendly_session={calendly_session}"
}

# Function to get contacts for a given URL
def get_contacts(url):
    print(f"Sending request to URL: {url}")
    response = requests.get(url, headers=headers, timeout=30)  # Set timeout to 30 seconds
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Initialize a set to store unique contacts
unique_contacts = set()

# Start with the base URL
current_url = base_url

# Loop to fetch contacts from all pages
while current_url:
    contacts_data = get_contacts(current_url)
    for contact in contacts_data.get("contacts", []):
        unique_contacts.add(json.dumps(contact))  # Convert dict to string for uniqueness
    print(f"Completed fetching page. Total unique contacts so far: {len(unique_contacts)}")
    
    next_page = contacts_data.get("pagination", {}).get("next_page")
    if next_page:
        next_page_encoded = urllib.parse.quote(next_page, safe='')
        current_url = base_url + next_page_encoded
    else:
        current_url = None
    
    time.sleep(2)  # Adding delay to give the API time to respond

print("Finished fetching contacts.")
print(f"Total unique contacts fetched: {len(unique_contacts)}")

# Convert the set back to a list of dictionaries
unique_contacts_list = [json.loads(contact) for contact in unique_contacts]

# Get the current date
current_date = datetime.now().strftime('%Y-%m-%d')

# Write contacts to a text file
text_filename = f'contacts_{current_date}.txt'
print(f"Writing contacts to {text_filename}")
with open(text_filename, 'w') as file:
    for contact in unique_contacts_list:
        file.write(json.dumps(contact) + '\n')
print(f"Finished writing to {text_filename}")

# Write contacts to a CSV file
csv_filename = f'contacts_{current_date}.csv'
csv_columns = ["uuid", "name", "email", "phone", "time_zone", "favorite", "notes", "visible", "next_event", "last_event"]
print(f"Writing contacts to {csv_filename}")
try:
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for contact in unique_contacts_list:
            writer.writerow(contact)
    print(f"Finished writing to {csv_filename}")
except IOError:
    print("I/O error during writing to CSV file")

# Output the number of unique contacts extracted
print(f"Number of unique contacts extracted: {len(unique_contacts_list)}")
