"""
This file generates gemini_training_data.json that is used within our gemini api (within app.py) to train the model
via few shot and zero shot prompting. 

Note: in order to generate the json file you should move this file outside of any folder (to overall project directory) 
and run python3 generate_training_data.py and the json file will be populated within gemini folder. This is a step
that has already been done!
"""


#import statements for pandas and json
import pandas as pd
import json

# get the path for both data files
greenhouse_gas_path = 'backend/venv/data/greenhouse-gas-emissions-per-kilogram-of-food-product.csv'
food_production_path = 'backend/venv/data/Food_Production.csv'

#read in the files using pandas read 
greenhouse_gas = pd.read_csv(greenhouse_gas_path)
food_production = pd.read_csv(food_production_path)

# format the training data - empty list
def generate_training_data():
    training_data = []

    # go through every row of first dataset and populate the training data list
    for _, row in greenhouse_gas.iterrows():
        #check for food and emission in dataset
        food = row['Entity']
        emission = row['GHG emissions per kilogram (Poore & Nemecek, 2018)']
        #test several different prompts to acocunt for different ways people could enter their prompts!
        training_data.append({
            "input": f"What is the carbon emission for {food.lower()}?",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": food.lower(),
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"{food.lower()} carbon emission?",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"{food.lower()} carbon emission",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"Tell me about {food.lower()} carbon emissions",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"Tell me about {food.lower()} emissions",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"Tell me about {food.lower()} carbon",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"How sustainable is {food.lower()}?",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"Environmental data on {food.lower()}?",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"{food.lower()} emissions",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"{food.lower()} footprint",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"{food.lower()} sustainability",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"{food.lower()} environment",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"emissions {food.lower()}",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"footprint{food.lower()}",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"sustainability{food.lower()}",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"impact{food.lower()}",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
            "input": f"{food.lower()} CO2",
            "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })

        training_data.append({
                "input": f"Is {food.lower()} eco friendly?",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
        })



        
    # go through every row of food production dataset and populate the training data list
    for _, row in food_production.iterrows():
        #again, get food and emission from data
        food = row['Food product']
        emission = row['Total_emissions']
        #as long as you find emission, add it to list 
        #test different variations in case of unique prompting by user
        if pd.notna(emission):  
            training_data.append({
                "input": f"What is the carbon emission for {food.lower()}?",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"What is the carbon emission for {food.lower()}?",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": food.lower(),
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"{food.lower()} carbon emission?",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"{food.lower()} carbon emission",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"Tell me about {food.lower()} carbon emissions",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"Tell me about {food.lower()} emissions",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"Tell me about {food.lower()} carbon",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"How sustainable is {food.lower()}?",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"Environmental data on {food.lower()}?",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"{food.lower()} emissions",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"{food.lower()} footprint",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"{food.lower()} sustainability",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"{food.lower()} environment",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"emissions {food.lower()}",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"footprint{food.lower()}",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"sustainability{food.lower()}",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"impact{food.lower()}",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"{food.lower()} CO2",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })

            training_data.append({
                "input": f"Is {food.lower()} eco friendly?",
                "output": f"{food} emits {emission} kg CO₂ per kilogram."
            })



    # account for some other things a user could type in (to respond accordingly, train gemini)
    training_data.append({
        "input": "What are eco-friendly food options",
        "output": "Please enter the food you are trying to find sustainable options for, and we will suggest alternatives!"
    })

    training_data.append({
        "input": "What are the most sustainable foods?",
        "output": "We only let you know how sustainable your foods are/offer alternatives. To look for eco friendly options, check out our community page where users have posted their low emission items!"
    })

    training_data.append({
        "input": "Which foods have lowest carbon foodprint?",
        "output": "We only let you know how sustainable your foods are/offer alternatives. To look for eco friendly options, check out our community page where users have posted their low emission items!"
    })

    training_data.append({
        "input": "How can I eat more sustainabile?",
        "output": "We only let you know how sustainable your foods are/offer alternatives. To look for eco friendly options, check out our community page where users have posted their low emission items & try your best to check your emissions!"
    })


    return training_data


# now generate and save training data in the json file under gemini folder
training_data = generate_training_data()
with open('gemini/gemini_training_data.json', 'w') as f:
    json.dump(training_data, f, indent=4)

#print statement to see code part is complete 
print("Training data saved to gemini_training_data.json!")