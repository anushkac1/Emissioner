# Emissioner
An app to help individuals track their carbon emissions footprint via the food choices they make. 

# Features

* Carbon footprint calculator that processes user input data to generate emissions measurements 
* Smart recommendation system that suggests personalized alternatives for reducing environmental impact based on user habits.
* History tracking system that maintains a record of all previous calculations and results for user reference. 
* User authentication and authorization
* Interactive community platform where users can create and share posts about their environmental journey


# Getting Started
1. Clone the repository
   
   ```git clone https://github.com/anushkac1/Emissioner.git```
2. Go into the respository

   ```cd Emissioner```
3. Install dependencies (Node.js) - please note, you may be prompted to download several dependencies such as axios in addition to this!

   ```npm install```

4. Create .env file
5. Input the following into the .env file (located outside of all folders) and create a Gemini API Key from https://aistudio.google.com/apikey
   ```
   .gitignore
   GEMINI_API_KEY='your-gemini-key-here'
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_secret_key

6. Run the application using the following command (sets to default port 5000):
   
   ```python app.py``` or ```python3 app.py```
7. To run the frontend, change directory into the frontend folder and run

   ```cd frontend```
   
   ```npm run start```

8. To exit the application, use Ctrl+C in the terminal and re-enter via the python app.py command.

# Potential Errors
1. Might face issues with your version of react and eslintConfig. Here are some potential ways to troubleshoot it. 
   * We recommend uninstalling and reinstalling node modules if the error persists
   * Check what versions you have
   * Is your ESLint compatible with your react version?
   * Update dependencies
   * Clear your cache 
   * Might need to include a ```root:true``` under your package.json extensions OR remove it(see below)
   * Ensure package.json includes
    ```
    "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
     },
    
2. Generating gemini_training_data.json requires you to move the python generation file outside of the Gemini folder first.
   Note this is already generated so there is no need to rerun this file. 
     


# Credits
Canvas - https://www.canva.com

Uiverse - https://uiverse.io

# Authors
Anushka Chokshi

Amrit Randev

Aditi Jorapur 

Sanjana Jagarlapudi

