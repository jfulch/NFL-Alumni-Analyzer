import pandas as pd

files = [
    'nfl-passing-final.csv',
    'nfl-receiving-final.csv',
    'nfl-rushing-final.csv',
    'nfl-defense-final.csv'
]

# New generic function to count NFL players by any entity (college, conference, etc.)
def count_nfl_players_by_entity(entity):
    
    player_counts = {}
    
    for file in files:
        file_path = f'../data/final/{file}'
        df = pd.read_csv(file_path)
        
        # Iterate over all unique colleges in the current file
        for item in df[entity].unique():
            if pd.notna(item):  # Ensure the college name is not NaN
                if item not in player_counts:
                    player_counts[item] = 0
                
                # Get the number of players that went to the college in the current file
                item_count = len(df[df[entity] == item])
                player_counts[item] += item_count
    
    # Sort the dictionary by the number of players in descending order
    sorted_player_player_counts = dict(sorted(player_counts.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_player_player_counts

# Pass in the entity as 'College' or 'Conference' 
def gets_stats_by_college_or_conf(stat, entity, files=files):
    stats_dict = {}
    
    for file in files:
        file_path = f'../data/final/{file}'
        df = pd.read_csv(file_path)
        
        # Iterate over all unique entities (colleges or conferences) in the current file
        for entity_name in df[entity].unique():
            if pd.notna(entity_name):  # Ensure the entity name is not NaN
                if entity_name not in stats_dict:
                    stats_dict[entity_name] = 0
                
                try:
                    # Get the number of the specified stat by each entity in the current file
                    stat_count = df[df[entity] == entity_name][stat].sum()
                    stats_dict[entity_name] += stat_count
                except KeyError:
                    # If the stat column doesn't exist, skip to the next file
                    continue
    
    # Sort the dictionary by the number of the specified stat in descending order
    sorted_stats_dict = dict(sorted(stats_dict.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_stats_dict

# Pass in either 'College' or 'Conference' to get the position counts by college or conference
def get_position_count_by_entity(entity):
    position_dict = {}
    
    for file in files:
        file_path = f'../data/final/{file}'
        df = pd.read_csv(file_path)
        
        # Iterate over all unique colleges in the current file
        for college in df[entity].unique():
            if pd.notna(college):  # Ensure the college name is not NaN
                if college not in position_dict:
                    position_dict[college] = {}
                
                # Get the number of players by position that went to the college in the current file
                position_counts = df[df[entity] == college]['Position'].value_counts().to_dict()
                
                # Add the position counts to the dictionary
                for position, count in position_counts.items():
                    if position not in position_dict[college]:
                        position_dict[college][position] = 0
                    position_dict[college][position] += count
    
    return position_dict

# Test the functions
# Try Solo tackles by college
# solo_tackes = gets_stats_by_college_or_conf('SOLO', 'College')
# college_solo_tackes = solo_tackes['Alabama']
# print(f'Solo Tackles by Alabama: {college_solo_tackes}')

# # Try Interceptions by conference
# interceptions = gets_stats_by_college_or_conf('INT', 'Conference')
# conference_ints = interceptions['SEC']
# print(f'Interceptions by SEC: {conference_ints}')

# # Try Position by college
# pos_dict = get_position_count_by_entity('Conference')
# print(pos_dict['SEC'])

# # count_nfl_players_by_entity
# print('NFL Players By College -----------')
# print(count_nfl_players_by_entity('College'))
# print('NFL Players By Conference -----------')
# print(count_nfl_players_by_entity('Conference'))