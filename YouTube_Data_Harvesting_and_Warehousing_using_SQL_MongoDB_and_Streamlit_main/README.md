# YouTube-Data-Harvesting-and-Warehousing-using-SQL-MongoDB-and-Streamlit

Project Title:
YouTube Data Harvesting and Warehousing using SQL, MongoDB and Streamlit

Skills take away From This Project:
Python scripting, Data Collection,MongoDB, Streamlit, API integration, Data Managment using MongoDB (Atlas) and SQL.

Domain : Social Media (YouTube)

Problem Statement:

The problem statement is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels. 
The application has the following features.

1.Ability to input a YouTube channel ID and retrieve all the relevant data 
(Channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, comments of each video) using Google API.

2.Automatically / Option to store the data in a MongoDB database as a data lake.

3.Ability to collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button.

4.Automatically / Option to select a channel name and migrate its data from the data lake to a SQL database as tables.

5.Ability to search and retrieve data from the SQL database using different search options, including joining tables to get channel details.

Installation:

1.Clone the repository: 

git clone https://github.com/MaathanMethil/YouTube-Data-Harvesting-and-Warehousing-using-SQL-MongoDB-and-Streamlit

Obtain API credentials:

1.Go to the Google Developers Console.

2.Create a new project or select an existing project.

3.Enable the YouTube Data API v3.

Configuration:

1.Open the mainfile.py file in the project directory.

2.Set the desired configuration options:

3.Specify your YouTube API key.

4.Choose the database connection details (SQL and MongoDB).

5.Get the Youtube Channel ID from the Youtube's sourcepage

6.provide the Youtube Channel ID data to be harvested.

7.Set other configuration options as needed.


Usage:

1.Launch the Streamlit app: streamlit run mainfile.py

2.Run the mainfile.py script, make sure you have main and sql files in the same folder.

3.The app will start and open in your browser. You can explore the harvested YouTube data and visualize the results.


Contributing:

Contributions are welcome! If you want to contribute to this project, please follow these steps:

1.Fork the repository.

2.Create a new branch: "git checkout -b feature/your-feature-name"

3.Make your modifications and commit the changes: "git commit -m "Add your commit message here"

4.Push your branch: "git push origin feature/your-feature-name"

5.Open a pull request on the GitHub repository, explaining the changes you made and why they should be merged.


Acknowledgments:

If you have any questions, suggestions, or feedback, please feel free to contact us at maathanrmethil94@gmail.com

We appreciate your interest in our project!
Thank you.




