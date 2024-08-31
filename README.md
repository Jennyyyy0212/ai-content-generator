# AI content generator project - AutoGenerator

## Problem Statement

Writing high-quality content that is optimized for search engines can be time-consuming and challenging. This project aims to automate the content generation process by leveraging AI techniques to generate relevant and engaging content based on given keyword-link pairs.


## Goals

The goal of this project is to develop an AI Content Generator that can generate SEO-oriented content based on pairs of links and keywords. The generated content can be used for various purposes such as blog posts, articles, or website content.


## Content Generation and CSV Export

The **AutoGenerator** class is designed to automate the process of content generation based on a provided pairs of link and keyword. The generated content is then stored in an SQLite database and exported to two CSV files for easy integration with platforms like Webflow and the meta data of contents. This project utilizes the OpenAI GPT-3.5 model for efficient and dynamic content creation. (OpenAI key is included.)

The `AutoGenerator` class handles the creation of SEO-oriented content based on the provided keyword-link pairs and exports the information into two respective CSV files.

## Features

- **Content Generation**: The project leverages the `ContentCreator` class to generate informative and engaging content by utilizing a pair of link and keyword inputs.

- **Database Integration**: The generated content is stored in an SQLite database for structured data management.

- **CSV Export**: The data stored in the database can be seamlessly exported to a CSV file using the `BlogDataToCSV` class, providing a convenient way to integrate the content with various platforms.

- **Logging**: The project includes a logging mechanism to capture and log errors or successful operations during content creation and export processes. Logs are stored in the 'autogenerate.log' file.

## AutoGenerator Class Methods:

#### `create(link: str, keyword: str) -> None`

Generates SEO-oriented content for the given link and keyword pair.

#### `export() -> None`

Exports the generated content and meta-data from the database into CSV files.

**Note**: `export()` will generate 2 csv file.
- XXX_data_table.csv : A csv file that can import to Webflow CMS directly 
- XXX_meta_table.csv : A csv file that can show the geneated aticle information(Include: 'title', 'blog picture link', 'primary keyword', 'other_keywords', 'funnel', 'minutes' ,'date','reference'.)
- `Title` column is the key column for both file


## Installation

Follow these steps to install and set up the AI Content Generator:

1. Clone the repository:

    ```bash
    git clone https://github.com/Jennyyyy0212/ai-content-generator.git
    ```

2. Navigate to the project directory(for example):

    ```bash
    cd ai-content-generator
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the configuration:

    Copy the sample configuration file and edit it with your preferences:

    ```bash
    cp config.example.json config.json
    ```

    Open `config.json` in a text editor and update the necessary settings.

## Usage

The AI Content Generator allows you to generate SEO-oriented content based on pairs of links and keywords. Use the provided `auto_generate.py` script, which includes the `AutoGenerator` class, to automate this process.

### Example Usage 
#### In terminal 
1. Ensure you are in the project directory:

    ```bash
    cd ai-content-generator
    ```
2. Create a python script
3. Revise below infomation on the script 
   ```python
   # Example in G.py
   from generators.auto_generate import AutoGenerator
      
   # Create an instance of the AutoGenerator class with the desired database name
   g = AutoGenerator('blog_name.db')
      
   # Define keyword-link pairs
   keyword_link_pairs = [
      ("keyword 1", "link 1"),
      ("keyword 2", "link 2"),
      ("keyword 3", "link 3"),
      ("keyword 4", "link 4"),
      ("keyword 5", "link 5"),
      # Add more pairs as needed
      ]
   # Iterate over the pairs and generate content for each
   for keyword, link in keyword_link_pairs:
       g.create(link, keyword)
       # Do something with the generated content, e.g., save it to a file or database
   
   # Export the information from the database into CSV files
   g.export()
   ```
4. Run the script:
   ```bash
    python YOUR_PYTHON_SCRIPT_NAME.py
    ```
#### In python
1. Create a python script and ensure in the project directory
2. Open the python editor.Ex: VS code, Jupyter Notebook
3. Run the below infomation on the script:
   ```python
   # Example in G.py
   from generators.auto_generate import AutoGenerator
      
   # Create an instance of the AutoGenerator class with the desired database name
   g = AutoGenerator('blog_name.db')
      
   # Define keyword-link pairs
   keyword_link_pairs = [
      ("keyword 1", "link 1"),
      ("keyword 2", "link 2"),
      ("keyword 3", "link 3"),
      ("keyword 4", "link 4"),
      ("keyword 5", "link 5"),
      # Add more pairs as needed
      ]
   # Iterate over the pairs and generate content for each
   for keyword, link in keyword_link_pairs:
       g.create(link, keyword)
       # Do something with the generated content, e.g., save it to a file or database
   
   # Export the information from the database into CSV files
   g.export()
   ```



# Developer Note

Generated by: Jenny

## Research Steps
1. `_content.py`: use openAI to read a outline from a link and generate the article with the metadata of developed article

    **main function**: 
    - `run(input_link,keyword)`: Run the entire content generation process including article, abstract, and image generation.
    - `get_all_results()`: Print the generated article, image link, and metadata.

2. `_info_generator.py`: turn the generated article from `content.py` to the field data that import to Webflow later

    **main function**: 
    - `generate_info_from_content(input_link, keyword): Generate field data that will import to webflow

3. `_data_to_csv.py`: manage data in an SQLite database for a blog and export data from an SQLite database to CSV files.

    **main function**: 
    - `add_blog_entry(name, post_body, post_summary, main_image, thumbnail_image, meta_title, meta_description, image_alt_text, tag, reading_time)`: Add a new blog entry to the database.
    - `insert_json_data_to_db(json_data_str, table_name)`: Insert JSON data into the meta table of the database.
    - `export_to_csv()`: Export data from the database to CSV files.

4. `auto_generator.py`: combine all above Python script to generate content from a pair of link and keyword and export it to a CSV file.

    **main function**: 
    - `create(input_link, keyword)`: generate and store content based on a link and keyword.
    - `export()`: turn all generated data to csv file
    - `get_content_generate_result()`:get the developed article result


## Improvement

Here are some potential areas for improvement in the AI Content Generator:

- Turn the openAI-created image directly upload by the .jpg link (Stop. Curently haven't found a solution and need human work. Arleady tried by Amazon S3 bucket. )
- Fine-turning content (In-Progress in Future Update section)
- Train database to use RAG and LLM (In-Progress in Future Update section)
- Implement a user-friendly interface for easier configuration and usage.
- Add support for different languages and writing styles.
- Optimize the content generation process for better performance.
- Incorporate feedback mechanisms to improve the quality of generated content. (In-Progress in Future Update section)

Feel free to contribute to the project by addressing these improvements or suggesting new ones!

## Future Update
### Fine-turning content
See more information in another folder: https://github.com/ABConvert/ai-content-generator/tree/master/langchain_test_folder

### Train database to use RAG and LLM
See more information in another repo: https://github.com/Jennyyyy0212/cro-web-discoverer
