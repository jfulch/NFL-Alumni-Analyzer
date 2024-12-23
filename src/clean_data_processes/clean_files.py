import pandas as pd

def clean_nfl_stats_file(file):
    file_path = f'../data/raw/{file}'
    df = pd.read_csv(file_path)

    # Split the 'NAME' column into 'PLR_NAME' and 'TEAM' using the last space as the delimiter
    df[['PLR_NAME', 'TEAM']] = df['NAME'].str.rsplit(' ', n=1, expand=True)

    # Drop the original 'name' column
    df = df.drop(columns=['NAME'])

    # Clean the 'YDS' column by removing commas and converting to integers
    if 'YDS' in df.columns:
        df['YDS'] = df['YDS'].astype(str).str.replace(',', '').astype(int)

    # Reorder columns if necessary
    df = df[['PLR_NAME', 'TEAM'] + [col for col in df.columns if col not in ['PLR_NAME', 'TEAM']]]

    # Strip the last .csv extension from the file name
    file = file.rstrip('.csv') + '-clean.csv'
    
    # Save the modified DataFrame back to a CSV file
    df.to_csv(f'../data/processed/{file}', index=False)
    
    # Print a success message
    print(f'Cleaned Up Name in: {file}')
    

# Loop through all the values in player_university_data.csv and fix the player names
def clean_college_data():
    file_path = '../data/raw/player_university_data.csv'
    df = pd.read_csv(file_path)
    
    # Remove the " from the Player column and reverse the first and last name
    df['Player'] = df['Player'].str.replace('"', '').str.split(', ').str[::-1].str.join(' ')
    
    # Save the modified DataFrame back to a new CSV file
    df.to_csv('../data/processed/player_university_data-clean.csv', index=False)
    
    # Print a success message
    print('Cleaned Up Player Names in: player_university_data-clean.csv')
    
# Clean the ESPN data to match other college data format
def clean_espn_college_data():
    file_path = '../data/raw/player_university_data_ESPN.csv'
    df = pd.read_csv(file_path)
    
    # Rename 'University' to 'College'
    df = df.rename(columns={'University': 'College'})
    
    # Ensure the headers are in the correct format
    df = df[['Player', 'Position', 'Team', 'College']]
    
    # Save the modified DataFrame back to a new CSV file
    df.to_csv('../data/processed/player_university_data_ESPN-clean.csv', index=False)
    
    # Print a success message
    print('Cleaned Up ESPN College Data in: player_university_data_ESPN-clean.csv')
    
def clean_schol_conf_data():
    file_path = '../data/raw/schools_conferences.csv'
    df = pd.read_csv(file_path)
    
    # Change all instances of 'Ohio St. to 'Ohio State'
    df['School'] = df['School'].str.replace('Ohio St.', 'Ohio State')
    
    # Save the modified DataFrame back to a new CSV file
    df.to_csv('../data/raw/schools_conferences.csv', index=False)