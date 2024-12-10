import pandas as pd
import json

# datasets 
greenhouse_gas_path = 'backend/venv/data/greenhouse-gas-emissions-per-kilogram-of-food-product.csv'
food_production_path = 'backend/venv/data/Food_Production.csv'

#read the files
greenhouse_gas = pd.read_csv(greenhouse_gas_path)
food_production = pd.read_csv(food_production_path)

# Function to format training data
def generate_training_data():
    training_data = []

    # Add data from greenhouse_gas
    for _, row in greenhouse_gas.iterrows():
        food = row['Entity']
        emission = row['GHG emissions per kilogram (Poore & Nemecek, 2018)']
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



        
    # Add data from food_production
    for _, row in food_production.iterrows():
        food = row['Food product']
        emission = row['Total_emissions']
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



    # Add generic queries in case user does not follow prompting 
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


# Generate and save training data
training_data = generate_training_data()
with open('gemini/gemini_training_data.json', 'w') as f:
    json.dump(training_data, f, indent=4)

print("Training data saved to gemini_training_data.json!")