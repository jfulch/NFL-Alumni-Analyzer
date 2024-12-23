import requests
from bs4 import BeautifulSoup
import csv

# Archive of v1 that get data from ESPN.
# This appeared to be missing some player info, so I used a new source for the data.
def get_espn_university_data():
    base_url = 'https://www.espn.com/nfl/college/_/letter/'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    # Initialize an empty list to store the data
    university_data = []

    # Get college football affiliate data
    for letter in alphabet:
        response = requests.get(base_url + letter, headers=headers)
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        # Find the table containing the list of presidents
        table = soup.find('table', {'class': 'tablehead'})

        # Check if the table exists
        if table:
            university_name = None
            # Iterate over the rows in the table
            for row in table.find_all('tr'):
                # Check if the row has the class 'stathead' to get the university name
                if 'stathead' in row.get('class', []):
                    university_name = row.get_text(strip=True)
                elif university_name:
                    # Collect the data into a dictionary
                    row_data = [td.get_text(strip=True) for td in row.find_all('td')]
                    if len(row_data) >= 3 and row_data[0] != 'PLAYER' and row_data[1] != 'TEAM' and row_data[2] != 'POSITION':
                        university_data.append({
                            'University': university_name,
                            'Player': row_data[0],
                            'Team': row_data[1],
                            'Position': row_data[2]
                        })
        else:
            print("Table not found")

    # Write the data to a CSV file
    with open('../data/raw/player_university_data_ESPN.csv', 'w', newline='') as csvfile:
        fieldnames = ['University', 'Player', 'Team', 'Position']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(university_data)
        
        print("Data has been successfully written to data/university_data_ESPN.csv")

get_espn_university_data()