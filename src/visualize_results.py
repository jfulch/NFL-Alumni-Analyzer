import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px
import webbrowser
import os
from analyze_data import count_nfl_players_by_entity
from analyze_data import gets_stats_by_college_or_conf
from analyze_data import get_position_count_by_entity

# Define colors for the bars
colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

# entity is the entity you want to look up ex: 'Conference' or 'College'
def plot_nfl_player_count_by_entity_bar(entity):
    num_players_by_entity = count_nfl_players_by_entity(entity)
    
    # Sort the dictionary to get the top 10 colleges or conferences
    top_10_entities = dict(sorted(num_players_by_entity.items(), key=lambda item: item[1], reverse=True)[:10])
    
    # Plot the results using matplotlib.pyplot
    plt.figure(figsize=(12, 8))
    bars = plt.bar(top_10_entities.keys(), top_10_entities.values(), color=colors)
    plt.xlabel(entity)
    plt.ylabel('Number of NFL Players')
    plt.title(f'Top 10 {entity}s by Number of Current NFL Players')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Add the value for each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom')  # va: vertical alignment
    
    # Save the figure
    output_file = f'top_10_{entity.lower()}_nfl_players.png'
    plt.savefig(f'../results/images/{output_file}')

    print(f'Graph saved to {output_file}')
    # Close the figure
    plt.close()

# entity is the entity you want to look up ex: 'Conference' or 'College'
def plot_position_count_by_entity_heatmap(entity):
    num_players_by_entity = count_nfl_players_by_entity(entity)
    top_10_entities = dict(sorted(num_players_by_entity.items(), key=lambda item: item[1], reverse=True)[:15])
    
    position_count_by_entity = get_position_count_by_entity(entity)
    
    # Filter the position count dictionary to only include the top 10 entities
    filtered_position_count = {k: position_count_by_entity[k] for k in top_10_entities.keys() if k in position_count_by_entity}
    
    # Create a DataFrame from the filtered dictionary
    df = pd.DataFrame(filtered_position_count)
    df = df.fillna(0)
    df = df.astype(int)
    
    # Sort the positions based on the total number of players in each position
    position_totals = df.sum(axis=1).sort_values(ascending=False)
    df = df.loc[position_totals.index]
    
    # Update y-tick labels to include the total number of NFL players
    ytick_labels = [f'{entity_name} ({num_players_by_entity[entity_name]})' for entity_name in df.columns]
    
    # Calculate the y-tick positions to be in the middle of each row
    ytick_positions = [i + 0.5 for i in range(len(df.columns))]
    
    # Plot the results using seaborn
    plt.figure(figsize=(20, 10))
    sns.heatmap(df.T, cmap='coolwarm', annot=True, fmt='d')  # Transpose the DataFrame and add annotations
    plt.xlabel('Position')
    plt.ylabel(entity)
    plt.title(f'Number of Players by Position for Top 15 {entity}')
    plt.yticks(ticks=ytick_positions, labels=ytick_labels, rotation=0)
    plt.tight_layout()
    
    # Save the figure
    output_file = f'position_count_by_{entity.lower()}_heatmap.png'
    plt.savefig(f'../results/images/{output_file}')
    
    print(f'Graph saved to {output_file}')
    # Close the figure
    plt.close()

# stat is the single stat you want to look up ex: 'TD'
# entity is the entity you want to look up ex: 'Conference' or 'College'
def plot_total_stats_by_entity_pie(stat, entity):
    # Get the stat by entity
    stat_by_entity = gets_stats_by_college_or_conf(stat, entity)
    
    # Convert the dictionary to a DataFrame for easier plotting
    df = pd.DataFrame(list(stat_by_entity.items()), columns=[entity, stat])
    
    # Sort the DataFrame by the stat in descending order and get the top 10 entities
    df = df.sort_values(by=stat, ascending=False).head(10)
    
    # Define a function to format the labels
    def func(pct, allvals):
        absolute = int(pct/100.*sum(allvals))
        return f"{pct:.1f}%\n({absolute:d})"
    
    # Plot the results using matplotlib
    plt.figure(figsize=(12, 8))
    plt.pie(df[stat], labels=df[entity], autopct=lambda pct: func(pct, df[stat]), startangle=140, colors=colors[:len(df)])
    plt.title(f'Distribution of Total NFL {stat} by Top 10 {entity}')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()
    
    # Adjust the layout to give more space at the top
    plt.subplots_adjust(top=0.85)
    
    # Save the figure
    output_file = f'total_{stat}_by_{entity}_pie.png'
    plt.savefig(f'../results/images/{output_file}')
    
    print(f'Graph saved to {output_file}')
    # Close the figure
    plt.close()

# stats is a list of stats you want to look up ex: ['SOLO', 'AST', 'YDS', 'SACK']
# entity is the entity you want to look up ex: 'Conference' or 'College'
# file is a list of files you want to look up ex: ['nfl-defense-final.csv']
# file_name is the name of the file you want to look up ex: 'Defense'
def plot_total_stats_by_entity_bar(stats, entity, file=None, file_name=None):
    # Create a DataFrame to hold all the stats
    data = {}
    for stat in stats:
        stat_by_entity = gets_stats_by_college_or_conf(stat, entity, file)
        data[stat] = stat_by_entity
    
    # Convert the dictionary to a DataFrame for easier plotting
    df = pd.DataFrame(data)
    df[entity] = df.index
    df['Total'] = df[stats].sum(axis=1)
    df = df.sort_values(by='Total', ascending=False).head(10)
    df_melted = df.melt(id_vars=[entity], value_vars=stats, var_name='Stat', value_name='Value')
    
    # Plot the results using seaborn
    plt.figure(figsize=(20, 10))
    ax = sns.barplot(x='Value', y=entity, hue='Stat', data=df_melted, palette='viridis')
    plt.xlabel('Total Value')
    plt.ylabel(entity)
    plt.title(f'Top 10 {file_name} Stats by Total NFL Stats')
    plt.tight_layout()
    
    # Add the total number of each stat to the end of each bar
    for p in ax.patches:
        width = p.get_width()
        plt.text(width + 1, p.get_y() + p.get_height() / 2, f'{int(width)}', ha='center', va='center')
    
    # Save the figure
    output_file = f'total_{file_name}_stats_by_{entity}_bar.png'
    plt.savefig(f'../results/images/{output_file}')
    
    print(f'Graph saved to {output_file}')
    # Close the figure
    plt.close()

# stats is a list of variables to plot [x, y, size]
# file is a list of files to plot
# type is a string to specify the type of plot
def plot_performance_by_college(files, stats, type):
    data_frames = [pd.read_csv(f'../data/final/{file}') for file in files]
    offense_data = pd.concat(data_frames)
    
    # Aggregate data by college
    summary = offense_data.groupby("College").agg({
        stats[0]: "sum",
        stats[1]: "sum",
        "Player": "count"
    }).reset_index()
    
    # Add conference for color coding (optional)
    summary = summary.merge(offense_data[["College", "Conference"]].drop_duplicates(), on="College")
    
    # Calculate the number of players for each conference
    conference_player_counts = summary.groupby("Conference")["Player"].sum().reset_index()
    conference_player_counts['Conference (Players)'] = conference_player_counts.apply(lambda row: f"{row['Conference']} ({row['Player']})", axis=1)
    
    # Merge the conference player counts back into the summary DataFrame
    summary = summary.merge(conference_player_counts[['Conference', 'Conference (Players)']], on="Conference")
    
    # Sort the DataFrame by the number of players in descending order
    summary = summary.sort_values(by="Player", ascending=False)
    
    # Create a list of conferences sorted by the number of players
    sorted_conferences = conference_player_counts.sort_values(by="Player", ascending=False)['Conference (Players)'].tolist()
    
    # Create scatter plot
    plt = px.scatter(
        summary,
        x=stats[0],
        y=stats[1],
        size="Player",
        color="Conference (Players)",
        hover_name="College",
        title=f"{type} Performance by College",
        labels={stats[0]: f"Total {stats[0]}", stats[1]: f"Total {stats[1]}"},
        category_orders={"Conference (Players)": sorted_conferences}  # Sort the legend by the number of players
    )
    
    # Save the plot as an HTML file
    output_file = f'../results/interactive/{type}_performance_by_college.html'
    plt.write_html(output_file)
    
    print(f'Scatter plot saved to {output_file}')
    
    # Open the HTML file in the default web browser
    webbrowser.open(f'file://{os.path.realpath(output_file)}', new=2)

# Create the Scatter plot
plot_performance_by_college(['nfl-defense-final.csv'], ['SOLO', 'SACK'], 'Defensive')
plot_performance_by_college(['nfl-rushing-final.csv', 'nfl-receiving-final.csv', 'nfl-passing-final.csv'], ['YDS', 'TD'], 'Offensive')

# Plot the number of NFL players by college and conference
plot_position_count_by_entity_heatmap('Conference')
plot_position_count_by_entity_heatmap('College')
plot_nfl_player_count_by_entity_bar('Conference')
plot_nfl_player_count_by_entity_bar('College')
plot_total_stats_by_entity_pie('TD', 'Conference')
plot_total_stats_by_entity_pie('TD', 'College')
plot_total_stats_by_entity_pie('SACK', 'Conference')
plot_total_stats_by_entity_pie('SACK', 'College')

#For Only defense stats
plot_total_stats_by_entity_bar(['SOLO', 'AST', 'YDS', 'SACK'], 'Conference', ['nfl-defense-final.csv'], "Defense")
plot_total_stats_by_entity_bar(['SOLO', 'AST', 'YDS', 'SACK'], 'College', ['nfl-defense-final.csv'], "Defense")

#For Only passing stats
plot_total_stats_by_entity_bar(['CMP', 'TD'], 'Conference', ['nfl-passing-final.csv'], "Passing")
plot_total_stats_by_entity_bar(['CMP', 'TD'], 'College', ['nfl-passing-final.csv'], "Passing")

#For Only rushing stats
plot_total_stats_by_entity_bar(['TD','BIG', 'LNG'], 'Conference', ['nfl-rushing-final.csv'], "Rushing")
plot_total_stats_by_entity_bar(['TD','BIG', 'LNG'], 'College', ['nfl-rushing-final.csv'], "Rushing")

#For Only receiving stats
plot_total_stats_by_entity_bar(['REC', 'AVG', 'TD'], 'Conference', ['nfl-receiving-final.csv'], "Receiving")
plot_total_stats_by_entity_bar(['REC', 'AVG', 'TD'], 'College', ['nfl-receiving-final.csv'], "Receiving")