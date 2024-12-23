import requests
from bs4 import BeautifulSoup
import csv

# Scrapes NCAA website standings to get the list of FBS schools and their conferences
def get_conference_data():
    url = "https://www.ncaa.com/standings/football/fbs"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    schools_conferences = []

    tables = soup.find_all('table')
    for table in tables:
        # Find the conference name using the class 'standings-conference'
        conference_header = table.find_previous(class_='standings-conference')
        if conference_header:
            conference_name = conference_header.text.strip()
        else:
            conference_name = "Unknown Conference"
        
        rows = table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cells = row.find_all('td')
            if cells:
                school = cells[0].text.strip()
                schools_conferences.append([school, conference_name])

    # Write to CSV file
    with open('../data/raw/schools_conferences.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['School', 'Conference'])  # Write header
        writer.writerows(schools_conferences)

    print("CSV file 'schools_conferences.csv' has been created successfully.")