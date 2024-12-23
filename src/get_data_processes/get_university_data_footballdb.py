import requests
from bs4 import BeautifulSoup
import csv

def get_university_data():
    base_url = 'https://www.footballdb.com/players/current.html?letter='
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
        
        # Find the div containing the table
        table_div = soup.find('div', {'class': 'divtable divtable-striped'})  

        # Check if the table exists
        if table_div:
            # Iterate over the rows in the table
            for row in table_div.find_all('div', class_='tr'):
                # Collect the data into a dictionary
                row_data = [td.get_text(strip=True) for td in row.find_all('div', class_='td')]
                if len(row_data) >= 4:
                    university_data.append({
                        'Player': row_data[0],
                        'Position': row_data[1],
                        'Team': row_data[2],
                        'College': row_data[3]
                    })
        else:
            print("Table not found")
    
    # Write the data to a CSV file
    with open('../data/raw/player_university_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['Player', 'Position', 'Team', 'College']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(university_data)
        
        print("Data has been successfully written to university_data.csv")
        