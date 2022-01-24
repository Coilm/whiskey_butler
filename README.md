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

Now that the reviews are extracted we need to convert them in something that can be feed in the rest of the model. To do so, the text was Lemmatized. Two lemmatization methods: WordNet and SpaCy. After inspection, SpaCy seemed to perform a better job at lemmatizing the reviews. A list of stop words was recursivly generated during Exploratory Data Analysis to remove words that don't add supplementary informations (like very common words from the english language).

Not that we have the transformed the reviews into lists of lemmatized words, it was necessary to find a numerical value for them. The technique chosen was TF-IDF. Which basically give a score to the importance of the word in the text.

We also one-hot encoded the style and the users. With this transformed data set it is then possible to find close whiskeys using Nearest Neighbours. This is use in the following app developped using streamlit [Whiskey Butler](http://www.whiskeybutler.ch). The code for this app is also available in the streamlit folder.

## 2. Exploratory Data Analysis

We used wordcloud and correlation to find the correlation between high-value words with the rest of the vocabulary. And here we see that using only n-gram can cause issues: the word "good" is strongly correlated with the word "bad". Thus probably indicating that the 2-gram "not good" is used a lot in the reviews.

<p align="center">
  <img src="https://github.com/Coilm/whiskey_butler/blob/main/images/good_correlation.png?raw=true)">
</p>

We can observe in the wordcloud that some good markers are visible. For example the Islay whiskeys have a strong presence of the words Peat and Smoke, which are obvious markers of this category.

<p align="center">
  <img src="https://github.com/Coilm/whiskey_butler/blob/main/images/wordcloud.png?raw=true)">
</p>

## 3. Clustering

For the clustering, we started by applying PCA on the pre-processed data and then applied multiple clustering techniques. Unfortunately without good results. However PCA is reputated to not be good with sparse data, which is the case of our dataset so we tried TruncatedSVD and UMAP. SVD didn't show better result, where the UMAP dimensionality reduction showed potential in futur clustering.

## 4. Score prediction

We wanted to use supervised machine learning to predict the scoring of the whiskey, to do so we use the pre-processed data and applied three regression models:

1. Ridge Regression
2. Hubar Regression
3. Neural Network

The issue with the prediction was that the spread of the score is not very large, between 60-100, with most reviews being in the 80s range.
