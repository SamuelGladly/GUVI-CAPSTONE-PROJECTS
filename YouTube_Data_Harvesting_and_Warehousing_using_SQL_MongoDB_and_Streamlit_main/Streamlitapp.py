
import json
import pandas as pd
import streamlit as st
import mysql.connector
import pymongo
from pymongo import MongoClient
from googleapiclient.discovery import build
from sqlquery import sql_q1, sql_q2, sql_q3, sql_q4, sql_q5, sql_q6, sql_q7, sql_q8, sql_q9, sql_q10

api_key = 'AIzaSyC9lK5JiTsTcRPq121wKccpM6CiJe5CRgg'
youtube = build('youtube', 'v3', developerKey=api_key)


# SQL Questions
q1 = sql_q1()
q2 = sql_q2()
q3 = sql_q3()
q4 = sql_q4()
q5 = sql_q5()
q6 = sql_q6()
q7 = sql_q7()
q8 = sql_q8()
q9 = sql_q9()
q10 = sql_q10()
#
st.sidebar.title("You Tube Data Harvest")
options = {
    "sql1" : "1.what are the names of all the videos and their corresponding channels?",
    "sql2" : "2.which channels have the most number of videos, and how many videos do they have?",
    "sql3" : "3.what are the top 10 most viewed videos and their respective channels?",
    "sql4" : "4.how many comments were made on each video and what are their corresponding videonames?",
    "sql5" : "5.which videos have the heighest number of likes, and what are their corresponding channelnames?",
    "sql6" : "6.what is the total number of likes and dislikes for each video, and what are their corresponding video names?",
    "sql7" : "7.what is the total number of views for each channels, and what are their corresponding channelnames?",
    "sql8" : "8.what are the names of all the channels that have published videos in the year 2022?",
    "sql9" : "9.what is the average duration of all videos in each channel, and what are their corresponding channelsnames?",
    "sql10" : "10.which videos have the highest number of comments, and what are their corresponding channelnames?"
    } 
#
#
def sql_query():
    selected_option = st.sidebar.selectbox("SQL Questions:", list(options.values())) # Dropdown component
    for key, value in options.items(): # Call function based on selected option
        if value == selected_option:
            if key == "sql1":
                st.write(q1)
            elif key == "sql2":
                st.write(q2)
            elif key == "sql3":
                st.write(q3)
            elif key == "sql4":
                st.write(q4)
            elif key == "sql5":
                st.write(q5)
            elif key == "sql6":
                st.write(q6)
            elif key == "sql7":
                st.write(q7)
            elif key == "sql8":
                st.write(q8)
            elif key == "sql9":
                st.write(q9)
            elif key == "sql10":
                st.write(q10)
    return selected_option

#
def ch_db_ql():
    # # # --------- # # #
    videoid_details = []
    v_c_data = []

    channel_id = st.sidebar.text_input("Channel ID") # get input from user
    channel_button = st.sidebar.button("Get Full data")

    if channel_button:

        def get_channel_data(youtube, channel_id): # ----------- 1
            
            channel_response = youtube.channels().list(
            id=channel_id,
            part='snippet,statistics,contentDetails')
            channel_detls = channel_response.execute()
            # ---------------
            c_data = dict ( Channel_name = channel_detls['items'][0]['snippet']['title'],
                            Channel_ID = channel_detls['items'][0]['id'],
                            Subscribers = channel_detls['items'][0]['statistics']['subscriberCount'],
                            Views = channel_detls['items'][0]['statistics']['viewCount'],
                            Description = channel_detls['items'][0]['snippet']['description'],
                            Total_Videos = channel_detls['items'][0]['statistics']['videoCount'],
                            Playlist_id = channel_detls['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
                            )
            return c_data

        # ---------------

        # Fetching the Video_ID Details from Playlist:
        def get_videoID_data(youtube, playid): # ----------- 2
            
            vid_details = []
            
            vid_request = youtube.playlistItems().list(
            playlistId=playid,
            maxResults=50,
            part='snippet,contentDetails' # snippet,statistics,contentDetails
            )
            response = vid_request.execute()
            
            for item in response['items']:
                vid_details.append(item['contentDetails']['videoId'])
            
            return vid_details

        # ---------------

        # Fetching video details of each video in the playlist:
        def get_videodetails(youtube, videoID_data): # ----------- 3
            
            for video_id in videoID_data: # Fetch video details
                video_response = youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=video_id,
                    maxResults=50
                ).execute()

                if video_response['items']:
                    video_details = {
                        "Video_Id": video_id,
                        "Video_Name": video_response['items'][0]['snippet']['title'],
                        "Video_Description": video_response['items'][0]['snippet']['description'],
                        "Video_Statistics": video_response['items'][0]['statistics']['commentCount'],
                        "Comment_Count": video_response['items'][0]['statistics'].get('commentCount', 0),
                        "View_Count": video_response['items'][0]['statistics'].get('viewCount', 0),
                        "Like_Count": video_response['items'][0]['statistics'].get('likeCount', 0),
                        "Favorite_Count": video_response['items'][0]['statistics'].get('favoriteCount', 0),
                        "Published_At": video_response['items'][0]['snippet']['publishedAt'],
                        "Duration": video_response['items'][0]['contentDetails']['duration'],
                        "Thumbnail": video_response['items'][0]['snippet']['thumbnails']['default']['url'],
                        "Caption_Status": video_response['items'][0]['contentDetails'].get('caption'),
                    }
                    
                videoid_details.append(video_details)
            
            return videoid_details

        # ---------------

        # Fetching the Commands of each videos
        def get_comments_details(youtube,videoID_data): # ----------- 4
            for i in videoID_data:
                comments_response = youtube.commentThreads().list(
                    part='snippet',
                    maxResults=2,  # only 2 comments per vios
                    videoId=i
                ).execute()
            
                comments = comments_response['items']
                
                for comment in comments:
                    comment_information = {
                        "Video_iD": i,
                        "Comment_Id": comment['snippet']['topLevelComment']['id'],
                        "Comment_Text": comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                        "Comment_Author": comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        "Comment_PublishedAt": comment['snippet']['topLevelComment']['snippet']['publishedAt']
                    }
                    v_c_data.append(comment_information)
            
            return v_c_data

        # ---------------

        getCH = get_channel_data(youtube, channel_id)
        Channel_Name = (getCH['Channel_name'][:4]) # get channel name from the getch
        playid = (getCH['Playlist_id'])

        videoID_data = get_videoID_data(youtube, playid)
        getVD = get_videodetails(youtube, videoID_data)
        getCC = get_comments_details(youtube,videoID_data)

        # Adding all datas to a single data frame.
        Main_data_frame = {
            'Channel': getCH,
            'VideoID': videoID_data,
            'VideoDetail': getVD,
            'Comments': getCC
        }
        # ---------------
        st.write("New Channel Data")
        Main_data_frame

        # Create a MongoClient instance to connect to the MongoDB server

        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client["youtubeid"] # Select the database
        collection = db[Channel_Name]
        mongo_dump = collection.insert_one(Main_data_frame) # Inserting the *** DATA into Mongo DB ***
        #

        # MySQL Connection ----------------------------------------
        mysql_conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='sql@123456789',
            port=3307,
            database='mongodb01'
        )

        # Create sql Connector -------------------------------------
        mysql_cursor = mysql_conn.cursor()

        # Channel table Creation 01:

        def get_sqlchannel_data():
            
            mysql_create_table = f"""CREATE TABLE mysql_{Channel_Name}_chtable
            (
            Channel_name VARCHAR(255),
            Channel_ID VARCHAR(255),
            Subscribers INT,
            Views INT,
            Description TEXT,
            Total_Videos INT,
            Playlist_id VARCHAR(255)
            )"""
            
            mysql_cursor.execute(mysql_create_table) # Create the table
            
            mongo_data = collection.find() # Fetch data from MongoDB collection
            
            # Insert data into MySQL table
            for document in mongo_data:
                
                Channel_name = document["Channel"]["Channel_name"]
                Channel_ID = document["Channel"]["Channel_ID"]
                Subscribers = document["Channel"]["Subscribers"]
                Views = document["Channel"]["Views"]
                Description = document["Channel"]["Description"]
                Total_Videos = document["Channel"]["Total_Videos"]
                Playlist_id = document["Channel"]["Playlist_id"]

                mysql_query = f"""
                INSERT INTO mysql_{Channel_Name}_chtable (
                    Channel_name, Channel_ID, Subscribers, Views, Description, Total_Videos, Playlist_id
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                )
                """
                mysql_values = (
                    Channel_name, Channel_ID, Subscribers, Views, Description, Total_Videos, Playlist_id
                )
                mysql_cursor.execute(mysql_query, mysql_values)

            mysql_cursor.execute(f"""select * from mongodb01.mysql_{Channel_Name}_chtable""")

            rows = mysql_cursor.fetchall() # Fetch the results of the query

            # Print the rows
            for row in rows:
                print(row)
            
            return rows

        #

        # Video table Creation 02:

        def get_sqlchannelvideo_data():

            mysql_create_table = f"""CREATE TABLE mysql_{Channel_Name}_vitable
            (
            Video_Id VARCHAR(255),
            Video_Name VARCHAR(255),
            Video_Description TEXT,
            Video_Statistics VARCHAR(255),
            Comment_Count INT,
            View_Count INT,
            Like_Count INT,
            Favorite_Count INT,
            Published_At VARCHAR(255),
            Duration VARCHAR(255),
            Thumbnail VARCHAR(255),
            Caption_Status VARCHAR(255),
            Playlist_id VARCHAR(255)
            )"""
            
            mysql_cursor.execute(mysql_create_table)
            
            mongo_data = collection.find() # Fetch data from MongoDB collection

            # Insert data into MySQL table
            for document in mongo_data:
                Playlist_id = document["Channel"]["Playlist_id"]
                for video_detail in document["VideoDetail"]:
                    
                    Video_Id = video_detail["Video_Id"]
                    Video_Name = video_detail["Video_Name"]
                    Video_Description = video_detail["Video_Description"]
                    Video_Statistics = video_detail["Video_Statistics"]
                    Comment_Count = video_detail["Comment_Count"]
                    View_Count = video_detail["View_Count"]
                    Like_Count = video_detail["Like_Count"]
                    Favorite_Count = video_detail["Favorite_Count"]
                    Published_At = video_detail["Published_At"]
                    Duration = video_detail["Duration"]
                    Thumbnail = video_detail["Thumbnail"]
                    Caption_Status = video_detail["Caption_Status"]
                    

                    mysql_query1 = f"""
                    INSERT INTO mysql_{Channel_Name}_vitable (
                        Video_Id, Video_Name, Video_Description, Video_Statistics, Comment_Count, View_Count, Like_Count,Favorite_Count, Published_At, Duration, Thumbnail, Caption_Status, Playlist_id
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    """
                    mysql_values1 = (
                        Video_Id, Video_Name, Video_Description, Video_Statistics, Comment_Count, View_Count, Like_Count,Favorite_Count, Published_At, Duration, Thumbnail, Caption_Status, Playlist_id
                    )
                    mysql_cursor.execute(mysql_query1, mysql_values1)

                mysql_cursor.execute(f"""select * from mongodb01.mysql_{Channel_Name}_vitable""")

                rows1 = mysql_cursor.fetchall() # Fetch the results of the query

                for row1 in rows1:
                    print(row1)

            return rows1

        # Comment table Creation 03:

        def get_sqlchannelcomments_data():
            
            mysql_create_table = f"""CREATE TABLE mysql_{Channel_Name}_cctable
            (
            Video_id VARCHAR(255),
            Comment_id VARCHAR(255),
            Comment_text TEXT,
            Comment_author VARCHAR(255),
            Comment_PublishedAt VARCHAR(255),
            Playlist_id VARCHAR(255)
            )"""

            mysql_cursor.execute(mysql_create_table)

            mongo_data = collection.find()

            for document in mongo_data: # Insert data into MySQL table
                Playlist_id = document["Channel"]["Playlist_id"]
                for cc_detail in document["Comments"]:
                    Video_iD = cc_detail["Video_iD"]
                    Comment_Id = cc_detail["Comment_Id"]
                    Comment_Text = cc_detail["Comment_Text"]
                    Comment_Author = cc_detail["Comment_Author"]
                    Comment_PublishedAt = cc_detail["Comment_PublishedAt"]

                    mysql_query2 = f"""
                    INSERT INTO mysql_{Channel_Name}_cctable (
                        Video_iD, Comment_Id, Comment_Text, Comment_Author, Comment_PublishedAt, Playlist_id
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s)"""
                    mysql_values2 = (
                        Video_iD, Comment_Id, Comment_Text, Comment_Author, Comment_PublishedAt, Playlist_id
                    )
                    mysql_cursor.execute(mysql_query2, mysql_values2)

                mysql_cursor.execute(f"""select * from mongodb01.mysql_{Channel_Name}_cctable""")
                
                rows2 = mysql_cursor.fetchall()

                for row2 in rows2:
                    print(row2)

            return rows2

        # Playlist table Creation 04:

        def get_sqlchannelplaylist_data():
            
            mysql_create_table = f"""CREATE TABLE mysql_{Channel_Name}_pltable ( Channel_ID VARCHAR(255), Playlist_id VARCHAR(255), VideoID VARCHAR(255) )"""

            mysql_cursor.execute(mysql_create_table)

            mongo_data = collection.find()

            # Insert data into the SQL table
            for document in mongo_data:
                
                Channel_ID = document["Channel"]["Channel_ID"]
                Playlist_id = document["Channel"]["Playlist_id"]
                video_pliD = document["VideoID"]
                mysql_query3 = f"""INSERT INTO mysql_{Channel_Name}_pltable (Channel_ID, VideoID, Playlist_id) VALUES (%s, %s, %s)"""
                mysql_values3 = [(Channel_ID, video_id, Playlist_id) for video_id in video_pliD]
                mysql_cursor.executemany(mysql_query3, mysql_values3)
            
            mysql_cursor.execute(f"""select * from mongodb01.mysql_{Channel_Name}_pltable""")
            
            rows3 = mysql_cursor.fetchall()

            for row3 in rows3:
                print(row3)
            
            return rows3

        #

        mysql_cursor = mysql_conn.cursor()

        def sql_execution():

            sqlch = get_sqlchannel_data() # SQL table creation
            sqlvi = get_sqlchannelvideo_data()
            sqlcc = get_sqlchannelcomments_data()
            sqlpl = get_sqlchannelplaylist_data()

        execution = sql_execution()

        dataf0 = pd.read_sql(f"""SELECT * FROM mongodb01.mysql_{Channel_Name}_chtable""", mysql_conn) # Read data from the hello table
        dataf1 = pd.read_sql(f"""SELECT * FROM mongodb01.mysql_{Channel_Name}_pltable""", mysql_conn) # dataf1 = pd.read_sql_query(execution[3], mysql_conn)
        dataf2 = pd.read_sql(f"""SELECT * FROM mongodb01.mysql_{Channel_Name}_vitable""", mysql_conn)
        dataf3 = pd.read_sql(f"""SELECT * FROM mongodb01.mysql_{Channel_Name}_cctable""", mysql_conn)

        #
        dataf0
        dataf1
        dataf2
        dataf3

        #
        st.line_chart(dataf0)  # Display the area chart
        # st.line_chart(dataf1)
        #
        mysql_conn.close()
        # # #

    # # # --------- # # #

def mongo_info():
    client = MongoClient("mongodb://localhost:27017")
    db = client["youtubeid"]  # Replace with your MongoDB database name
    collection_names = db.list_collection_names()

    # Dropdown for selecting collection
    selected_collection = st.sidebar.selectbox("Mongo DB Collections:", collection_names)

    # Retrieve data from selected collection
    if selected_collection:
        collection = db[selected_collection]
        data = list(collection.find())

        # Display data
        st.write("Channel Data:")
        for document in data:
            st.write(document)

#
# Main Function:
def main(): 
    ch_db_ql()
    mongo_info()
    sql_query()


#
if __name__ == "__main__":
    main()
# # # --------- # # #
