from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

#Load the CSV file
data_path = 'backend/venv/data/greenhouse-gas-emissions-per-kilogram-of-food-product.csv'
emission_data = pd.read_csv(data_path)

#Endpoint to get emissions for a specific food item
@app.route('/get_emission', methods=['POST'])
def get_emission():
    #Get food item from request
    food_item = request.json.get('food', '').strip().lower()
    
    #Search for the food item in the CSV data
    matching_data = emission_data[emission_data['Entity'].str.lower() == food_item]
    
    if not matching_data.empty:
        #If found, get the emission value
        emission_value = matching_data.iloc[0]['GHG emissions per kilogram (Poore & Nemecek, 2018)'] 
        response = {
            'food': food_item,
            'emission': emission_value
        }
    else:
        #If not found, return an error message
        response = {
            'error': f"No emission data found for '{food_item}'. Please check your input."
        }
    
    return jsonify(response)

if __name__=="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))

