from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import csv

# User needs to pass in the correct espn URL
def get_nfl_data(url,file_name,defense=False):
    # Initialize the WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-css')
    driver = webdriver.Chrome(options=chrome_options)
    
    # Navigate to the webpage
    driver.get(url)

    # Click "Show More" until all data is loaded
    while True:
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'loadMore__link') and contains(text(), 'Show More')]"))
            )
            show_more_button.click()
            # Wait for the new content to load
            WebDriverWait(driver, 10).until(
                EC.staleness_of(show_more_button)
            )
        except TimeoutException:
            break  # Break the loop when the "Show More" button is no longer available

    # Find both tables
    tables = driver.find_elements(By.CSS_SELECTOR, 'table.Table')

    # Ensure there are at least two tables
    if len(tables) < 2:
        print("Error: Less than two tables found on the page.")
        driver.quit()
        exit()

    table1 = tables[0]
    table2 = tables[1]
    
    #if defeense is passed in, the headers and logic are slightly different
    if defense:
        # Extract headers from both tables
        headers1 = [th.text.strip() for th in table1.find_elements(By.XPATH, './/tr[2]/th')]
        headers2 = [th.text.strip() for th in table2.find_elements(By.XPATH, './/tr[2]/th')[1:]]  # Skip the first column of table2
        all_headers = headers1 + headers2

        # Extract and combine data
        combined_data = []
        rows1 = table1.find_elements(By.TAG_NAME, 'tr')[2:]  # Skip header row
        rows2 = table2.find_elements(By.TAG_NAME, 'tr')[2:]  # Skip header row
    else:
        # Extract headers for offense only
        headers1 = [th.text.strip() for th in table1.find_elements(By.TAG_NAME, 'th')]
        headers2 = [th.text.strip() for th in table2.find_elements(By.TAG_NAME, 'th')[1:]]  # Skip the first column of table2
        all_headers = headers1 + headers2

        # Extract and combine data for offense only
        combined_data = []
        rows1 = table1.find_elements(By.TAG_NAME, 'tr')[1:]  # Skip header row
        rows2 = table2.find_elements(By.TAG_NAME, 'tr')[1:]  # Skip header row
        

    # Combine data
    for row1, row2 in zip(rows1, rows2):
        player_data1 = [td.text.strip().replace('\n', ' ') for td in row1.find_elements(By.TAG_NAME, 'td')]
        player_data2 = [td.text.strip() for td in row2.find_elements(By.TAG_NAME, 'td')[1:]]  # Skip the first column of table2
        combined_data.append(player_data1 + player_data2)

    # Save combined data to CSV
    with open(f'../data/raw/{file_name}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(all_headers)
        writer.writerows(combined_data)

    print(f"NFL player stats have been saved to '{file_name}.csv'")

    # Close the browser
    driver.quit()