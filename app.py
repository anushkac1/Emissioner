# from flask import Flask, request, jsonify
# import google.generativeai as genai
# from dotenv import load_dotenv
# from flask_cors import CORS
# from fuzzywuzzy import fuzz
# import json
# import os


# load_dotenv()


# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY is not set in the environment.")

# app = Flask(__name__)
# CORS(app)

# genai.configure(api_key=GEMINI_API_KEY)

# with open('gemini/gemini_training_data.json', 'r') as f:
#     training_data = json.load(f)


# valid_inputs = [item['input'] for item in training_data]



# def find_best_match(query):
#     best_match = max(valid_inputs, key=lambda x: fuzz.ratio(x.lower(), query.lower()))
#     similarity_score = fuzz.ratio(best_match.lower(), query.lower())
#     return best_match if similarity_score > 70 else None 



# def get_ai_emission_and_suggestions(food_item):
#     """
#     Query Gemini with the food item to get carbon emission estimates and suggestions.
#     """
#     prompt = f"""
#     The user has entered the food item '{food_item}'.
    
#     Use your training data to:
#     1. Estimate the carbon emissions (in kg CO₂ per kilogram) for '{food_item}'.
#     2. Suggest three alternative food items that are more eco-friendly with lower emissions.
#     Provide the estimates and brief explanations for each alternative.
#     """

#     try:
#         # Query Gemini
#         model = genai.GenerativeModel('gemini-pro')
#         response = model.generate_content(prompt)
#         return response.text  # Return Gemini's response as text
#     except Exception as e:
#         return f"Error with Gemini API: {str(e)}"



# @app.route('/get_emission', methods=['POST'])
# def get_emission():
#     """
#     Flask endpoint to get emissions for a specific food item using predefined training data or Gemini.
#     """
#     # Get food item from the request
#     food_item = request.json.get('food', '').strip().lower()

#     # Check for a direct or fuzzy match in training data
#     best_match = find_best_match(food_item)

#     if best_match:
#         # Find the output for the matched input
#         matched_output = next(
#             (item['output'] for item in training_data if item['input'].lower() == best_match.lower()), None
#         )
#         return jsonify({
#             'food': food_item,
#             'emission': matched_output,
#             'recommendations': None
#         })
#     else:
#         # If no match, fallback to Gemini
#         ai_response = get_ai_emission_and_suggestions(food_item)
#         return jsonify({
#             'food': food_item,
#             'emission': 'Data not available in predefined training data.',
#             'recommendations': ai_response
#         })



# @app.route('/validate_query', methods=['POST'])
# def validate_query():
#     """
#     Check if the user query is valid.
#     """
#     query = request.json.get('query', '').strip().lower()
#     best_match = find_best_match(query)
#     if best_match:
#         return jsonify({
#             'valid': True,
#             'best_match': best_match
#         })
#     else:
#         return jsonify({
#             'valid': False,
#             'message': "Invalid query. Please check your input and try again."
#         }), 400  # Bad request



# if __name__ == "__main__":
#     app.run(host=os.getenv('IP', '0.0.0.0'),
#             port=int(os.getenv('PORT', 4444)))




from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
from fuzzywuzzy import fuzz

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

app = Flask(__name__)
CORS(app)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load training data
with open('gemini/gemini_training_data.json', 'r') as f:
    training_data = json.load(f)

# Extract valid inputs from training data
valid_inputs = [item['input'] for item in training_data]

# Helper function to find the best match for a query
def find_best_match(query):
    best_match = max(valid_inputs, key=lambda x: fuzz.ratio(x.lower(), query.lower()))
    similarity_score = fuzz.ratio(best_match.lower(), query.lower())
    return best_match if similarity_score > 70 else None  # Threshold for fuzzy matching


def query_gemini_for_emission(food_item):
    """
    Query Gemini to estimate carbon emissions for a food item.
    Extract only the carbon emissions value from the response.
    """
    prompt = f"""
    The user has entered the food item '{food_item}'.

    Provide only the carbon emissions value (in kg CO₂ per kilogram) for '{food_item}'.
    Respond in the following format:
    "{food_item} emits approximately X kg CO₂ per kilogram."
    """

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        # Parse the response to extract the emissions value
        lines = response.text.strip().splitlines()
        for line in lines:
            # if "kg CO₂" in line:
            #     return line  # Return the first line containing emissions
            if "kg CO₂" in line:
                # Clean up duplicates or trailing 'kg CO₂'
                return line.replace(" kg CO₂", "", line.count("kg CO₂") - 1).strip()

        # If no valid data is found in the response
        return "No precise CO₂ data found for this item."
    except Exception as e:
        return f"Error with Gemini API: {str(e)}"


# def query_gemini_for_alternatives(food_item):
#     """
#     Query Gemini to provide eco-friendly alternatives for a food item.
#     """
#     prompt = f"""
#     The user has entered the food item '{food_item}'.
#     Suggest three alternative food items that are more eco-friendly with lower emissions.
#     Provide a brief explanation for each alternative.
#     """
#     try:
#         model = genai.GenerativeModel('gemini-pro')
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception as e:
#         return f"Error with Gemini API: {str(e)}"

def query_gemini_for_alternatives(food_item):
    """
    Query Gemini to provide eco-friendly alternatives for a food item.
    Returns a concise response with three alternative food items.
    """
    prompt = f"""
    The user has entered the food item '{food_item}'.
    Suggest three alternative food items that are more eco-friendly with lower emissions.
    Provide just the names of the alternatives in a numbered list format, with each item on a new line.
    """
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-pro')
        
        # Query the Gemini model
        response = model.generate_content(prompt)
        
        # Process the response for better formatting
        raw_text = response.text.strip()
        formatted_items = raw_text.split('\n')  # Split response into individual items
        formatted_items = [item.strip().lstrip("0123456789.- ") for item in formatted_items]  # Clean up numbering or symbols
        
        # Create a properly formatted string
        formatted_response = "\n".join(f"{i+1}. {item}" for i, item in enumerate(formatted_items))
        
        return formatted_response
    except Exception as e:
        return f"Error with Gemini API: {str(e)}"




@app.route('/get_emission', methods=['POST'])
def get_emission():
    """
    Flask endpoint to get emissions for a specific food item using predefined training data or Gemini.
    """
    # Get food item from the request
    food_item = request.json.get('food', '').strip().lower()

    # Check for a direct or fuzzy match in training data
    best_match = find_best_match(food_item)

    if best_match:
        # Find the output for the matched input
        matched_output = next(
            (item['output'] for item in training_data if item['input'].lower() == best_match.lower()), None
        )
        # Always query Gemini for alternatives
        alternatives = query_gemini_for_alternatives(food_item)
        return jsonify({
            'food': food_item,
            'emission': matched_output,
            'recommendations': alternatives
        })
    else:
        # If no match, query Gemini for emissions and alternatives
        emission = query_gemini_for_emission(food_item)
        alternatives = query_gemini_for_alternatives(food_item)
        return jsonify({
            'food': food_item,
            'emission': emission,
            'recommendations': alternatives
        })

@app.route('/validate_query', methods=['POST'])
def validate_query():
    """
    Check if the user query is valid.
    """
    query = request.json.get('query', '').strip().lower()
    best_match = find_best_match(query)
    if best_match:
        return jsonify({
            'valid': True,
            'best_match': best_match
        })
    else:
        return jsonify({
            'valid': False,
            'message': "Invalid query. Please check your input and try again."
        }), 400  # Bad request

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 4444)))


