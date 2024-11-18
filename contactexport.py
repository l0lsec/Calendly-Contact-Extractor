import requests
import json
import csv
import time
import urllib.parse
from datetime import datetime

# Calendly session cookie
calendly_session = "YOUR_SESSION_COOKIE_HERE"

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
all_fieldnames = set()  # To track all possible fieldnames dynamically

# Start with the base URL
current_url = base_url

# Loop to fetch contacts from all pages
while current_url:
    contacts_data = get_contacts(current_url)
    for contact in contacts_data.get("contacts", []):
        unique_contacts.add(json.dumps(contact))  # Convert dict to string for uniqueness
        all_fieldnames.update(contact.keys())  # Dynamically collect all fieldnames
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

# Ensure all_fieldnames are sorted for consistent output
sorted_fieldnames = sorted(all_fieldnames)

# Write contacts to a text file
text_filename = f'contacts_{current_date}.txt'
print(f"Writing contacts to {text_filename}")
with open(text_filename, 'w') as file:
    for contact in unique_contacts_list:
        file.write(json.dumps(contact) + '\n')
print(f"Finished writing to {text_filename}")

# Write contacts to a CSV file
csv_filename = f'contacts_{current_date}.csv'
print(f"Writing contacts to {csv_filename}")
try:
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=sorted_fieldnames)
        writer.writeheader()
        for contact in unique_contacts_list:
            # Fill missing fields with None
            sanitized_contact = {field: contact.get(field, None) for field in sorted_fieldnames}
            writer.writerow(sanitized_contact)
    print(f"Finished writing to {csv_filename}")
except IOError:
    print("I/O error during writing to CSV file")

# Output the number of unique contacts extracted
print(f"Number of unique contacts extracted: {len(unique_contacts_list)}")
