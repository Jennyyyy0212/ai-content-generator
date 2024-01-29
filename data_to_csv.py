# %%
import pandas as pd
import sqlite3

# %%
class BlogDataToDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('test_blog_data.db')  # SQLite database

        # Create a table for the blog data if it doesn't exist
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS test_blog_data (
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
        ''')

    def add_blog_entry(self, name, post_body, post_summary, main_image, thumbnail_image, meta_title, meta_description, image_alt_text, tag, reading_time):
        # Insert data into the database
        self.conn.execute('''
            INSERT INTO test_blog_data (Name, Slug, Collection_ID, Item_ID, Created_On, Updated_On, Published_On, Post_Body, Post_Summary, Main_Image, Thumbnail_Image, Featured, Color, Meta_Title, Meta_Description, Image_Alt_Text, Tag, Reading_Time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, "", "", "", "", "", "", post_body, 
              post_summary, main_image, thumbnail_image, False, "", meta_title, meta_description, 
              image_alt_text, tag, reading_time))
        # Commit the changes
        self.conn.commit()

    def close_database(self):
        # Close the database connection
        self.conn.close()

# %%
class BlogDataToCSV:
    def __init__(self, database_filename, csv_filename):
        self.database_filename = database_filename
        self.csv_filename = csv_filename

    def export_to_csv(self):
        # Retrieve data from the database and export it to CSV
        conn = sqlite3.connect(self.database_filename)
        query = "SELECT * FROM test_blog_data"
        df = pd.read_sql_query(query, conn)
        df.to_csv(self.csv_filename, index=False)

        # Close the database connection
        conn.close()


