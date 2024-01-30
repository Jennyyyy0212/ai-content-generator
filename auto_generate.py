# %%
from data_to_csv import *
from info_generator import ContentCreator
from content import ArticleGenerator
#import info_generator, data_to_csv
import logging

# %%
class AutoGenerator:
    def __init__(self, db_file_name):
        self.content_generator = None
        self.info_generator = None
        self.database_generator = None
        self.csv_geneator = None
        self.link = None
        self.keyword = None
        self.db_file_name = db_file_name

        # Configure logging
        logging.basicConfig(filename='autogenerate.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    
    def close(self):
        self.database_generator.close_database()

    def create(self,link, keyword):
        try:
            self.info_generator = ContentCreator()
            self.info_generator.generate_info_from_content(link, keyword)
            self.link = link
            self.keyword = keyword
            self.content_generator = self.info_generator.content_generator
            self.database_generator = BlogDataToDatabase(self.db_file_name)
            self.database_generator.add_blog_entry(self.info_generator.title, self.info_generator.html_content, self.info_generator.post_summary, self.info_generator.main_t_image, self.info_generator.main_t_image, self.info_generator.meta_title, self.info_generator.meta_description, self.info_generator.image_alt_text, self.info_generator.tag, self.info_generator.read_time_str) 
            self.database_generator.insert_json_data_to_db(self.content_generator.get_metadata())
            logging.info("Content added successfully.")
        except Exception as e:
            logging.error(f"Error during data creation: {str(e)}")

    def export(self):
        try:
            self.csv_geneator = BlogDataToCSV(self.db_file_name)
            self.csv_geneator.export_to_csv()
            self.close()
            logging.info("Export completed successfully.")
        except Exception as e:
            logging.error(f"Error during export: {str(e)}")

    def get_content_generate_result(self):
        return self.content_generator.get_all_results()


