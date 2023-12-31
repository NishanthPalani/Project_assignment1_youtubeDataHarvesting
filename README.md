# **YOUTUBE_DATA_HARVESTING**


## *Introduction*

Youtube_Data_Harvesting is a project aiming to give users a friendly environment to collect and store the data for analysis. Inorder to achieve a user friendly environment this was built on top of Streamlit Dashboard. At the backend these data will initially get stored to MongoDB and later migrated to SQL achieving analytics part for users on the data extracted.


## *Table of Contents*

1.  Technologies used
1.  Libraries used
1.  Features
1.  Retrieving data from the YouTube API
1.  MongoDB usage
1.  SQL usage
1.  Data Analysis using Streeamlit and Plotly


## *Technologies used*

1. Python    - for Coding
1. MongoDB   - NOSQL Database for storing the data(JSON) from YOUTUBE
1. MYSQL     - SQL Database for storing the transformed data to perform data analysis
1. Streamlit - for Visualization front-end
1. Plotly    - to perform visualized charts for data analysis


## *Libraries used*

Below libraires were used to code the project
```python
- import google_auth_oauthlib.flow
- import googleapiclient.discovery
- import googleapiclient.errors
- import pandas as pd
- import pymongo
- import streamlit as st 
- import numpy as np
- import pymysql
- import plotly.express as px
```

## *Features*

- Retrieve data from the YouTube API, including channel information, playlists, videos, and comments.
- Store the retrieved data in a MongoDB database.
- Migrate the data to a SQL.
- Analyze and visualize data using Streamlit and Plotly to gain insights


## *Retrieving data from the YouTube API*

The project utilizes the Google API to retrieve comprehensive data from YouTube channels. The data includes information on channels, playlists, videos, and comments. By interacting with the Google API, we collect the data with a JSON file.


## *MongoDB Usage*

The retrieved data from YOUTUBE API is stored in to a MongoDB database based on user input. If the data already exists in the database, it will throw an error "Channel details already loaded to Mongodb". This storage process ensures data is stored efficiently by proper usage.


## *SQL Usage*

The application allows users to migrate data from MongoDB to a SQL. Users can choose which channel's data to migrate and store. To ensure compatibility with a structured format, the data is cleaned and converted to a pandas library. Following data cleaning, the information is segregated into separate tables, including channels, playlists, videos, and comments.


## *Data Analysis using Streamlit and Plotly*

This project provides data analysis and Visualize capabilities using Plotly and Streamlit. With the integrated Plotly library, users can select any of the 10 default questions available and do the analysis for the channels loaded with its appealing charts and graphs to gain insights from the collected data.


The Streamlit app provide users an interface connect with data and explore the charts visually. 


**Contact**

📧 Email: nishanthnici@gmail.com 




