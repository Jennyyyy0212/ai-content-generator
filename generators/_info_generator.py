from ._content import ArticleGenerator  # Import all from the 'content' module
import openai                   # Import the 'openai' package for using the OpenAI API
import markdown                 # Import the 'markdown' package for working with Markdown text
import re                       # Import the 're' module for regular expressions
import os                       # Import the 'os' module for interacting with the operating system
from dotenv import load_dotenv, find_dotenv 
# Import the 'load_dotenv' and 'find_dotenv' functions from the 'dotenv' package

_ = load_dotenv(find_dotenv())  # Load environment variables from a '.env' file (if found)

os.environ['OPENAI_API_KEY'] = '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'
openai.api_key  = os.getenv('OPENAI_API_KEY')

class ContentCreator:
    """
    This class is responsible for generating content and metadata for blog posts.
    It uses OpenAI's GPT-3 model for content generation.
    """

    TAG_LIST =[
        "A/B Testing",             # For articles related to A/B testing experiments and techniques
        "E-commerce",              # For blogs about online retail and e-commerce strategies
        "Conversion Optimization", # For content on optimizing conversion rates and sales
        "Marketing Strategies",    # For posts discussing various marketing approaches
        "Online Retail",           # For articles focusing on the online retail industry
        "Consumer Behavior",       # For blogs exploring consumer psychology and behavior
        "Pricing Strategies",      # For content on pricing strategies and tactics
        "Shopify Tips",            # For tips and advice specific to Shopify users
        "Website Optimization",    # For blogs about optimizing websites for better performance
        "Data Analytics",          # For articles on data analysis and its applications
        "Marketing Insights",      # For sharing insights and trends in marketing
        "E-commerce Trends",       # For posts discussing emerging trends in e-commerce
        "Testing Methods",         # For content on various testing and experimentation methods
        "Business Growth",         # For blogs related to business growth strategies
        "Digital Marketing",       # For articles covering digital marketing topics
        "User Experience",         # For content focused on improving user experience
        "Data-driven Decisions",   # For posts emphasizing data-driven decision-making
        "Online Sales",            # For blogs about strategies to boost online sales
        "Marketing Tactics",       # For articles on specific marketing tactics and techniques
        "Retail Strategies"        # For content on retail strategies, both online and offline
    ]

    # Average reading speed in words per minute
    WORDS_PER_MINUTE = 250  # You can adjust this based on your audience's reading speed

    def __init__(self):
        """
        Initialize the ContentCreator instance.

        Attributes:
            client (OpenAI): The OpenAI API client.
            keyword (str): The keyword for the content.
            title (str): The title of the generated content.
            content (str): The generated content.
            html_content (str): The generated content in HTML format.
            main_t_image (str): The main article image link.
            meta_title (str): The SEO-friendly meta title.
            meta_description (str): The SEO-friendly meta description.
            image_alt_text (str): The image alt text.
            tag (str): The assigned tag for the article.
            read_time (int): The estimated reading time in minutes.
            read_time_str (str): The reading time as a string (e.g., "5 mins").
            content_generator (ArticleGenerator): An instance of the ArticleGenerator class.
        """
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
        self.keyword = None
        self.title = None
        self.content = None
        self.html_content = None
        self.main_t_image = None
        self.meta_title = None
        self.meta_description = None
        self.image_alt_text = None
        self.tag = None
        self.read_time = None
        self.read_time_str = None
        self.content_generator = None


    # normal prompt generation 
    def _get_completion(self,prompt):
        """
        Get a completion from the GPT-3 model based on the provided prompt.

        Args:
            prompt (str): The prompt for generating content.

        Returns:
            str: The generated content.
        """
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content
    
    def _remove_quote(self, text):
        """
        Remove quotes from the beginning and end of a text.

        Args:
            text (str): The text to remove quotes from.

        Returns:
            str: The text without quotes.
        """
        return text.strip('"')

    def split_markdown_title_content(self, markdown_text):
        """
        Split Markdown text into title and content.
        Assumes the first line is the title, marked with '#'.

        Args:
            markdown_text (str): The Markdown text to split.

        Returns:
            tuple: A tuple containing the title and content.
        """
        self.title, self.content = markdown_text.split('\n', 1)
        self.title = self.title[2:] if self.title.startswith('# ') else self.title

        return self.title, self.content
    
    def convert_markdown_to_html(self,markdown_content):
        """
        Convert Markdown text to HTML.

        Args:
            markdown_content (str): The Markdown content to convert.

        Returns:
            str: The HTML content.
        """
        self.html_content = markdown.markdown(markdown_content)
        return self.html_content
    
    def generate_post_summary(self,abstract):
        """
        Generate a post summary between 20 and 50 words based on the provided abstract.

        Args:
            abstract (str): The abstract of the article.

        Returns:
            str: The generated post summary.
        """
        prompt = f"""
            rewrite a SEO-friendly and engaging post summary between 20 and 50 words for the following text:  
            ```{abstract}```

            return the post summary only.
            """
        self.post_summary = self._remove_quote(self._get_completion(prompt))
        return self.post_summary
    
    def generate_meta_title(self):
        """
        Generate a clickable article title based on the provided outline and keyword.

        Returns:
            str: The generated meta title.
        """
        prompt = f"""
        rewrite a SEO-friendly and engaging meta title between 60 and 64 characters and include the ```{self.keyword}``` for the following text:  
        title: ```{self.title}```

        return the meta title only.
        """
        self.meta_title = self._remove_quote(self._get_completion(prompt))
        return self.meta_title
    
    def generate_meta_description(self):
        """
        Generate a SEO-friendly and engaging meta description based on the article content.

        Returns:
            str: The generated meta description.
        """
        prompt = f"""
        Write a SEO-friendly and engaging meta description between 150 and 154 characters based on article.
        When writing meta description:
        1. Include a call to action within your Meta Description to give your reader a clear instruction of what action to take and what’s in it for them.
        2. Include the ```{self.keyword}``` 
        3.Provide just enough information to explain what the page is about but not so much that it ruins the curiosity factor.

        article : ```{self.content}```

        return the meta description only.
        """
        self.meta_description = self._remove_quote(self._get_completion(prompt))
        return self.meta_description
    
    # create image alt text
    def generate_image_alt_text(self, abstract):
        """
        Generate image alt text based on the provided abstract.

        Args:
            abstract (str): The abstract that generated the image.

        Returns:
            str: The generated image alt text.
        """
        prompt = f"""
            create a image alt text by the abstract that generated the image within 125 characters: ```{abstract}```

        """
        self.image_alt_text = self._remove_quote(self._get_completion(prompt))
        return self.image_alt_text
    
    # assign the tag into article 
    def assign_tag(self):
        """
        Assign a relevant tag to the article based on its content.

        Returns:
            str: The assigned tag.
        """
        prompt = f"""
            Suggest one relevant tag within the tag list for the following article: ```{self.content}```

            tag list: ```{self.TAG_LIST}

            return tag text only
        """
        self.tag = self._get_completion(prompt)
        return self.tag
    
    def calculate_read_time(self):
        """
        Calculate the estimated reading time of the article.

        Returns:
            int: The estimated reading time in minutes.
        """
        words = re.findall(r'\w+', self.content)
        word_count = len(words)

        # Calculate the estimated read time in minutes
        read_time_minutes = word_count / self.WORDS_PER_MINUTE

        # Round up to the nearest minute
        read_time_minutes = round(read_time_minutes)
        self.read_time = read_time_minutes
        return self.read_time
    
    def generate_info_from_content(self, input_link, keyword):
        """
        Generate information and metadata from the content provided by the ArticleGenerator.

        Args:
            input_link (str): The input link to fetch content from.
            keyword (str): The keyword associated with the content.

        Returns:
            tuple: A tuple containing information and metadata about the content.
        """
        self.content_generator = ArticleGenerator()
        self.content_generator.run(input_link,keyword)
        self.keyword = keyword
        article = self.content_generator.get_article()
        abstract = self.content_generator.get_abstract()

        self.split_markdown_title_content(article)
        self.convert_markdown_to_html(self.content)
        self.main_t_image = self.content_generator.get_picture_link()
        self.generate_post_summary(abstract)
        self.generate_meta_title()
        self.generate_meta_description()
        self.generate_image_alt_text(abstract)
        self.assign_tag()
        self.read_time_str = str(self.calculate_read_time()) + " mins"

        return self.title, self.content, self.html_content, self.main_t_image, self.meta_title, \
            self.meta_description, self.image_alt_text, self.tag, self.read_time, self.read_time_str