import pandas as pd
from thefuzz import process

position_mapping = {
    'Defensive Tackle': 'DT',
    'Quarterback': 'QB',
    'Running Back': 'RB',
    'Wide Receiver': 'WR',
    'Tight End': 'TE',
    'Offensive Tackle': 'OT',
    'Offensive Guard': 'OG',
    'Center': 'C',
    'Defensive End': 'DE',
    'Linebacker': 'LB',
    'Cornerback': 'CB',
    'Safety': 'S',
    'Kicker': 'K',
    'Punter': 'P',
    'Long Snapper': 'LS'
}

def combine_data(player_data_file, player_university_file, espn_university_file):
    player_data_path = f'../data/processed/{player_data_file}'
    university_data_path = f'../data/processed/{player_university_file}'
    espn_university_data_path = f'../data/processed/{espn_university_file}'
    
    # Load the csv files into DataFrames
    player_data = pd.read_csv(player_data_path)
    university_data = pd.read_csv(university_data_path)
    espn_university_data = pd.read_csv(espn_university_data_path)
    
    # Using Fuzzy String Matching to find the best match because the two websites use different naming conventions
    # and sometimes the names are slightly different
    # Create a dictionary to map player names to their best match in the university data
    player_name_map = {
        'Tutu Atwell':'Chatarius Atwell', # Hard-coded because the name is different on the university site
    }
    for player_name in player_data['PLR_NAME']:
        best_match, score, _ = process.extractOne(player_name, university_data['Player'])
        if score >= 80:  # Adjust the threshold as needed
            player_name_map[player_name] = best_match
        else:
            # If no match is found in university_data, check in espn_university_data
            best_match, score, _ = process.extractOne(player_name, espn_university_data['Player'])
            if score >= 80:  # Adjust the threshold as needed
                player_name_map[player_name] = best_match
    
    # Add a new column to player_data for the matched university player name
    player_data['Matched_Player'] = player_data['PLR_NAME'].map(player_name_map)
    
    # Merge the two DataFrames on the matched player names
    combined_data = player_data.merge(university_data, left_on='Matched_Player', right_on='Player', how='left')
    
    # Merge with espn_university_data if there are any NaN values in the merged columns
    combined_data = combined_data.combine_first(
        player_data.merge(espn_university_data, left_on='Matched_Player', right_on='Player', how='left')
    )
    
    # Drop the 'Matched_Player' column
    combined_data = combined_data.drop(columns=['Matched_Player'])
    
    # Rename 'TEAM' to 'Team ABR'
    combined_data = combined_data.rename(columns={'TEAM': 'Team ABR'})
    
    # Ensure 'PLR_NAME', 'Player', 'Team ABR', and 'Team' are the first four columns
    columns_order = ['PLR_NAME', 'Player', 'Team ABR', 'Team'] + [col for col in combined_data.columns if col not in ['PLR_NAME', 'Player', 'Team ABR', 'Team']]
    combined_data = combined_data[columns_order]
    
    # Apply the position mapping to the Position column
    combined_data['Position'] = combined_data['Position'].map(position_mapping).fillna(combined_data['Position'])
    
    # Strip the last .csv extension from the file name
    output_file = player_data_file.rstrip('.csv') + '-combined.csv'
    
    # Save the combined DataFrame to a new CSV file
    combined_data.to_csv(f'../data/processed/{output_file}', index=False)
    
    # Print a success message
    print(f'Combined Data: {output_file}')