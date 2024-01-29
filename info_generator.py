# %%
#%pip install markdown
from content import *
import openai
import markdown
import re
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

os.environ['OPENAI_API_KEY'] = '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'
openai.api_key  = os.getenv('OPENAI_API_KEY')

# %%
class ContentCreator:
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


    def reset(self, keyword, content_generator):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
        self.keyword = keyword
        self.content_generator = content_generator
        self.title = None
        self.content = None

    # normal prompt generation 
    def _get_completion(self,prompt):
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content
    
    def _remove_quote(self, text):
        return text.strip('"')

    def split_markdown_title_content(self, markdown_text):
        """
        Split Markdown text into title and content.
        Assumes the first line is the title, marked with '#'.
        """
        self.title, self.content = markdown_text.split('\n', 1)
        self.title = self.title[2:] if self.title.startswith('# ') else self.title

        return self.title, self.content
    
    def convert_markdown_to_html(self,markdown_content):
        """
        Convert Markdown text to HTML: 
        """
        self.html_content = markdown.markdown(markdown_content)
        return self.html_content
    
    def generate_post_summary(self,abstract):
        prompt = f"""
            rewrite a SEO-friendly and engaging post summary between 20 and 50 words for the following text:  
            ```{abstract}```

            return the post summary only.
            """
        self.post_summary = self._remove_quote(self._get_completion(prompt))
        return self.post_summary
    
    def generate_meta_title(self):
        # generate a clickable article title based on the provided outline and keyword.

        prompt = f"""
        rewrite a SEO-friendly and engaging meta title between 60 and 64 characters and include the ```{self.keyword}``` for the following text:  
        title: ```{self.title}```

        return the meta title only.
        """
        self.meta_title = self._remove_quote(self._get_completion(prompt))
        return self.meta_title
    
    def generate_meta_description(self):

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

            prompt = f"""
            create a image alt text by the abstract that generated the image within 125 characters: ```{abstract}```

            """
            self.image_alt_text = self._remove_quote(self._get_completion(prompt))
            return self.image_alt_text
    
    # assign the tag into article 
    def assign_tag(self):

            prompt = f"""
            Suggest one relevant tag within the tag list for the following article: ```{self.content}```

            tag list: ```{self.TAG_LIST}

            return tag text only
            """
            self.tag = self._get_completion(prompt)
            return self.tag
    
    def calculate_read_time(self):
        # Count words in the text (using a simple regex pattern)
        words = re.findall(r'\w+', self.content)
        word_count = len(words)

        # Calculate the estimated read time in minutes
        read_time_minutes = word_count / self.WORDS_PER_MINUTE

        # Round up to the nearest minute
        read_time_minutes = round(read_time_minutes)
        self.read_time = read_time_minutes
        return self.read_time
    
    def generate_info_from_content(self, input_link, keyword):
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
        


    


