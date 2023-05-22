import itertools

# variables
considerDraw = False
winPoint = 2 #points if won
drawPoint = 1 #points if draw
losePoints = 0 #negative points if lost, enter it as negativei.e -1,-2 etc it will be added to the points table
calculateTop2Nrr = True #check for top 2 qualification by nrr
calculateTop2Points = True #check for top 2 qualification by points alone
calculateTop4Nrr = True #check for top 4 qualification by nrr
calculateTop4Points = True #check for top 4 qualification by points alone


#Teams and Initial Points
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

# Generating all possible outcomes of the remaining matches
if considerDraw:
    possible_outcomes = itertools.product(['team1_wins', 'team2_wins','draw'], repeat=len(remaining_matches))
else:
    possible_outcomes = itertools.product(['team1_wins', 'team2_wins'], repeat=len(remaining_matches))

# Variables to keep track of the teams' chances of finishing in the top 4
team_chances = {"top2nrr":{team: 0 for team in teams},
                "top2points":{team: 0 for team in teams},
                "top4nrr":{team: 0 for team in teams},
                "top4points":{team: 0 for team in teams}}
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
            points[team2] += losePoints
        elif match_outcome == 'team2_wins':
            points[team2] += winPoint
            points[team1] += losePoints
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
    # Adjust ranks for teams with equal points to be the same
    rank_counter = 1
    for i in range(1, len(ranks)):
        if ranks[i]['points'] == ranks[i-1]['points']:
            ranks[i-1]['rank'] = ranks[i]['rank']
            ranks[i]['nrrrank'] = ranks[i-1]['nrrrank']
    for team in teams:
        rank = next(rank_info['rank'] for rank_info in ranks if rank_info['team'] == team)
        nrrRank = next(rank_info['nrrrank'] for rank_info in ranks if rank_info['team'] == team)
        if rank <= 4 and calculateTop4Points:
            team_chances['top4points'][team] += 1 
        if nrrRank <= 4 and calculateTop4Nrr:
            team_chances['top4nrr'][team] += 1
        if rank <= 2 and calculateTop2Points:
            team_chances['top2points'][team] += 1 
        if nrrRank <= 2 and calculateTop2Nrr:
            team_chances['top2nrr'][team] += 1
    total_scenarios += 1

from tabulate import tabulate

# Combine the results from different categories into a single list
combined_results = []
if calculateTop2Points:
    for team, chances in team_chances['top2points'].items():
        probability = chances / total_scenarios
        combined_results.append([team, f"{probability * 100:.2f}%", "", "", ""])
if calculateTop2Nrr:
    for team, chances in team_chances['top2nrr'].items():
        probability = chances / total_scenarios
        existing_team = next((result for result in combined_results if result[0] == team), None)
        if existing_team:
            existing_team[2] = f"{probability * 100:.2f}%"
        else:
            combined_results.append([team, "", f"{probability * 100:.2f}%", "", ""])
if calculateTop4Points:
    for team, chances in team_chances['top4points'].items():
        probability = chances / total_scenarios
        existing_team = next((result for result in combined_results if result[0] == team), None)
        if existing_team:
            existing_team[3] = f"{probability * 100:.2f}%"
        else:
            combined_results.append([team, "", "", f"{probability * 100:.2f}%", ""])
if calculateTop4Nrr:
    for team, chances in team_chances['top4nrr'].items():
        probability = chances / total_scenarios
        existing_team = next((result for result in combined_results if result[0] == team), None)
        if existing_team:
            existing_team[4] = f"{probability * 100:.2f}%"
        else:
            combined_results.append([team, "", "", "", f"{probability * 100:.2f}%"])

# Sort the combined results based on the team name
sorted_results = sorted(combined_results, key=lambda x: (float(x[1].strip("%")), float(x[2].strip("%")), float(x[3].strip("%")), float(x[4].strip("%"))), reverse=True)

# Print the combined results in a table format
headers = ["Team", "Top 2 Points", "Top 2 NRR", "Top 4 Points", "Top 4 NRR"]
print(tabulate(sorted_results, headers=headers, tablefmt="fancy_grid"))