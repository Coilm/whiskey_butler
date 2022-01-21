# Whiskey Butler
![Dev](https://img.shields.io/badge/Developer-Loic%20Musy-blue)
![Python](https://img.shields.io/badge/Python-3.6%2B-informational)

## Your own personal whiskey butler using the power of machine learning

This project was created as the capstone project of the **EPFL Extension School**'s class: **Applied Data Science: Machine Learning**. The goal of the project was to show that the skills teached during the class were correctly assimilated.

The goal of the project is to use a database of reviews from reddit and Natural Language Processing (NLP) to predict whiskeys which are similar to the whiskey entered by the user.

The project is structured in 4 python notebooks:

0. Extracting reviews
1. Data Cleaning and Engineering
2. Exploratory Data Analysis
3. Clustering using unsupervised machine learning
4. Score prediction using supervised machine learning 

## 0. Extracting reviews
The user reviews are regrouped in a csv as a google sheet: [here](https://docs.google.com/spreadsheets/d/1XjgQHckNzC06H9d1IeGeIIbgUqAUfwR601OklPNyNgc/edit#gid=695409533), a copy of it is present on this git.

Then to extract the reviews the package ```requests``` was used in conjonction with the Reddit Api. The script is available as ```extract_reddit.py```. You will need a reddit account and create an app [here](https://www.reddit.com/prefs/apps). Take note of the password_id and client_id. Then create a ```.env``` filled with:
```python
CLIENT_ID = <app client id>
PASSWORD_ID = <app password id>
USERNAME = <reddit username>
PASSWORD = <reddit password>
``` 

replacing the <> as necessary. Once it is done you can run the script.

> :warning: The script is taking long time to run and is putting some load on the Reddit website, please don't abuse it!

## 1. Data Cleaning and Engineering
