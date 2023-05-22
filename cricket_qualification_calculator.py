# Imports
import itertools
from tabulate import tabulate

# Function to calculate probability percentage
def calculate_probability(chances, total_scenarios):
    return f"{(chances / total_scenarios) * 100:.2f}%"

# Function to combine results for table structure
def update_combined_results(combined_results, team, chances, index,total_scenarios):
    probability = calculate_probability(chances, total_scenarios)
    existing_team = next((result for result in combined_results if result[0] == team), None)
    if existing_team:
        existing_team[index] = probability
    else:
        new_team = ["" for _ in range(5)]
        new_team[0] = team
        new_team[index] = probability
        combined_results.append(new_team)

# Function to simulate outcome
def simnulate_outcomes(teams, initial_points, remaining_matches, considerDraw, winPoint=2, drawPoint=1, losePoint=0):
    # Generating all possible outcomes of the remaining matches
    if considerDraw:
        possible_outcomes = itertools.product(
            ['team1_wins', 'team2_wins', 'draw'], repeat=len(remaining_matches))
    else:
        possible_outcomes = itertools.product(
            ['team1_wins', 'team2_wins'], repeat=len(remaining_matches))

    # Variables to keep track of the teams' chances of finishing in the top 4
    team_chances = {"top2nrr": {team: 0 for team in teams},
                    "top2points": {team: 0 for team in teams},
                    "top4nrr": {team: 0 for team in teams},
                    "top4points": {team: 0 for team in teams}
                    }
    total_scenarios = 0
    # Simulate all possible outcomes
    for outcome in possible_outcomes:
        # Reset the points for each team
        points = initial_points.copy()

        # Simulate the outcomes of the remaining matches based on the current scenario
        for i, match in enumerate(remaining_matches):
            match_outcome = outcome[i]
            team1 = match['team1']
            team2 = match['team2']
            if match_outcome == 'team1_wins':
                points[team1] += winPoint
                points[team2] += losePoint
            elif match_outcome == 'team2_wins':
                points[team2] += winPoint
                points[team1] += losePoint
            else:
                points[team1] += drawPoint
                points[team2] += drawPoint

        # Determine the ranks based on points
        sorted_teams = sorted(points, key=lambda x: points[x], reverse=True)
        ranks = []
        current_rank = 1
        for team in sorted_teams:
            rank_info = {
                'team': team,
                'points': points[team],
                'rank': current_rank,
                'nrrrank': current_rank
            }
            ranks.append(rank_info)
            current_rank += 1
        # Adjust ranks for teams with equal points to be the same for nrr and points too
        rank_counter = 1
        for i in range(1, len(ranks)):
            if ranks[i]['points'] == ranks[i-1]['points']:
                ranks[i]['nrrrank'] = ranks[i-1]['nrrrank']
        for i in range(len(ranks)-1,0,-1):
            if ranks[i]['points'] == ranks[i-1]['points']:
                ranks[i-1]['rank'] = ranks[i]['rank']
        # calculating and adding in scenarios where teams get qualified
        for team in teams:
            rank = next(rank_info['rank']
                        for rank_info in ranks if rank_info['team'] == team)
            nrrRank = next(rank_info['nrrrank']
                           for rank_info in ranks if rank_info['team'] == team)
            if rank <= 4:
                team_chances['top4points'][team] += 1
            if nrrRank <= 4:
                team_chances['top4nrr'][team] += 1
            if rank <= 2:
                team_chances['top2points'][team] += 1
            if nrrRank <= 2:
                team_chances['top2nrr'][team] += 1
        total_scenarios += 1
    # Combine the results from different categories into a single list
    combined_results = []
    categories = ['top2points', 'top2nrr', 'top4points', 'top4nrr']

    index = 0
    for category in categories:
        index += 1
        for team, chances in team_chances[category].items():
            update_combined_results(combined_results, team, chances, index,total_scenarios)
    # Sort the combined results based on the team name
    # sorting results from col 2 to 4 while striping percent
    sorted_results = sorted(combined_results, key=lambda x: (float(x[1].strip("%")), float(
        x[2].strip("%")), float(x[3].strip("%")), float(x[4].strip("%"))), reverse=True)

    # Print the combined results in a table format
    headers = ["Team", "Top 2 Points",
               "Top 2 NRR", "Top 4 Points", "Top 4 NRR"]
    print(tabulate(sorted_results, headers=headers, tablefmt="fancy_grid"))

# Teams and Initial Points
teams = [
    'Chennai Super Kings', 'Delhi Capitals', 'Kolkata Knight Riders', 'Lucknow Super Giants',
    'Mumbai Indians', 'Sunrisers Hyderabad', 'Royal Challengers Bangalore', 'Gujarat Titans', 'Punjab Kings',
    'Rajasthan Royals',
]
initial_points = {
    'Chennai Super Kings': 15,
    'Delhi Capitals': 10,
    'Gujarat Titans': 18,
    'Kolkata Knight Riders': 12,
    'Mumbai Indians': 14,
    'Lucknow Super Giants': 15,
    'Punjab Kings': 12,
    'Rajasthan Royals': 14,
    'Royal Challengers Bangalore': 14,
    'Sunrisers Hyderabad': 8
}

# Remaining matches with format
# {'team1': 'Team A', 'team2': 'Team 2', 'match_number': 0}
remaining_matches = [
    {'team1': 'Delhi Capitals',
        'team2': 'Chennai Super Kings', 'match_number': 67},
    {'team1': 'Kolkata Knight Riders',
        'team2': 'Lucknow Super Giants', 'match_number': 68},
    {'team1': 'Mumbai Indians', 'team2': 'Sunrisers Hyderabad', 'match_number': 69},
    {'team1': 'Royal Challengers Bangalore',
        'team2': 'Gujarat Titans', 'match_number': 70}
]

simnulate_outcomes(teams, initial_points, remaining_matches, considerDraw=False, winPoint=2, drawPoint=1, losePoint=0)
