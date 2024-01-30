# %%
import pandas as pd
import sqlite3
import json
import os

# %%
class BlogDataToDatabase:
    def __init__(self, database_filename):
        self.conn = sqlite3.connect(database_filename)  # SQLite database
        table_prefix = os.path.splitext(database_filename)[0]
        self.data_table = f"{table_prefix}_data_table"
        self.meta_table = f"{table_prefix}_meta_table"
        # Create a table for the blog data if it doesn't exist
        create_data_table_query = '''
            CREATE TABLE IF NOT EXISTS {} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Slug TEXT,
                Collection_ID TEXT,
                Item_ID TEXT,
                Created_On TEXT,
                Updated_On TEXT,
                Published_On TEXT,
                Post_Body TEXT,
                Post_Summary TEXT,
                Main_Image TEXT,
                Thumbnail_Image TEXT,
                Featured BOOLEAN,
                Color TEXT,
                Meta_Title TEXT,
                Meta_Description TEXT,
                Image_Alt_Text TEXT,
                Tag TEXT,
                Reading_Time TEXT
            )
        '''.format(self.data_table)

        self.conn.execute(create_data_table_query)

        create_meta_table_query = '''
            CREATE TABLE IF NOT EXISTS {} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                blog_picture_link TEXT,
                primary_keyword TEXT,
                other_keywords TEXT,
                funnel TEXT,
                minutes REAL,
                date TEXT,
                reference TEXT
            )
        '''.format(self.meta_table)
        self.conn.execute(create_meta_table_query)

    def add_blog_entry(self, name, post_body, post_summary, main_image, thumbnail_image, meta_title, meta_description, image_alt_text, tag, reading_time):
        # Insert data into the database
        insert_sql = '''
            INSERT INTO {} (Name, Slug, Collection_ID, Item_ID, Created_On, Updated_On, Published_On, Post_Body, Post_Summary, Main_Image, Thumbnail_Image, Featured, Color, Meta_Title, Meta_Description, Image_Alt_Text, Tag, Reading_Time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''.format(self.data_table)

        self.conn.execute(insert_sql, (name, "", "", "", "", "", "", post_body, 
                                    post_summary, main_image, thumbnail_image, False, "", meta_title, meta_description, 
                                    image_alt_text, tag, reading_time))
        
        # Commit the changes
        self.conn.commit()

    def insert_json_data_to_db(self, json_data_str):
        try:
            # # Parse the JSON data
            # data = json.loads(json_data)

            # # Connect to the SQLite database
            # cursor = self.conn.cursor()
            # # Create a list of column names and placeholders
            # columns = ', '.join(data.keys())
            # placeholders = ', '.join(['?'] * len(data))

            # # Construct the SQL INSERT statement
            # insert_sql = f"INSERT INTO {self.meta_table} ({columns}) VALUES ({placeholders})"

            # # Insert the data into the table
            # cursor.execute(insert_sql, tuple(data.values()))
            json_data = json.loads(json_data_str)

            insert_sql = '''
                INSERT INTO {} (title, blog_picture_link, primary_keyword, other_keywords, funnel, minutes, date, reference) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''.format(self.meta_table)

            self.conn.execute(insert_sql, (
                json_data.get('title', ''),
                json_data.get('blog picture link', ''),
                json_data.get('primary keyword', ''),
                json.dumps(json_data.get('other_keywords', [])),  # Convert the list to a JSON string
                json_data.get('funnel', ''),
                json_data.get('minutes', 0),  # Default value if 'minutes' is missing or not a number
                json_data.get('date', ''),
                json_data.get('reference', '')
            ))

            # Commit the transaction and close the connection
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting JSON data: {str(e)}")


    def close_database(self):
        # Close the database connection
        self.conn.close()

# %%
class BlogDataToCSV:
    def __init__(self, database_filename):
        self.database_filename = database_filename
        table_prefix = os.path.splitext(database_filename)[0]
        self.data_table = f"{table_prefix}_data_table"
        self.meta_table = f"{table_prefix}_meta_table"
        self.csv_data_filename = f"{self.data_table}_data.csv"
        self.csv_meta_filename = f"{self.meta_table}_data.csv"

    
    def export_to_csv(self):
        # Retrieve data from table1 and export it to CSV1
        conn = sqlite3.connect(self.database_filename)
        query1 = "SELECT * FROM {self.date_table}"
        df1 = pd.read_sql_query(query1, conn)
        df1.to_csv(self.csv_data_filename, index=False)

        # Retrieve data from table2 and export it to CSV2
        query2 = f"SELECT * FROM {self.meta_table}"
        df2 = pd.read_sql_query(query2, conn)
        df2.to_csv(self.csv_meta_filename, index=False)

        # Close the database connection
        conn.close()

