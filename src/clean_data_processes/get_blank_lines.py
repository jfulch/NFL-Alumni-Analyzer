import pandas as pd

# Loop through all of the with-conconference files and print out all records that have a NaN value in the 'Player' column
def print_nan_player(file):
    file_path = f'../data/final/{file}'
    df = pd.read_csv(file_path)
    
    # Strip the last .csv extension from the file name
    output_file = file.rstrip('.csv') + '-nan-player-file.csv'
    
    # Save the NaN player records to a new CSV file
    df[df['Player'].isna()].to_csv(f'../data/testing/{output_file}', index=False)
    
    # Print a success message
    print(f'Printed NaN Players in: {file}-nan-players.csv')