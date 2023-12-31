import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import pymongo
from pprint import pprint
import streamlit as st 
from streamlit_option_menu import option_menu
import numpy as np
import pymysql
import re
import plotly.express as px 
import matplotlib.pyplot as plt

### Below will establish the connection with MongoDB with database "Youtube" and then collection "youtube_data"
client = pymongo.MongoClient("mongodb://localhost:27017")
mydb = client["youtube"]
db = mydb.youtube_data


### Function call for youtube API which is for retreiving the channel details from youtube
def youtube_API():
    global youtube
    api_service_name = "youtube"
    api_version = "v3"
    api="AIzaSyCoUgfDmu3SyrueCuikUHYmtBlebKMstzs"  ## Developer key created to access youtube
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api)

    return youtube

###### Function call to Extract Channel details from a youtube Channel
#1. Below Fucntion will extract the channel details from YOUTUBE JSON object(Dictionary format in python).
#2. Once extracted, using a FOR LOOP we are iterating the extracted details by creating a dictionary variable 'channel_list' to store Channel details.
#3. Then we are creating a variable 'cplaylistid' to store the playlist id from Channel details. This will help in extracting the video details
#   that were uploaded for each channel

def youtube_channel_extract(channelid):
    global channel_response_list
    global cplaylistid
    
    youtube_API()
    channel_response_list = []
    request_channel = youtube.channels().list(
      part="snippet,contentDetails,statistics",
      id=channelid) 
    channel_response = request_channel.execute()
    
    for i in range(len(channel_response["items"])):
        channel_list = dict(Channel_Name = channel_response["items"][i]["snippet"]["title"],
                            Channel_Id = channel_response["items"][i]["id"],
                            Subscription_Count = channel_response["items"][i]["statistics"]["subscriberCount"],
                            Channel_Views = channel_response["items"][i]["statistics"]["viewCount"],
                            Channel_Description = channel_response["items"][i]["snippet"]["description"],
                            Playlist_Id = channel_response["items"][i]["contentDetails"]["relatedPlaylists"]["uploads"])
        channel_response_list.append(channel_list)
    
    cplaylistid = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]  #Will help in extracting the video details for channels

    return channel_response_list


###### Function call to Extract playlist details for each Channel
#1. Below Fucntion will extract the playlist details from YOUTUBE JSON object(Dictionary format in python).
#2. Inorder to extract the Playlist details Channel_id will be passed as a key
#3. At a time max of 50 playlist id's can only be extracted. Hence we are iterating the maxresults in a condition'while max_page' until the EOF is reached
#4. Based on the details extracted we are creating a dictionary varibale 'playlistid_list' to store the playlist info

def youtube_playlistid_extract(channelid):
    global playlist_response_list
    youtube_API()
    
    playlist_request = youtube.playlists().list(
    part="snippet,contentDetails",
    channelId=channelid,
    maxResults=50)
    playlist_response = playlist_request.execute()
    
    playlist_response_list = []
    for i in range(len(playlist_response["items"])):
        playlistid_list = dict(playlist_id = playlist_response["items"][i]["id"],
                            Channel_Id = playlist_response["items"][i]["snippet"]["channelId"],
                            playlist_name = playlist_response["items"][i]["snippet"]["title"],
                            video_count = playlist_response["items"][i]["contentDetails"]["itemCount"])
        playlist_response_list.append(playlistid_list)
    
    next_page_token = playlist_response.get("nextPageToken")
    max_page = True
    
    while max_page:
        if next_page_token is None:
            max_page = False
        else:
            playlist_request = youtube.playlists().list(
            part="snippet,contentDetails",
            channelId=channelid,
            maxResults=50,
            pageToken=next_page_token)
            playlist_response = playlist_request.execute()

            for i in range(len(playlist_response["items"])):
                playlistid_list = dict(playlist_id = playlist_response["items"][i]["id"],
                                       Channel_Id = playlist_response["items"][i]["snippet"]["channelId"],
                                       playlist_name = playlist_response["items"][i]["snippet"]["title"],
                                       video_count = playlist_response["items"][i]["contentDetails"]["itemCount"])
                playlist_response_list.append(playlistid_list)
            
            next_page_token = playlist_response.get("nextPageToken")
    
    return playlist_response_list


###### Function call to Extract Videoid's for each Channel
#1. Below Fucntion will extract the Video id's based on the playlistid which was stored in 'cplaylistid' at the time of retreving channel info.
#2. With the help of 'cplaylistid' we can store only max of 50 videoids at a time. So we will iterate the 'maxResults' until EOF
#3. Once the details of Video id's are stored we can easily get the video details from YOUTUBE object

def youtube_videolist_extract(cplaylistid):
    global videoids
    youtube_API()
    
    videoids_request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=cplaylistid,
        maxResults=50)
    videoids_response = videoids_request.execute()
    
    videoids = []
    for i in range(len(videoids_response["items"])):
        videoids.append(videoids_response["items"][i]["contentDetails"]["videoId"])
    
    next_page_token = videoids_response.get("nextPageToken")
    max_page = True
    
    while max_page:
        if next_page_token is None:
            max_page = False
        else:                                                                                                               
            videoids_request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=cplaylistid,
            maxResults=50,
            pageToken=next_page_token)
            videoids_response = videoids_request.execute()

            for i in range(len(videoids_response["items"])):
                videoids.append(videoids_response["items"][i]["contentDetails"]["videoId"])
            
            next_page_token = videoids_response.get("nextPageToken")
    
    return videoids


###### Function call to Extract Video details for each Channel
#1. Below Fucntion will extract the Video details from the output of fucntion 'youtube_videolist_extract' which has details of video id's
#2. Inside the function we are iterating the video ids's one by one to get the Video details and storing it in a dictionary varibale 'videolist'

def youtube_video_extract(videoids):
    global videolist
    youtube_API()

    hours_pattern = re.compile(r'(\d+)H')                       #Using a regular experssion format to get the details of hours from Duration format
    minutes_pattern = re.compile(r'(\d+)M')                     #Using a regular experssion format to get the details of Minutes from Duration format
    seconds_pattern = re.compile(r'(\d+)S')                     #Using a regular experssion format to get the details of Seconds from Duration format
    
    videolist = []
    for i in videoids:
        videolist_request = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=i)
        videolist_response = videolist_request.execute()

        for videolist_resp in videolist_response["items"]:
            dur = videolist_resp["contentDetails"]["duration"]   #Storing the Duration details inorder to extract the hours,minutes,seconds
            hours = hours_pattern.search(dur)                    #This will store hours from Duration by finding the value of number for one or more before H
            minutes = minutes_pattern.search(dur)                #This will store Minutes from Duration by finding the value of number for one or more before M
            seconds = seconds_pattern.search(dur)                #This will store Seconds from Duration by finding the value of number for one or more before S
            hours = int(hours.group(1)) if hours else '00'       # will format Hours to INT and if not found will reaplce it will '00'
            minutes = int(minutes.group(1)) if minutes else '00' # will format Minutes to INT and if not found will reaplce it will '00'
            seconds = int(seconds.group(1)) if seconds else '00' # will format Seconds to INT and if not found will reaplce it will '00'
            dur1 = f'{hours}:{minutes}:{seconds}'                # will format the string to Time format
            videoitems = dict(Channel_Id = videolist_resp["snippet"]["channelId"],
                              Channel_Name = videolist_resp["snippet"]["channelTitle"],
                              Video_Id = videolist_resp["id"],
                              Video_Name = videolist_resp["snippet"]["title"],
                              Video_Description = videolist_resp["snippet"]["localized"]["description"],
                              Tags = ' '.join(videolist_resp["snippet"].get("tags",["NA"])),
                              PublishedAt = videolist_resp["snippet"]["publishedAt"],
                              View_Count = videolist_resp["statistics"].get("viewCount"),
                              Like_Count = videolist_resp["statistics"].get("likeCount"),
                              Dislike_Count = videolist_resp["statistics"].get("dislikecount"),
                              Favorite_Count = videolist_resp["statistics"].get("favoriteCount"),
                              Comment_Count = videolist_resp["statistics"].get("commentCount"),
                              Duration = dur1,
                              thumbnail = videolist_resp["snippet"]["thumbnails"]["default"]["url"],
                              caption_status= videolist_resp["contentDetails"]["caption"]
                             )   
            videolist.append(videoitems)
    
    return videolist


###### Function call to Extract Comment details for each video's
#1. Below Fucntion will extract the Videoids's details from the output of fucntion 'youtube_videolist_extract'
#2. Inside the function we are iterating the video ids's one by one to get the Comment details for each videos and storing it in a dictionary varibale 'comment_items'
#3. At a time only a max of 50 comments can be processed hence iterating the details based on 'maxResults' until EOF for each video

def youtube_comments_extract(videoids):
    global commentids
    youtube_API()
    
    commentids = []
    try:    
        for y in videoids:
            comment_request = youtube.commentThreads().list(
            part="snippet",
            videoId=y,
            maxResults=50)
            comment_response = comment_request.execute()

            for i in range(len(comment_response["items"])):
                comment_items = dict(Comment_Id = comment_response["items"][i]["id"],
                                     video_id = comment_response["items"][i]["snippet"]["topLevelComment"]["snippet"]["videoId"],
                                     Channel_Id = comment_response["items"][i]["snippet"]["topLevelComment"]["snippet"]["channelId"],
                                     Comment_Text = comment_response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                                     Comment_Author = comment_response["items"][i]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                                     Comment_PublishedAt = comment_response["items"][i]["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                                    )
                commentids.append(comment_items)
            
            next_page_token = comment_response.get("nextPageToken")
            max_page = True

            while max_page:
                if next_page_token is None:
                    max_page = False
                else:                                                                                                               
                    comment_request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=y,
                    pageToken=next_page_token,
                    maxResults=50)
                    comment_response = comment_request.execute()

                    for i in range(len(comment_response["items"])):
                        comment_items = dict(Comment_Id = comment_response["items"][i]["id"],
                                             video_id = comment_response["items"][i]["snippet"]["topLevelComment"]["snippet"]["videoId"],
                                             Channel_Id = comment_response["items"][i]["snippet"]["topLevelComment"]["snippet"]["channelId"],
                                             Comment_Text = comment_response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                                             Comment_Author = comment_response["items"][i]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                                             Comment_PublishedAt = comment_response["items"][i]["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                                            )
                        commentids.append(comment_items)

                    next_page_token = comment_response.get("nextPageToken")
                
    except:
        pass
    
    return commentids

##### Main Function which will call other sub functions. 
#1. This will become active when dashbord button for "Extract and Load Data to MongoDB" is submitted
def call_extract(channelid):
    youtube_channel_extract(channelid)
    youtube_playlistid_extract(channelid)
    youtube_videolist_extract(cplaylistid)
    youtube_video_extract(videoids)
    youtube_comments_extract(videoids)
    
    mongodb_load()

    return "Channel details extracted and Loaded"


###### Below function will load details into Mongo DB
def mongodb_load():

    information = mydb.youtube_data
    dict_data = dict({"Channel_Name":channel_response_list,
                            "Playlist_id":playlist_response_list,
                            "Video_Id":videolist,
                            "Comment_Id":commentids
                           })
    information.insert_one(dict_data)

    return "Channel details loaded to MongoDB"


###### Below function will extract details from Mongo DB to load data to SQL
def mongodb_retreive():
    global df_channel, df_playlist, df_videoid, df_comment

    db = mydb.youtube_data

    data_channel = []
    data_playlist = []
    data_videoid = []
    data_comment = []
    data_channel_info = []

    for i in db.find({},{"_id":0,"Channel_Name":1}):
        for y in i["Channel_Name"]:
            data_channel.append(y)
    df_channel = pd.DataFrame(data_channel)

    for i in db.find({},{"_id":0,"Playlist_id":1}):
        for y in i["Playlist_id"]:
            data_playlist.append(y)
    df_playlist = pd.DataFrame(data_playlist)
    
    for i in db.find({},{"_id":0,"Video_Id":1}):
        for y in i["Video_Id"]:
            data_videoid.append(y)
    df_videoid = pd.DataFrame(data_videoid)
    df_videoid["PublishedAt"] = pd.to_datetime(df_videoid["PublishedAt"])
    df_videoid['PublishedAt'] = df_videoid['PublishedAt'].dt.strftime('%y-%m-%d %H:%M:%S')
    
    for i in db.find({},{"_id":0,"Comment_Id":1}):
        for y in i["Comment_Id"]:
            data_comment.append(y)
    df_comment = pd.DataFrame(data_comment).drop_duplicates()
    df_comment["Comment_PublishedAt"] = pd.to_datetime(df_comment["Comment_PublishedAt"])
    df_comment['Comment_PublishedAt'] = df_comment['Comment_PublishedAt'].dt.strftime('%y-%m-%d %H:%M:%S')

    for i in db.find({},{"_id":0,"Channel_Name":1}):
        for y in i["Channel_Name"]:
            data_channel_info.append(y)

    return "MongoDB details retreived"


###### Below function will delete define the Tables in SQL and create its schema in Databas "youtube_data".
def sql_table_define():

    ## Below steps will establish the connection to MYSQL
    myconnection = pymysql.connect(host = '127.0.0.1',user='root',passwd='admin@123')
    cur = myconnection.cursor()

    ## Below steps will create the database 'youtube_data' in MYSQL
    cur.execute("create database if not exists youtube_data")
    myconnection = pymysql.connect(host = '127.0.0.1',user='root',passwd='admin@123',database = "youtube_data")
    cur = myconnection.cursor()

    ## Below steps will drop the tables if it exists already in MYSQL
    cur.execute("drop table if exists Channel")
    cur.execute("drop table if exists playlist")
    cur.execute("drop table if exists Video")
    cur.execute("drop table if exists Comment")
    myconnection.commit()

    ## Below steps will create a table in MYSQL
    cur.execute("create table if not exists Channel(Channel_Name VARCHAR(255),Channel_Id VARCHAR(255) primary key,Subscription_Count int,Channel_Views int,Channel_Description text,Playlist_Id VARCHAR(255))")
    myconnection.commit()
    cur.execute("create table if not exists Playlist(playlist_id VARCHAR(255) primary key,Channel_Id VARCHAR(255),playlist_name VARCHAR(255), video_count int)")
    myconnection.commit()
    cur.execute("create table if not exists Video(Channel_Id VARCHAR(255),Channel_Name VARCHAR(255),Video_Id VARCHAR(255) primary key,Video_Name VARCHAR(255),Video_Description text,Tags text,PublishedAt TIMESTAMP DEFAULT NULL,View_Count int,Like_Count int,Dislike_Count int,Favorite_Count int,Comment_Count int,Duration Time,thumbnail VARCHAR(255),caption_status VARCHAR(255))")
    myconnection.commit()
    cur.execute("create table if not exists Comment(Comment_Id VARCHAR(255) primary key,video_id VARCHAR(255), Channel_Id VARCHAR(255),Comment_Text text,Comment_Author VARCHAR(255),Comment_PublishedAt TIMESTAMP DEFAULT NULL)")


#1. This will become active when dashbord button for "Load Data to SQL" is submitted
def sql_load(resultchannel_id):

    ## Below steps will establish the connection to database 'youtube_data' in MYSQL
    myconnection = pymysql.connect(host = '127.0.0.1',user='root',passwd='admin@123',database = "youtube_data")
    cur = myconnection.cursor()
    
    ## Below steps will extract the channel id's when User selets a Channel Name in "Select a Channel to begin transformation" from Dashboard
    df_item1 = df_channel.loc[df_channel["Channel_Id"] == resultchannel_id]
    df_item2 = df_playlist.loc[df_playlist["Channel_Id"] == resultchannel_id]
    df_item3 = df_videoid.loc[df_videoid["Channel_Id"] == resultchannel_id]
    df_item4 = df_comment.loc[df_comment["Channel_Id"] == resultchannel_id]


    ## Below steps will load the SQL table based on the Channeld extracted above
    sql = "insert into Channel values(%s,%s,%s,%s,%s,%s)"
    for i in range(0,len(df_item1)):
        cur.execute(sql,tuple(df_item1.iloc[i]))
        myconnection.commit()

    sql = "insert into Playlist values(%s,%s,%s,%s)"
    for i in range(0,len(df_item2)):
        cur.execute(sql,tuple(df_item2.iloc[i]))
        myconnection.commit()

    sql = "insert into Video values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for i in range(0,len(df_item3)):
        cur.execute(sql,tuple(df_item3.iloc[i]))
        myconnection.commit()

    sql = "insert into Comment values(%s,%s,%s,%s,%s,%s)"
    for i in range(0,len(df_item4)):
        cur.execute(sql,tuple(df_item4.iloc[i]))
        myconnection.commit()
        
    return "Data loaded to SQL successfully"

###### Streamlit app coding starts ######

###### Below steps will create a side bar menu in Streamlit dashboard
with st.sidebar:
    selected = option_menu(
        menu_title="HOME",
        options = ["Extract and Transformation","View"],
        icons = ["scissors","card-text"],
        menu_icon ="house",
        default_index = 0,
    )

###### Below steps will be active if "Extract and Transformation" side bar menu in selected in Streamlit dashboard
if selected == "Extract and Transformation":

    st.markdown("### Enter YouTube Channel ID")
    channelid = st.text_input("Hint: go to Channel home page --> Right click -->View page source-->Find Channel_id")

    if st.button("Extract and Load Data to MongoDB"):
        if channelid == "":
            st.error("Enter the Channel id to begin")
        else:
            channel_ids = []
            for i in db.find({},{"_id":0,"Channel_Name":1}):
                for y in i["Channel_Name"]:
                    channel_ids.append(y["Channel_Id"])
            
            if channelid not in channel_ids:
                channel_call = call_extract(channelid)
                st.success(channel_call)
            else:
                st.success("Channel details already loaded to Mongodb")


    #if st.button("Upload to MongoDB"):
     #   mongodb_load=mongodb_load()
      #  mongodb_load=mongodb_load(channel_response_list,playlist_response_list,videolist,commentids)
       # st.success(mongodb_load)


    data_channel1 = ["Select Channel"]

    for i in db.find({},{"_id":0,"Channel_Name":1}):
        for y in i["Channel_Name"]:
            data_channel1.append(y.get("Channel_Name"))

    st.text("                     ")
    st.text("                     ")
    st.text("                     ")
    st.text("                     ")
    st.text("                     ")
    

    #st.text("Select a Channel to begin transformation")
    result = st.selectbox("Select a Channel to begin transformation",data_channel1)

    if st.button("load data to SQL"):
        if result == "Select Channel":
            st.error("Select a Channel to load")
        else:
            mongodb_retreive()
            resultchannel_id = df_channel[df_channel["Channel_Name"] == result]["Channel_Id"].item()
            load_sql = sql_load(resultchannel_id)
            st.success(load_sql)

###### Below steps will be active if "View" side bar menu in selected in Streamlit dashboard
## There will be a default of 10 questions which can be selected to visulize data
if selected == "View":
    myconnection = pymysql.connect(host = '127.0.0.1',user='root',passwd='admin@123',database = "youtube_data")
    cur = myconnection.cursor()

    questions = st.selectbox("You can check for below questions for different answers",("Select your question",
                                        "1. What are the names of all the videos and their corresponding channels?",
                                        "2. Which channels have the most number of videos, and how many videos do they have?",
                                        "3. What are the top 10 most viewed videos and their respective channels?",
                                        "4. How many comments were made on each video, and what are their corresponding video names?",
                                        "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
                                        "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
                                        "7. What is the total number of views for each channel, and what are their corresponding channel names?",
                                        "8. What are the names of all the channels that have published videos in the year 2022?",
                                        "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                                        "10. Which videos have the highest number of comments, and what are their corresponding channel names?"),index=0)




    if questions == "1. What are the names of all the videos and their corresponding channels?":
        df_ques1 = pd.read_sql_query("select Channel_Name, Video_Name from video",myconnection)
        df_ques1 = pd.DataFrame(df_ques1)
        st.write(df_ques1)

    if questions == "2. Which channels have the most number of videos, and how many videos do they have?":
        df_ques2 = pd.read_sql_query("select Channel_Name, count(Video_Name) as video_count from video group by Channel_Name order by video_count desc;",myconnection)
        df_ques2 = pd.DataFrame(df_ques2)
        st.write(df_ques2)
        st.text(" ")
        fig = px.bar(df_ques2,x="Channel_Name",y="video_count",color="Channel_Name",text="video_count",
                     labels={"Channel_Name":"Channel Names","video_count":"Total Video counts"})
        fig.update_layout(
            width=800,
            height=500
        )
        fig.update_layout(title_text="Channel Name & its Count", title_x=0.3,title_font_color="orange")
        st.write(fig)

    if questions == "3. What are the top 10 most viewed videos and their respective channels?":
        df_ques3 = pd.read_sql_query("select Channel_Name, Video_Name, View_Count from video order by View_count desc limit 10;",myconnection)
        df_ques3 = pd.DataFrame(df_ques3)
        st.write(df_ques3)
        st.text(" ")
        st.title(":green[**Top 10 most Viewed channel]")
        fig = px.bar(df_ques3,x="Video_Name",y="View_Count",color="Channel_Name",
                     labels={"Video_Name":"Video Names","View_Count":"Total View counts"})
        fig.update_layout(
            width=800,
            height=700
        )
        fig.update_layout(title_text="Video Name & Video Count", title_x=0.3,title_font_color="white")
        st.write(fig)

    if questions == "4. How many comments were made on each video, and what are their corresponding video names?":
        df_ques4 = pd.read_sql_query("select Video_Name, Comment_Count from video order by Comment_count desc;",myconnection)
        df_ques4 = pd.DataFrame(df_ques4)
        st.write(df_ques4)

    if questions == "5. Which videos have the highest number of likes, and what are their corresponding channel names?":
        df_ques5 = pd.read_sql_query("select Channel_Name, Video_Name, Like_Count from video order by like_count desc;",myconnection)
        df_ques5 = pd.DataFrame(df_ques5)
        st.write(df_ques5)

    if questions == "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
        df_ques6 = pd.read_sql_query("select Channel_Name, Video_Name, Like_Count, Dislike_Count from video order by Like_Count desc;",myconnection)
        df_ques6 = pd.DataFrame(df_ques6)
        st.write(df_ques6)

    if questions == "7. What is the total number of views for each channel, and what are their corresponding channel names?":
        df_ques7 = pd.read_sql_query("select Channel_Name, Channel_Views from channel order by Channel_views desc;",myconnection)
        df_ques7 = pd.DataFrame(df_ques7)
        st.write(df_ques7)
        st.title(":orange[**Total views for each channel]")
        fig = px.bar(df_ques7,x="Channel_Views",y="Channel_Name",color="Channel_Name",hover_name="Channel_Views",text="Channel_Views",orientation="h",
                     labels={"Channel_Views":"Total count of Channel Views","Channel_Name":"Channel Names"})
        fig.update_layout(
            width=800,
            height=600
        )
        fig.update_traces(marker_line_color = 'black',
                  marker_line_width = 2, opacity = 1)
        fig.update_layout(title_text="Channel Name & total views", title_x=0.3,title_font_color="violet")
        st.write(fig)

    if questions == "8. What are the names of all the channels that have published videos in the year 2022?":
        df_ques8 = pd.read_sql_query("select Channel_Name, PublishedAt from video where substring(PublishedAt,1,4) = 2022 ;",myconnection)
        df_ques8 = pd.DataFrame(df_ques8)
        st.write(df_ques8)
        st.text(" ")
        st.text(" ")
        fig = px.pie(df_ques8,names="Channel_Name",color_discrete_sequence=px.colors.sequential.Teal_r)
        fig.update_layout(title_text="Channel published in 2022", title_x=0.3,title_font_color="grey")
        st.write(fig)

    if questions == "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?":
        df_ques9 = pd.read_sql_query("select channel_Name, SUBSTRING(SEC_TO_TIME(avg(Duration)),1,8) as Average_Duration from video group by Channel_Name order by Average_Duration;",myconnection)
        df_ques9 = pd.DataFrame(df_ques9)
        st.write(df_ques9)
        st.text("")
        st.text("")
        fig = px.bar(df_ques9,x="channel_Name",y="Average_Duration",hover_name="channel_Name",color="channel_Name",
                     labels={"channel_Name":"Channel Names","Average_Duration":"Average Duration of each Channel"})
        fig.update_layout(title_text="Average Duration for Each Channel", title_x=0.2,title_font_color="yellow")
        st.write(fig)

    if questions == "10. Which videos have the highest number of comments, and what are their corresponding channel names?":
        df_ques10 = pd.read_sql_query("select Channel_Name, Video_Name, Comment_Count from video order by Comment_count desc;",myconnection)
        df_ques10 = pd.DataFrame(df_ques10)
        st.write(df_ques10)
