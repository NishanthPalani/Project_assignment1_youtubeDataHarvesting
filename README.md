# **YOUTUBE_DATA_HARVESTING**


## *Introduction*

Youtube_Data_Harvesting project is a project aiming to give users a friendly environment to collect and store the data for analysis. Inrder to achieve a user friendly environment this was built on top of Streamlit Dashboard. At the backend these data will initially get stored to MongoDB and later to SQL achieving analysis part for users on the data extracted.


## *Table of Contents*
1.  Technologies used to build this project
1.  Libraries used
1.  MongoDB usage
1.  SQL usage
1.  Streamlit usage
1.  plotly 


## *Technologies used*
1. Python - Coding
1. MongoDB - Database for storing the data from YOUTUBE
1. MYSQL - Database for storing the transformed data to perform data analysis
1. Streamlit app - for Visualization front-end
1. Plotly - to perform visualized charts for data analysis


## *Libraries used*
Below libraires were used to perform the full project
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
- Analyze and visualize data using Streamlit and Plotly.
- Gain insights into channel performance, video metrics, and more.

## *Retrieving data from the YouTube API*
The project utilizes the Google API to retrieve comprehensive data from YouTube channels. The data includes information on channels, playlists, videos, and comments. By interacting with the Google API, we collect the data with a JSON file.

## *Storing data in MongoDB*
The retrieved data is stored in a MongoDB database based on user authorization. If the data already exists in the database, it will throw an error "Channel details already loaded to Mongodb". This storage process ensures data is stored efficiently by proper usage.

## *Migrating data to a SQL data warehouse*
The application allows users to migrate data from MongoDB to a SQL. Users can choose which channel's data to migrate and store. To ensure compatibility with a structured format, the data is cleaned and converted to a pandas library. Following data cleaning, the information is segregated into separate tables, including channels, playlists, videos, and comments, utilizing SQL queries.

## *Data Analysis*
This project provides data analysis and Visualize capabilities using Plotly and Streamlit. With the integrated Plotly library, users can select the any of the 10 default questions available  and check do the analysis for the channels loaded with its appealing charts and graphs to gain insights from the collected data.

- **Channel Analysis:** Channel analysis includes insights on playlists, videos, subscribers, views, likes, comments, and durations. Gain a deep understanding of the channel's performance through detailed visualizations and summaries.

- **Video Analysis:** Video analysis focuses on views, likes, comments, and durations by providing useres a visual representations to gather insights.

The Streamlit app provides an users an interface to see the charts and explore the data visually. 


**Contact**

📧 Email: nishanthnici@gmail.com 




