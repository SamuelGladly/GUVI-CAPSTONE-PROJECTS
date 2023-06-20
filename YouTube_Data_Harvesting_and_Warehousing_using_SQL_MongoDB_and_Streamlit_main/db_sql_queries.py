import pandas as pd
import mysql.connector

# MySQL Connection
mysql_conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    port=3307,
    database='mongodb01'
)

# Create a cursor object
mysql_cursor = mysql_conn.cursor()
#
def sql_q1(): # 1.what are the names of all the videos and their corresponding channels?
    sql_query01 = f"""SELECT chtable.Channel_Name,vitable.Video_Name
    FROM mongodb01.mysql_ammu_vitable AS vitable
    INNER JOIN mongodb01.mysql_ammu_chtable AS chtable ON vitable.Playlist_id = chtable.Playlist_id
    UNION
    SELECT chtable.Channel_Name,vitable.Video_Name
    FROM mongodb01.mysql_back_vitable AS vitable
    INNER JOIN mongodb01.mysql_back_chtable AS chtable ON vitable.Playlist_id = chtable.Playlist_id
    UNION
    SELECT chtable.Channel_Name,vitable.Video_Name
    FROM mongodb01.mysql_gran_vitable AS vitable
    INNER JOIN mongodb01.mysql_gran_chtable AS chtable ON vitable.Playlist_id = chtable.Playlist_id
    UNION
    SELECT chtable.Channel_Name,vitable.Video_Name
    FROM mongodb01.mysql_irfa_vitable AS vitable
    INNER JOIN mongodb01.mysql_irfa_chtable AS chtable ON vitable.Playlist_id = chtable.Playlist_id
    UNION
    SELECT chtable.Channel_Name,vitable.Video_Name
    FROM mongodb01.mysql_khal_vitable AS vitable
    INNER JOIN mongodb01.mysql_khal_chtable AS chtable ON vitable.Playlist_id = chtable.Playlist_id
    UNION
    SELECT chtable.Channel_Name,vitable.Video_Name
    FROM mongodb01.mysql_mone_vitable AS vitable
    INNER JOIN mongodb01.mysql_mone_chtable AS chtable ON vitable.Playlist_id = chtable.Playlist_id
    UNION
    SELECT chtable.Channel_Name,vitable.Video_Name
    FROM mongodb01.mysql_noma_vitable AS vitable
    INNER JOIN mongodb01.mysql_noma_chtable AS chtable ON vitable.Playlist_id = chtable.Playlist_id
    UNION
    SELECT chtable.Channel_Name,vitable.Video_Name
    FROM mongodb01.mysql_tami_vitable AS vitable
    INNER JOIN mongodb01.mysql_tami_chtable AS chtable ON vitable.Playlist_id = chtable.Playlist_id;"""
    #
    mysql_cursor.execute(sql_query01)

    # Fetch the result into a Pandas DataFrame
    result = mysql_cursor.fetchall()
    q1df = pd.DataFrame(result, columns=['Channel_name', 'Video_Name'])
    # print("SQL - q1df")
    #
    return q1df

#
# ----------------------------------------

def sql_q2(): # 2.which channels have the most number of videos, and how many videos do they have?
    sql_query02 = f"""select Channel_name, Total_Videos from mysql_ammu_chtable
    Union
    select Channel_name, Total_Videos from mysql_back_chtable
    Union
    select Channel_name, Total_Videos from mysql_fire_chtable
    Union
    select Channel_name, Total_Videos from mysql_gran_chtable
    Union
    select Channel_name, Total_Videos from mysql_irfa_chtable
    Union
    select Channel_name, Total_Videos from mysql_khal_chtable
    Union
    select Channel_name, Total_Videos from mysql_mone_chtable
    Union
    select Channel_name, Total_Videos from mysql_noma_chtable
    Union
    select Channel_name, Total_Videos from mysql_tami_chtable
    order by Total_Videos Desc;
    """
    #
    mysql_cursor.execute(sql_query02)
    
    # Fetch the result into a Pandas DataFrame
    result = mysql_cursor.fetchall()
    q2df = pd.DataFrame(result, columns=['Channel_name', 'Total_Videos'])
    # print("SQL - q2df")
    #
    return q2df

#
# ----------------------------------------

def sql_q3(): # 3.what are the top 10 most viewed videos and their respective channels?
    sql_query03 = f"""SELECT Video_Name, Channel_Name, View_Count
    FROM (
    SELECT v.Video_Name, c.Channel_Name, v.View_Count
    FROM mongodb01.mysql_ammu_vitable v
    JOIN mongodb01.mysql_ammu_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT v.Video_Name, c.Channel_Name, v.View_Count
    FROM mongodb01.mysql_back_vitable v
    JOIN mongodb01.mysql_back_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT v.Video_Name, c.Channel_Name, v.View_Count
    FROM mongodb01.mysql_fire_vitable v
    JOIN mongodb01.mysql_fire_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT v.Video_Name, c.Channel_Name, v.View_Count
    FROM mongodb01.mysql_gran_vitable v
    JOIN mongodb01.mysql_gran_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT v.Video_Name, c.Channel_Name, v.View_Count
    FROM mongodb01.mysql_irfa_vitable v
    JOIN mongodb01.mysql_irfa_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT v.Video_Name, c.Channel_Name, v.View_Count
    FROM mongodb01.mysql_khal_vitable v
    JOIN mongodb01.mysql_khal_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT v.Video_Name, c.Channel_Name, v.View_Count
    FROM mongodb01.mysql_mone_vitable v
    JOIN mongodb01.mysql_mone_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT v.Video_Name, c.Channel_Name, v.View_Count
    FROM mongodb01.mysql_tami_vitable v
    JOIN mongodb01.mysql_tami_chtable c ON v.Playlist_id = c.Playlist_id
    ) AS combined_results
    ORDER BY View_Count DESC LIMIT 10;
    """
    #
    mysql_cursor.execute(sql_query03)
    
    # Fetch the result into a Pandas DataFrame
    result = mysql_cursor.fetchall()
    q3df = pd.DataFrame(result, columns=['Video_Name', 'Channel_Name','View_Count'])
    # print("SQL - q3df")
    #
    return q3df
#
# ----------------------------------------

def sql_q4(): # 4.how many comments were made on each video and what'r their corresponding video names?
    sql_query04 =f"""select l.Channel_name, COUNT(Comment_id) AS Comments
    from mongodb01.mysql_ammu_cctable AS c
    join mongodb01.mysql_ammu_chtable AS l on l.Playlist_id = c.Playlist_id
    group by l.Channel_name
    union
    select l.Channel_name, COUNT(Comment_id) AS Comments
    from mongodb01.mysql_back_cctable AS c
    join mongodb01.mysql_back_chtable AS l on l.Playlist_id = c.Playlist_id
    group by l.Channel_name
    union
    select l.Channel_name, COUNT(Comment_id) AS Comments
    from mongodb01.mysql_fire_cctable AS c
    join mongodb01.mysql_fire_chtable AS l on l.Playlist_id = c.Playlist_id
    group by l.Channel_name
    union
    select l.Channel_name, COUNT(Comment_id) AS Comments
    from mongodb01.mysql_irfa_cctable AS c
    join mongodb01.mysql_irfa_chtable AS l on l.Playlist_id = c.Playlist_id
    group by l.Channel_name
    union
    select l.Channel_name, COUNT(Comment_id) AS Comments
    from mongodb01.mysql_khal_cctable AS c
    join mongodb01.mysql_khal_chtable AS l on l.Playlist_id = c.Playlist_id
    group by l.Channel_name
    union
    select l.Channel_name, COUNT(Comment_id) AS Comments
    from mongodb01.mysql_mone_cctable AS c
    join mongodb01.mysql_mone_chtable AS l on l.Playlist_id = c.Playlist_id
    group by l.Channel_name
    union
    select l.Channel_name, COUNT(Comment_id) AS Comments
    from mongodb01.mysql_noma_cctable AS c
    join mongodb01.mysql_noma_chtable AS l on l.Playlist_id = c.Playlist_id
    group by l.Channel_name
    union
    select l.Channel_name, COUNT(Comment_id) AS Comments
    from mongodb01.mysql_gran_cctable AS c
    join mongodb01.mysql_gran_chtable AS l on l.Playlist_id = c.Playlist_id
    group by l.Channel_name
    union
    select l.Channel_name, COUNT(Comment_id) AS Comments
    from mongodb01.mysql_tami_cctable AS c
    join mongodb01.mysql_tami_chtable AS l on l.Playlist_id = c.Playlist_id
    group by l.Channel_name;
    """

    mysql_cursor.execute(sql_query04)
    
    # Fetch the result into a Pandas DataFrame
    result = mysql_cursor.fetchall()
    q4df = pd.DataFrame(result, columns=['Channel_name', 'Comment_id'])
    # print("SQL - q3df")
    #
    return q4df

#
# ----------------------------------------

def sql_q5(): # 5.which videos have heighest number of likes, and what'r their corresponding channelnames?
    sql_query05 =f"""SELECT Channel_Name, Like_Count
    FROM (
    SELECT c.Channel_Name, v.Like_Count
    FROM mongodb01.mysql_ammu_vitable v
    JOIN mongodb01.mysql_ammu_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Like_Count
    FROM mongodb01.mysql_back_vitable v
    JOIN mongodb01.mysql_back_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Like_Count
    FROM mongodb01.mysql_fire_vitable v
    JOIN mongodb01.mysql_fire_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Like_Count
    FROM mongodb01.mysql_gran_vitable v
    JOIN mongodb01.mysql_gran_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Like_Count
    FROM mongodb01.mysql_irfa_vitable v
    JOIN mongodb01.mysql_irfa_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Like_Count
    FROM mongodb01.mysql_khal_vitable v
    JOIN mongodb01.mysql_khal_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Like_Count
    FROM mongodb01.mysql_mone_vitable v
    JOIN mongodb01.mysql_mone_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Like_Count
    FROM mongodb01.mysql_tami_vitable v
    JOIN mongodb01.mysql_tami_chtable c ON v.Playlist_id = c.Playlist_id
    ) AS combined_results
    ORDER BY Like_Count DESC LIMIT 10;
    """
    mysql_cursor.execute(sql_query05)
    
    # Fetch the result into a Pandas DataFrame
    result = mysql_cursor.fetchall()
    q5df = pd.DataFrame(result, columns=['Channel_Name', 'Like_Count'])
    # print("SQL - q3df")
    #
    return q5df

#
# ----------------------------------------

def sql_q6(): # 6.what is the total no.of likes & dislikes for each video, & what'r their corresponding videonames?
    sql_query06 = f"""select Video_Name, Like_Count from mongodb01.mysql_ammu_vitable UNION
    select Video_Name, Like_Count from mongodb01.mysql_back_vitable UNION
    select Video_Name, Like_Count from mongodb01.mysql_fire_vitable UNION
    select Video_Name, Like_Count from mongodb01.mysql_gran_vitable UNION
    select Video_Name, Like_Count from mongodb01.mysql_irfa_vitable UNION
    select Video_Name, Like_Count from mongodb01.mysql_khal_vitable UNION
    select Video_Name, Like_Count from mongodb01.mysql_mone_vitable UNION
    select Video_Name, Like_Count from mongodb01.mysql_noma_vitable UNION
    select Video_Name, Like_Count from mongodb01.mysql_tami_vitable order by Like_Count Desc; 
    """
    mysql_cursor.execute(sql_query06)
    
    # Fetch the result into a Pandas DataFrame
    result = mysql_cursor.fetchall()
    q6df = pd.DataFrame(result, columns=['Video_Name', 'Like_Count'])
    # print("SQL - q3df")
    #
    return q6df

#
# ----------------------------------------

def sql_q7(): # 7.what is the total no.of views for each channels, & what'r their corresponding channelnames?
    sql_query07 = f"""select Channel_name, Views, Total_Videos from mongodb01.mysql_ammu_chtable union
    select Channel_name, Views, Total_Videos from mongodb01.mysql_back_chtable union
    select Channel_name, Views, Total_Videos from mongodb01.mysql_fire_chtable union
    select Channel_name, Views, Total_Videos from mongodb01.mysql_gran_chtable union
    select Channel_name, Views, Total_Videos from mongodb01.mysql_irfa_chtable union
    select Channel_name, Views, Total_Videos from mongodb01.mysql_khal_chtable union
    select Channel_name, Views, Total_Videos from mongodb01.mysql_mone_chtable union
    select Channel_name, Views, Total_Videos from mongodb01.mysql_noma_chtable union
    select Channel_name, Views, Total_Videos from mongodb01.mysql_tami_chtable order by Views desc;
    """
    mysql_cursor.execute(sql_query07)
    
    # Fetch the result into a Pandas DataFrame
    result = mysql_cursor.fetchall()
    q7df = pd.DataFrame(result, columns=['Channel_name', 'Views','Total_Videos'])
    # print("SQL - q3df")
    #
    return q7df

#
# ----------------------------------------

def sql_q8(): # 8.what are the names of all the channels that have published videos in the year 2022?
    sql_query08 = f"""SELECT Channel_Name, Published_At
    FROM (
    SELECT c.Channel_Name, v.Published_At
    FROM mongodb01.mysql_ammu_vitable v
    JOIN mongodb01.mysql_ammu_chtable c ON v.Playlist_id = c.Playlist_id
    where YEAR(Published_At) < 2023
    UNION
    SELECT c.Channel_Name, v.Published_At
    FROM mongodb01.mysql_back_vitable v
    JOIN mongodb01.mysql_back_chtable c ON v.Playlist_id = c.Playlist_id
    where YEAR(Published_At) < 2023
    UNION
    SELECT c.Channel_Name, v.Published_At
    FROM mongodb01.mysql_fire_vitable v
    JOIN mongodb01.mysql_fire_chtable c ON v.Playlist_id = c.Playlist_id
    where YEAR(Published_At) < 2023
    UNION
    SELECT c.Channel_Name, v.Published_At
    FROM mongodb01.mysql_gran_vitable v
    JOIN mongodb01.mysql_gran_chtable c ON v.Playlist_id = c.Playlist_id
    where YEAR(Published_At) < 2023
    UNION
    SELECT c.Channel_Name, v.Published_At
    FROM mongodb01.mysql_irfa_vitable v
    JOIN mongodb01.mysql_irfa_chtable c ON v.Playlist_id = c.Playlist_id
    where YEAR(Published_At) < 2023
    UNION
    SELECT c.Channel_Name, v.Published_At
    FROM mongodb01.mysql_khal_vitable v
    JOIN mongodb01.mysql_khal_chtable c ON v.Playlist_id = c.Playlist_id
    where YEAR(Published_At) < 2023
    UNION
    SELECT c.Channel_Name, v.Published_At
    FROM mongodb01.mysql_mone_vitable v
    JOIN mongodb01.mysql_mone_chtable c ON v.Playlist_id = c.Playlist_id
    where YEAR(Published_At) < 2023
    UNION
    SELECT c.Channel_Name, v.Published_At
    FROM mongodb01.mysql_tami_vitable v
    JOIN mongodb01.mysql_tami_chtable c ON v.Playlist_id = c.Playlist_id
    where YEAR(Published_At) < 2023
    
    ) AS combined_results
    ORDER BY Channel_Name DESC;
    """
    mysql_cursor.execute(sql_query08)
    
    # Fetch the result into a Pandas DataFrame
    result = mysql_cursor.fetchall()
    q8df = pd.DataFrame(result, columns=['Channel_name', 'Views'])
    # print("SQL - q3df")
    #
    return q8df

#
# ----------------------------------------

def sql_q9(): # 9.whats the average duration ofall videos in eachchannel, & what'r their corresponding channelsnames?
    sql_query09 = f"""SELECT Channel_Name, Duration
    FROM (
    SELECT c.Channel_Name, v.Duration
    FROM mongodb01.mysql_ammu_vitable v
    JOIN mongodb01.mysql_ammu_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Duration
    FROM mongodb01.mysql_back_vitable v
    JOIN mongodb01.mysql_back_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Duration
    FROM mongodb01.mysql_fire_vitable v
    JOIN mongodb01.mysql_fire_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Duration
    FROM mongodb01.mysql_gran_vitable v
    JOIN mongodb01.mysql_gran_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Duration
    FROM mongodb01.mysql_irfa_vitable v
    JOIN mongodb01.mysql_irfa_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Duration
    FROM mongodb01.mysql_khal_vitable v
    JOIN mongodb01.mysql_khal_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Duration
    FROM mongodb01.mysql_mone_vitable v
    JOIN mongodb01.mysql_mone_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Duration
    FROM mongodb01.mysql_tami_vitable v
    JOIN mongodb01.mysql_tami_chtable c ON v.Playlist_id = c.Playlist_id
    
    ) AS combined_results
    ORDER BY Duration asc limit 20;
    """
    mysql_cursor.execute(sql_query09)
    
    # Fetch the result into a Pandas DataFrame
    result = mysql_cursor.fetchall()
    q9df = pd.DataFrame(result, columns=['Channel_Name','Duration'])
    # print("SQL - q3df")
    #
    return q9df

    
def sql_q10(): # 10.which videos have highest no of comments, and what'r their corresponding channelnames?
    sql_query10 = f"""SELECT Channel_Name, COUNT(Comment_id) AS comment
    FROM (
    SELECT c.Channel_Name, v.Comment_id
    FROM mongodb01.mysql_ammu_cctable v
    JOIN mongodb01.mysql_ammu_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Comment_id
    FROM mongodb01.mysql_back_cctable v
    JOIN mongodb01.mysql_back_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Comment_id
    FROM mongodb01.mysql_fire_cctable v
    JOIN mongodb01.mysql_fire_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Comment_id
    FROM mongodb01.mysql_gran_cctable v
    JOIN mongodb01.mysql_gran_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Comment_id
    FROM mongodb01.mysql_irfa_cctable v
    JOIN mongodb01.mysql_irfa_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Comment_id
    FROM mongodb01.mysql_khal_cctable v
    JOIN mongodb01.mysql_khal_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Comment_id
    FROM mongodb01.mysql_mone_cctable v
    JOIN mongodb01.mysql_mone_chtable c ON v.Playlist_id = c.Playlist_id
    UNION
    SELECT c.Channel_Name, v.Comment_id
    FROM mongodb01.mysql_tami_cctable v
    JOIN mongodb01.mysql_tami_chtable c ON v.Playlist_id = c.Playlist_id
    ) AS combined_results
    GROUP BY Channel_Name
    ORDER BY comment DESC;
    """
    mysql_cursor.execute(sql_query10)
    
    # Fetch the result into a Pandas DataFrame
    result = mysql_cursor.fetchall()
    q10df = pd.DataFrame(result, columns=['Channel_Name', 'Comment_id'])
    # print("SQL - q3df")
    #
    return q10df

#
# ----------------------------------------
#
