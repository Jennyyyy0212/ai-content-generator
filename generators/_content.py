import openai               # Import the OpenAI Python library
import os                   # Import the os module for operating system-related functions
import time                 # Import the time module for handling timestamps
import datetime             # Import the datetime module for date-related operations
import random               # Import the random module for generating random values
from openai import OpenAI   # Import the OpenAI class from the OpenAI library

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

os.environ['OPENAI_API_KEY'] = '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'

openai.api_key = os.getenv('OPENAI_API_KEY')

class ArticleGenerator:
    """
        ArticleGenerator class generates articles, abstracts, and images for blog content.
        It utilizes the OpenAI API for content generation and image creation.

        Attributes:
            client (OpenAI): An instance of the OpenAI client.
            total_start_time (float): The timestamp when the generation process starts.
            today_date (datetime.date): The current date.
            outline (str): The article outline obtained from a given link.
            new_outline (str): A revised article outline with a clickable title.
            other_keywords (str): Related keywords for the article content.
            level (str): The funnel level for targeting the audience.
            selected_funnel (str): The selected funnel description.
            full_article (str): The generated full article content.
            image_link (str): The link to the blog picture.
            abstract (str): A short abstract of the article.
            metadata (str): JSON data structure containing metadata about the generated content.
    """

    top_funnel = f""" 
    Prospective Shopify owners and e-commerce enthusiasts who are relatively new to the online selling landscape. 
    They may be exploring entrepreneurship opportunities, seeking to set up their first online store, or looking for ways to enhance their existing store. 
    This group values simplicity and is eager to grasp the basics of e-commerce and A/B testing without diving too deep into technicalities. 
    Their main goals include understanding the fundamentals of e-commerce, learning about Shopify, and gaining insights into the potential of A/B testing to optimize their store's performance. 
    """

    middle_funnel = f""" 
    E-commerce merchants in the growth phase who are actively looking to improve their Conversion Rate Optimization (CRO). 
    This segment comprises business owners and marketing professionals with a moderate level of experience in running online stores. 
    They are interested in detailed insights, case studies, and industry trends to implement effective CRO strategies. 
    They appreciate practical guides, checklists, and analytics insights to optimize their conversion rates.
    """

    bottom_funnel = f""" 
    Experienced e-commerce professionals, marketers, and business owners who are well-versed in A/B testing but are now seeking advanced techniques and tools. 
    This segment is specifically interested in service demos, sophisticated A/B testing frameworks, and understanding the psychology behind user behavior. 
    They want to stay ahead of the curve with tools that offer in-depth analytics and insights. 
    This group may also have a keen interest in ethical considerations and privacy aspects related to A/B testing.
    """

    funnel_list = {'top':top_funnel, 'middle': middle_funnel, 'bottom': bottom_funnel}

    def __init__(self):
        """
        Initializes an instance of the ArticleGenerator class, which generates articles, abstracts, and images for blog content using the OpenAI API.

        Attributes:
            client (OpenAI): An instance of the OpenAI client.
            total_start_time (float): The timestamp when the generation process starts.
            today_date (datetime.date): The current date.
            outline (str): The article outline obtained from a given link.
            new_outline (str): A revised article outline with a clickable title.
            other_keywords (str): Related keywords for the article content.
            level (str): The funnel level for targeting the audience.
            selected_funnel (str): The selected funnel description.
            full_article (str): The generated full article content.
            image_link (str): The link to the blog picture.
            abstract (str): A short abstract of the article.
            metadata (str): JSON data structure containing metadata about the generated content.

        Initializes the ArticleGenerator with necessary attributes, including an instance of the OpenAI client, timestamps, and placeholders for various content components.
        """
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
        self.total_start_time = None
        self.today_date = None
        self.outline = None
        self.new_outline = None
        self.other_keywords = None
        self.level = None
        self.selected_funnel = None
        self.full_article = None
        self.image_link = None
        self.abstract = None
        self.metadata = None
        self.duration = None

    def _get_completion(self, prompt):
        """
        Get a completion response from the OpenAI API based on the provided prompt.

        Args:
            prompt (str): The input prompt for content generation.

        Returns:
            str: The generated content as a response to the prompt.
        """
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            temperature=0 #update the temperature from 0 to 1 to make randomness
        )
        return response.choices[0].message.content

    def _reset(self):
        """
        Reset the instance attributes to their default values.
        """
        self.total_start_time = None
        self.today_date = None
        self.outline = None
        self.new_outline = None
        self.other_keywords = None
        self.level = None
        self.selected_funnel = None
        self.full_article = None
        self.image_link = None
        self.abstract = None
        self.metadata = None
        self.duration = None
    

    def _get_outline(self, website_link):
        """
        Obtain an article outline based on a provided website link.

        Args:
            website_link (str): The link to the source article.

        Returns:
            str: The generated article outline.
        """
        prompt = f"""
        create an outline based on the article link
        ```{website_link}```
        """
        self.outline = self._get_completion(prompt)
        return self.outline
    

    def _generate_new_outline(self, keyword):
        """
        Generate a new article outline with a clickable title based on the provided outline and keyword.

        Args:
            keyword (str): The primary keyword for the article.

        Returns:
            str: The revised article outline with a clickable title.
        """

        prompt = f"""
        Based on the outline, create a clickable article title that included the keyword and revise the outline to be used in my owm article based on revised title \
        It shouldn't include any other brand service or product. 
        keyword: ```{keyword}```
        outline: ```{self.outline}```
        """
        self.new_outline = self._get_completion(prompt)
        return self.new_outline

    def _generate_keyword(self, keyword):
        """
        Generate 10 related keywords for the article content based on the new outline.

        Args:
            keyword (str): The primary keyword for the article.
            new_outline (str): The revised article outline with a clickable title.

        Returns:
            str: Related keywords for the article content.
        """

        prompt = f"""
        Based on the new outline, list some keywords that related the content and title in total of 10. Do not include the primpary keyword.
        primary keyword: ```{keyword}```
        outline: ```{self.new_outline}```
        """
        self.other_keywords = self._get_completion(prompt)
        return self.other_keywords
    
    def _get_funel(self):
        """
        Get a funnel description based on the provided level.

        Args:
            level (str): The funnel level (top, middle, or bottom).

        Returns:
            str: The funnel description.
        """
        self.selected_funnel = self.funnel_list.get(self.level)
        return self.selected_funnel

    def _get_funel_level(self):
        """
        Get a random funnel level (top, middle, or bottom).

        Returns:
            str: A randomly selected funnel level.
        """
        self.level = random.choice(["top", "middle", "bottom"])
        return self.level

    def _create_article(self, keyword):
        """
        Generate the full article content with specific instructions.

        Args:
            keyword (str): The primary keyword for the article.

        Returns:
            str: The generated full article content.
        """

        instructions = f"""
        Rewrite this title. Write at least 1000 words article readable for people in 6th grade. Use the headings and subheadings but use different words. \
        Do not use the brands from the outline, use my brands from the XML <internal links> only. \
        Once you've used an internal link, do not use that internal link again.\
        Take the <avatar> and write an article specifically for that person. Your tone should match the needs of the <avatar>. Do not mention the <avatar>. \
        Do not mention other companies or brands, but focus more on educational or informative content. \
        Write with a huge degree of creativity and informative burstiness. Try to include <keywords> as much as possible. \
        Naturally add the primary keywords and other keywords into articles.  Explain nouns or ideas with examples and detailed explanations. \
        
        The article should be written in a manner that is easily understandable by individuals at a 6th-grade reading level. This involves using simple language, short sentences, and clear explanations of any complex terms or concepts.\
            
        Each heading (formatted as '##' for H2 and '###' for H3) must be followed by at least eight sentences of relevant content. Additionally, for every ordered or unordered list in the article, there must be accompanying explanations and examples followed by at least five sentences for each list item, formatted in Markdown. The article must include at least one ordered (numbered) or unordered (bulleted) list. These lists should be formatted in Markdown (e.g., '* Item' for unordered lists, '1. Item' for ordered lists) and must appear under a heading formatted as either '##' (H2) or '###' (H3). \
             
        Do not  mention any brand, services, or products. It is informative content. Create pictures to explain the ideas. \
        Include all of the following markdown formatting at least once:

        <sample markdown>

        This is some basic, sample markdown.
            # H1 for title
            ## H2. for main section
            ### H3 for subsection within main section. The smallest level of heading
            
            * Unordered lists or Ordered list within the main sections or subsection:
            1. One
            2. Two
            3. Three
            * More

            And **bold**, *italics*, and even *italics and later **bold***. [A link](https://markdowntohtml.com) to somewhere.

        </sample markdown>

        Use all parts of <sample markdown>. Use the <outline> with the Focus keyword . Articles should include the h1, h2, h3 font size. where H1 is used for main title of the article and include the Focus keyword in <outline>. H2 are headings that break up the main sections of your content, add most keywords here, plan on around 3-5 of these H2s. H3 are break up and list individual points in the main sections, in the form of numbered lists or clarifying sections to an H2 heading, for <keywords>

        Firstly, write an introduction, with one paragraph, and an unordered list summarizing the entire article

        Secondly, write the first half of the main part of the content, write at least 5 paragraphs.

        Thirdly, write the second half of the main part of the content, write at least 3 paragraphs

        Finally, write the conclusion, and include some links to other similar blogs at the bottom, write one paragraph.


        <outline>

        Focus keyword: ```{keyword}```

        title and outline: ```{self.new_outline}```

        </outline>

        <avatar>

        funnel: ```{self.selected_funnel}```

        </avatar>

        <keywords>

        ```{self.other_keywords}```

        </keywords>

        <internal links>

        http://help.abconvert.io/en/
        https://abconvert.io/
        https://help.abconvert.io/
        https://help.abconvert.io/cdn-cgi/l/email-protection
        https://help.abconvert.io/en/
        https://help.abconvert.io/en/articles/7991764-how-does-abconvert-work
        https://help.abconvert.io/en/articles/7992482-how-to-run-price-test-only-on-new-customer
        https://help.abconvert.io/en/articles/7994393-how-abconvert-analytics-works
        https://help.abconvert.io/en/articles/8517478-how-to-start-a-url-redirect-test
        https://help.abconvert.io/en/articles/8522853-how-to-test-product-price-shipping-at-the-same-time
        https://help.abconvert.io/en/articles/8540376-how-to-find-product-using-advanced-search
        https://help.abconvert.io/en/articles/8663230-how-to-set-up-utm-filter-for-price-test
        https://help.abconvert.io/en/articles/8663287-how-to-end-test-safely-on-recharge-subscription-products
        https://help.abconvert.io/en/articles/8676035-how-to-start-a-price-test
        https://help.abconvert.io/en/articles/8726911-how-to-manage-duplicate-product
        https://help.abconvert.io/en/articles/8730805-how-to-run-a-price-test-only-in-the-selected-countries
        https://help.abconvert.io/en/articles/8735286-how-to-sync-inventory-for-your-test-products
        https://help.abconvert.io/en/collections/3907966-shipping-rate-test
        https://help.abconvert.io/en/collections/4080621-onboarding
        https://help.abconvert.io/en/collections/4080626-advanced-topic
        https://www.abconvert.io/
        https://www.abconvert.io/abconvert-vs-intelligems
        https://www.abconvert.io/blog
        https://www.abconvert.io/blog/beginners-guide-to-a-b-testing
        https://www.abconvert.io/blog/enhancing-e-commerce-success-a-comprehensive-guide-to-a-b-testing-for-conversion-rate-optimization
        https://www.abconvert.io/blog/glossary-a-b-testing-essentials-for-e-commerce
        https://www.abconvert.io/blog/mastering-price-testing-in-e-commerce-with-the-ice-framework
        https://www.abconvert.io/blog/price-test-basics-how-to-optimize-your-e-commerce-store
        https://www.abconvert.io/blog/the-art-of-price-testing-key-to-maximizing-store-profits
        https://www.abconvert.io/blog/the-psychology-of-online-shopping-understanding-consumer-behavior
        https://www.abconvert.io/blog/the-ultimate-guide-to-optimizing-your-shopify-store-with-abconvert
        https://www.abconvert.io/blog/understanding-split-testing-a-comparative-look-with-a-b-testing
        https://www.abconvert.io/blog/why-black-friday-is-the-best-day-for-price-testing
        https://www.abconvert.io/contact-us
        https://www.abconvert.io/features
        https://www.abconvert.io/pricing
        https://www.abconvert.io/privacy-policy
        https://www.abconvert.io/why-a-b-test
        instructions
        </internal links>
    
        """
        prompt = f"""
        create the whole article followed by instructions in the markdown format.
        ```{instructions}```
        """
        self.full_article = self._get_completion(prompt)
        return self.full_article

    def _get_abstract(self):
        """
        Generate a short abstract of the article within 500 characters.

        Args:
            final_article (str): The generated full article content.

        Returns:
            str: A short abstract of the article.
        """
        prompt = f"""
        do the overview of the article within 500 characters.

        article: ```{self.full_article}```
        """

        self.abstract = self._get_completion(prompt)
        return self.abstract
    
    def _create_blog_picture(self):
        """
        Generate a blog picture based on the provided abstract.

        Args:
            abstract (str): A short abstract of the article.

        Returns:
            str: The link to the generated blog picture.
        """
        prompt = f"Create a blog picture in English based on the following blog content: '{self.abstract}'."

        # Specify other parameters
        n = 1  # Number of images to generate
        size = "1792x1024"  # Max image size
        quality = "standard"  # set image quality

        # Generate image using OpenAI API
        response = self.client.images.generate(
            model="dall-e-3",  # Check for the latest model name
            prompt=prompt,
            n=n,
            size=size,
            quality=quality
        )
        # Extract the generated image URL
        self.image_link = response.data[0].url

        return self.image_link
    
    def _get_duration(self):
        """
        Calculate the duration of the content generation process.

        Returns:
            float: The duration in minutes.
        """
        total_finish_time = time.time()
        self.duration = round((total_finish_time - self.total_start_time) / 60, 2)
        return self.duration

    def _create_metadata(self, keyword, input_link):
        """
        Create metadata in JSON format containing information about the generated content.

        Args:
            keyword (str): The primary keyword for the article.
            input_link (str): The link to the source content.

        Returns:
            str: JSON data structure containing metadata.
        """
        prompt = f"""
        Create a JSON data structure designed to collect information on titles, keywords, and funnels. \
        The structure should include keys named 'title', 'blog picture link', 'primary keyword', 'other_keywords', 'funnel', 'minutes' ,'date',and 'reference'. \
        Each 'title' should be a string representing the title in the outline, \
            'primary keyword' should be the keyword, \
            'blog picture link' should be the blog picture link, \
            'other keyword' should be the other keyword, \
            'funnel' should be one of the level in the funnel (top, middle,or bottom), \
            'minutes' should be the duration of the program, \
            'date' is today's date in the format of MM-DD-YYYY, \
            and 'reference' should be the website link. \

        outline: ```{self.new_outline}```
        blog picture link: ```{self.image_link}```
        primary keyword: ```{keyword}```
        other keyword: ```{self.other_keywords}```
        funnel: ```{self.level}```
        minutes = ```{self.duration}```
        date ```{self.today_date}```
        reference: ```{input_link}```
        """

        self.metadata = self._get_completion(prompt)
        return self.metadata

    def _generate_article(self, input_link, keyword):
        """
        Generate an article, abstract, and image based on the provided input link and keyword.

        Args:
            input_link (str): The link to the source content.
            keyword (str): The primary keyword for the article.
        """
        self._reset()
        self.total_start_time = time.time()
        self.today_date = datetime.date.today()
        self.outline = self._get_outline(input_link)
        self.new_outline = self._generate_new_outline(keyword)
        self.other_keywords = self._generate_keyword(keyword)
        self.level = self._get_funel_level()
        self.selected_funnel = self._get_funel()
        self.full_article = self._create_article(keyword)

    def _generate_picture(self):
        """
        Generate a blog picture based on the article's abstract.
        """
        self.abstract = self._get_abstract()
        self.image_link = self._create_blog_picture()

    def run(self, input_link, keyword):
        """
        Run the entire content generation process including article, abstract, and image generation.

        Args:
            input_link (str): The link to the source content.
            keyword (str): The primary keyword for the article.
        """
        self._generate_article(input_link, keyword)
        self._generate_picture()
        self._get_duration()
        self.metadata = self._create_metadata(keyword, input_link)

    def get_all_results(self):
        """
        Print the generated article, image link, and metadata.
        """
        print("Article: ")
        print(self.full_article)
        print()
        print("Picture link: ")
        print(self.image_link)
        print()
        print("Meta data: ")
        print(self.metadata)