# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit
from apps.config import config_dict
from apps import create_app, db
from flask import Flask, render_template, request, jsonify
import openai
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

app = Flask(__name__)

# OpenAI API Key
openai.api_key = ""
try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
    
if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)             )
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT = ' + app_config.ASSETS_ROOT )

@app.route("/", methods=["GET", "POST"])
def chat():
    chat_response = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = openai.Completion.create(
            engine="davinci",  # Or any other appropriate engine
            prompt=user_input,
            max_tokens=50  # Adjust as needed
        )
        chat_response = response.choices[0].text.strip()
        print(chat_response)
    return render_template("home/generative.html", user_input=user_input, chat_response=chat_response)


@app.route("/", methods=["GET"])
def regression():
    pd.options.display.max_rows = 9999
    df = pd.read_csv('finaldata.csv')
    df["Hardest.Hit.Area..HHA."] = df["Hardest.Hit.Area..HHA."].astype('category')
    df2 = df[["Total.Score","Hardest.Hit.Area..HHA.","Low.Income.Area..LIA..Census.Tract...Score","Rural","HHA.Score","Tribal.Community.Score..Geographic.Only."]]
    X = np.array([
        df2["Low.Income.Area..LIA..Census.Tract...Score"],
        df2["Rural"],
        df2["HHA.Score"],
        df2["Tribal.Community.Score..Geographic.Only."]
    ]).T
    y = np.array(df2["Total.Score"])
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    # Initialize and fit linear regression model
    model = LinearRegression()
    model.fit(X_scaled, y)
    print("Coefficients:", model.coef_)
    print("Intercept:", model.intercept_)
    # Predictions
    data = {
        "Low.Income.Area..LIA..Census.Tract...Score": [0.5, 1.2, 0.8],
        "Rural": [1, 0, 1],   # Maybe 1 indicates Rural and 0 indicates Not Rural
        "HHA.Score": [0.9, 0.4, 0.7],
        "Tribal.Community.Score..Geographic.Only.": [0.2, 0.5, 0.1]
    }
    new_data = pd.DataFrame(data)
    new_data_array = np.array([
        new_data["Low.Income.Area..LIA..Census.Tract...Score"],
        new_data["Rural"],
        new_data["HHA.Score"],
        new_data["Tribal.Community.Score..Geographic.Only."]
    ]).T
    # Scale the new data using the same scaler
    new_data_scaled = scaler.transform(new_data_array)
    # Make predictions on the new data
    new_predictions = model.predict(new_data_scaled)
    # You can add the predictions back to the new data dataframe if you want
    new_data["Predicted_Total_Score"] = new_predictions
    print(new_data)
    return render_template("home/generative.html", regression_response=new_data)


if __name__ == "__main__":
    app.run(debug=True)