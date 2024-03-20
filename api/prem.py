import pandas as pd
from flask import Blueprint, jsonify

# Create Blueprint for Prem API
prem_api = Blueprint('prem_api', __name__, url_prefix='/api/prem')

# Load the Premier League match dataset
match_data = pd.read_csv('path_to_prem_dataset.csv')  # Update path to your Premier League match dataset

# Define Prem API routes

# Route to get general information about the Premier League
@prem_api.route('/info', methods=['GET'])
def get_prem_info():
    prem_info = {
        'league': 'Premier League',
        'country': 'England',
        'season': '2021-2022',
        'teams': ['Arsenal', 'Chelsea', 'Liverpool', 'Manchester United', 'Manchester City', 'Tottenham Hotspur', 'Leicester City', 'West Ham United', 'Everton', 'Leeds United', 'Aston Villa', 'Wolverhampton Wanderers', 'Southampton', 'Crystal Palace', 'Newcastle United', 'Brighton & Hove Albion', 'Burnley', 'Fulham', 'West Bromwich Albion', 'Sheffield United']
    }
    return jsonify(prem_info)

# Route to get match information for a specific match
@prem_api.route('/matches/<int:match_id>', methods=['GET'])
def get_match_info(match_id):
    match_info = match_data.loc[match_data['MatchID'] == match_id].to_dict(orient='records')
    if not match_info:
        return jsonify({'error': 'Match not found'}), 404
    return jsonify(match_info[0])

# Route to get match information for all matches
@prem_api.route('/matches', methods=['GET'])
def get_all_matches_info():
    all_matches_info = match_data.to_dict(orient='records')
    return jsonify(all_matches_info)

# Add more routes and functionality as needed

