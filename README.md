**YOUTUBE_DATA_HARVESTING**

**Introduction**

Youtube_Data_Harvesting project is a project aiming to give users a friendly environment to collect and store the data for analysis. Inrder to achieve a user friendly environment this was built on top of Streamlit Dashboard. At the backend these data will initially get stored to MongoDB and later to SQL achieving analysis part for users on the data extracted.


**Table of Contents**
   1.  Technologies used to build this project
   2.  Libraries used
   3.  MongoDB usage
   4.  SQL usage
   5.  Streamlit usage
   6.  plotly 


**Technologies used to build this project**
  1. Python - Coding
  2. MongoDB - Database for storing the data from YOUTUBE
  3. MYSQL - Database for storing the transformed data to perform data analysis
  4. Streamlit app - for Visualization front-end
  5. Plotly - to perform visualized charts for data analysis


**Libraries used**

Below libraires were used to perform the full project
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import pymongo
import streamlit as st 
import numpy as np
import pymysql
import re
import plotly.express as px 



