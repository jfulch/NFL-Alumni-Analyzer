from get_data_processes.get_university_data_footballdb import get_university_data
from get_data_processes.get_university_data_ESPN import get_espn_university_data
from get_data_processes.get_conference_data import get_conference_data
from get_data_processes.get_nfl_data import get_nfl_data
import concurrent.futures
import time

# Master function that calls smallert data fetching functions that can be run concurrently
def fetch_all_data():
    start_time = time.time()  
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(get_university_data),
            executor.submit(get_espn_university_data),
            executor.submit(get_conference_data),
            executor.submit(lambda: get_nfl_data('https://www.espn.com/nfl/stats/player', 'nfl-passing')),
            executor.submit(lambda: get_nfl_data('https://www.espn.com/nfl/stats/player/_/stat/receiving', 'nfl-receiving')),
            executor.submit(lambda: get_nfl_data('https://www.espn.com/nfl/stats/player/_/stat/rushing', 'nfl-rushing')),
            executor.submit(lambda: get_nfl_data('https://www.espn.com/nfl/stats/player/_/view/defense', 'nfl-defense', True))
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")
    
    end_time = time.time()  
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")

# Call the function to fetch all data
fetch_all_data()