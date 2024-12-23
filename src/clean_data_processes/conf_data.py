import pandas as pd
from thefuzz import process

# Adds what conference each player was in, based on the school they went to
def add_conf_data(player_data_file):
    player_data_path = f'../data/processed/{player_data_file}'
    conf_data_path = '../data/raw/schools_conferences.csv'
    
    # Load the csv files into DataFrames
    df = pd.read_csv(player_data_path)
    conf_data = pd.read_csv(conf_data_path)
    
    # Create a dictionary to map college names to their best match in the conference data
    college_name_map = {
        'Brigham Young': 'BYU'  # Hard-coded because the conference data uses 'BYU' instead of 'Brigham Young'
    }
    for college_name in df['College']:
        if pd.notna(college_name):  # Ensure the college_name is not NaN
            college_name = str(college_name)  # Ensure the college_name is a string
            best_match, score, _ = process.extractOne(college_name, conf_data['School'])
            if score >= 80:  # Adjust the threshold as needed
                college_name_map[college_name] = best_match
    
    # Add a new column to df for the matched conference school name
    df['Matched_School'] = df['College'].map(college_name_map)
    
    # Merge the two DataFrames on the matched school names
    combined_data = df.merge(conf_data, left_on='Matched_School', right_on='School', how='left')
    
    # Drop the 'Matched_School' column
    combined_data = combined_data.drop(columns=['Matched_School'])
    
    # Strip the '-clean-combined.csv' extension from the file name
    if player_data_file.endswith('-clean-combined.csv'):
        output_file = player_data_file.replace('-clean-combined.csv', '-final.csv')
    else:
        output_file = player_data_file + '-final.csv'
    
    # Save the combined DataFrame to a new CSV file
    combined_data.to_csv(f'../data/final/{output_file}', index=False)
    
    # Print a success message
    print(f'Combined Data with Conference: {output_file}')