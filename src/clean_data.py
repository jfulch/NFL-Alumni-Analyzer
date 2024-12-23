from clean_data_processes.clean_files import clean_nfl_stats_file
from clean_data_processes.clean_files import clean_college_data
from clean_data_processes.clean_files import clean_espn_college_data
from clean_data_processes.clean_files import clean_schol_conf_data
from clean_data_processes.combine_data import combine_data
from clean_data_processes.conf_data import add_conf_data
from clean_data_processes.get_blank_lines import print_nan_player

# Call the function to clean the NFL data
clean_nfl_stats_file('nfl-passing.csv')
clean_nfl_stats_file('nfl-receiving.csv')
clean_nfl_stats_file('nfl-rushing.csv')
clean_nfl_stats_file('nfl-defense.csv')

# Call the function to clean the college data
clean_college_data()
clean_espn_college_data()
clean_schol_conf_data()

# Call the function to combine data
combine_data('nfl-rushing-clean.csv', 'player_university_data-clean.csv', 'player_university_data_ESPN-clean.csv')
combine_data('nfl-passing-clean.csv', 'player_university_data-clean.csv', 'player_university_data_ESPN-clean.csv')
combine_data('nfl-receiving-clean.csv', 'player_university_data-clean.csv', 'player_university_data_ESPN-clean.csv')
combine_data('nfl-defense-clean.csv', 'player_university_data-clean.csv', 'player_university_data_ESPN-clean.csv')

# Call the function to add conference data
add_conf_data('nfl-rushing-clean-combined.csv')
add_conf_data('nfl-passing-clean-combined.csv')
add_conf_data('nfl-receiving-clean-combined.csv')
add_conf_data('nfl-defense-clean-combined.csv')

# Call the function to print NaN player records
print_nan_player('nfl-rushing-final.csv')
print_nan_player('nfl-passing-final.csv')
print_nan_player('nfl-receiving-final.csv')
print_nan_player('nfl-defense-final.csv')
