Certainly! Here's a `README.md` file for your script:

```markdown
# Calendly Contacts Extractor

This Python script extracts all contacts from Calendly by querying the API and handles pagination to ensure all contacts are fetched. The script stores the contacts in a text file and a CSV file, with filenames that include the current date. The script also outputs the number of unique contacts extracted.

## Features

- Queries Calendly API to fetch contacts.
- Handles pagination to extract all contacts.
- Stores contacts in a text file and a CSV file.
- Appends the current date to the filenames.
- Outputs the number of unique contacts extracted.

## Requirements

- Python 3.x
- `requests` module

## Installation

1. Clone the repository or download the script.
2. Install the required Python module:

```bash
pip install requests
```

## Usage

1. Replace the `calendly_session` variable in the script with your Calendly session ID cookie.
2. Run the script:

```bash
python calendly_contacts_extractor.py
```

## Script Details

### Functions

- `get_contacts(url)`: Sends an HTTP GET request to the specified URL to fetch contacts and handles any HTTP errors.

### Process

1. The script starts with the base URL for the API.
2. It loops through each page of contacts, adding the contacts to a set to ensure uniqueness, and then moves to the next page using the `next_page` URL provided in the response.
3. After fetching all contacts, the script writes the contacts to a text file and a CSV file with filenames that include the current date.
4. The script prints the total number of unique contacts extracted.

## Example Output

The script will generate two files in the working directory:

- `contacts_YYYY-MM-DD.txt`
- `contacts_YYYY-MM-DD.csv`

Where `YYYY-MM-DD` is the current date.

Additionally, the script will print the number of unique contacts extracted:

```plaintext
Finished fetching contacts.
Total unique contacts fetched: 123
Writing contacts to contacts_2023-07-03.txt
Finished writing to contacts_2023-07-03.txt
Writing contacts to contacts_2023-07-03.csv
Finished writing to contacts_2023-07-03.csv
Number of unique contacts extracted: 123
```

## Contributing

If you have suggestions for improving this script, feel free to create an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
```

