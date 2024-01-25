# %%
# !pip  install openai

# %%
# import packages and openai_key
import openai
import os
import time
import datetime
import random
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

os.environ['OPENAI_API_KEY'] = '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'

openai.api_key  = os.getenv('OPENAI_API_KEY')

# %%
# set up the function 
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

# normal prompt generation 
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


# %%
# set a time of the start time of generating a content
total_start_time = None
outline = None
new_outline = None
other_keywords = None
level = None
selected_funnel = None
abstract = None
full_article = None
image_link = None
today_date = None
metadata = None


# %%
#create avatar list in funnels
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

# %%
level = random.choice(["top","middle","bottom"])
selected_funnel = funnel_list.get(level)
## pick a ramdom funnel

# %%
def _reset():
    # define in case
    global total_start_time, full_article, today_date, outline, new_outline, other_keywords, level, \
        selected_funnel, abstract, full_article,image_link, metadata
    total_start_time = None
    outline = None
    new_outline = None
    other_keywords = None
    level = None
    selected_funnel = None
    abstract = None
    full_article = None
    image_link = None
    today_date = None
    metadata = None

def _get_outline(website_link):
    # read the outline from the website link
    # need to change website link

    prompt = f"""
    create an outline based on the article link
    ```{website_link}```
    """
    outline = get_completion(prompt)
    return outline

def _generate_new_outline(keyword, outline):
    # generate a clickable article title based on the provided outline and keyword.

    prompt = f"""
    Based on the outline, create a clickable article title that included the keyword and revise the outline to be used in my owm article based on revised title \
    It shouldn't include any other brand service or product. 
    keyword: ```{keyword}```
    outline: ```{outline}```
    """
    new_outline = get_completion(prompt)
    return new_outline

def _generate_keyword(keyword, new_outline):
    # list the 10 related keywords

    prompt = f"""
    Based on the new outline, list some keywords that related the content and title in total of 10. Do not include the primpary keyword.
    primary keyword: ```{keyword}```
    outline: ```{new_outline}```
    """
    other_keywords = get_completion(prompt)
    return other_keywords

def _get_funel(level):
    selected_funnel = funnel_list.get(level)
    return selected_funnel

def _get_funel_level():
    level = random.choice(["top","middle","bottom"])
    return level

def _create_article(keyword, new_outline, selected_funnel, other_keywords):
    # creating the article with instructions
    
    instructions = f"""
    Rewrite this title. Write the article readable for people in 6th grade. Use the headings and subheadings but use different words. \
    Do not use the brands from the outline, use my brands from the XML <internal links>. \
    Once you've used an internal link, do not use that internal link again. \
    Take the <avatar> and write an article specifically for that person. Your tone should match the needs of the <avatar>. Do not mention the <avatar>. \
    Do not mention other companies or brands, but focus more on educational or informative content. \
    Write with a huge degree of creativity and informative burstiness. Try to include <keywords> as much as possible. \
    Naturally add the primary keywords and other keywords into articles.  Explain nouns or ideas with examples and detailed explanations. \
    Do not  mention any brand, services, or products. It is informative content. Create pictures to explain the ideas. \
    Include all of the following HTML formatting at least once:

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

    Use all parts of <sample markdown>. Use the <outline> with the Focus keyword . Articles should include the h1, h2, h3 font size. where H1 is used for main title of the article and include the Focus keyword in <outline>. H2 are headings that break up the main sections of your content, add most keywords here, plan on around 3-5 of these H2s in 1000 words article. H3 are break up and list individual points in the main sections, in the form of numbered lists or clarifying sections to an H2 heading, for <keywords>

    Firstly, write an introduction, with one paragraph, and an unordered list summarizing the entire article

    Secondly, write the first half of the main part of the content, write at least 5 paragraphs.

    Thirdly, write the second half of the main part of the content, write at least 3 paragraphs

    Finally, write the conclusion, and include some links to other similar blogs at the bottom, write one paragraph.


    <outline>

    Focus keyword: ```{keyword}```

    title and outline: ```{new_outline}```

    </outline>

    <avatar>

    funnel: ```{selected_funnel}```

    </avatar>

    <keywords>

    ```{other_keywords}```

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
    article = get_completion(prompt)
    return article

def _get_abstract(final_article):
    # create a short abstract of article within 500 words due to the prompt limit in image generation

    prompt = f"""
    do the overview of the artciel within 500 characters.

    article: ```{final_article}```
    """

    abstract= get_completion(prompt)
    return abstract


def _create_blog_picture(abstract):
    # function to create blog picture
    # change testing_text to article
    # Define the prompt
    prompt = f"Create a blog picture in English based on the following blog content: '{abstract}'."

    # Specify other parameters
    n = 1  # Number of images to generate
    size = "1792x1024"  # Max image size
    quality = "standard" # set image quality

    # Generate image using OpenAI API
    response = client.images.generate(
        model="dall-e-3",  # Check for the latest model name
        prompt=prompt,
        n=n,
        size=size,
        quality= quality
    )

    # Extract the generated image URL
    image_url = response.data[0].url

    return image_url

def _get_duration(total_start_time):
    total_finish_time = time.time()
    duration = round((total_finish_time - total_start_time) / 60,2)
    return duration

def _create_metadata(new_outline, image_url, keyword, other_keywords, level, duration, today_date, website_link):
    # create meta data in JSON
    prompt = f"""
    Create a JSON data structure designed to collect information on titles, keywords, and funnels. \
    The structure should include keys named 'title', 'blog picture link', 'primary keyword', 'other_keywords', 'funnel', 'minutes' ,'date',and 'reference'. \
    Each 'title' should be a string representing the title in the outline, \
        'primary keyword' should be the primary keyword, \
        'blog picture link' should be the blog picture link, \
        'other keyword' should be the other keyword, \
        'funnel' should be one of the level in the funnel (top, middle,or bottom), \
        'minutes' should be the duration of the program, \
        'date' is the today's date in the format of MM-DD-YYYY, \
        and 'reference' should be the website link. \


    outline: ```{new_outline}```
    blog picture link: ```{image_url}```
    primary keyword: ```{keyword}```
    other keyword: ```{other_keywords}```
    funnel: ```{level}```
    minutes = ```{duration}```
    date ```{today_date}```
    reference: ```{website_link}```
    """

    artilce_meta= get_completion(prompt)
    return artilce_meta


# %%
# Generate article
def _generate_article(input_link, keyword):
    global total_start_time, today_date, outline, new_outline, other_keywords, level, full_article, \
        selected_funnel, full_article
    _reset()
    total_start_time = time.time()
    today_date = datetime.date.today()
    outline = _get_outline(input_link)
    new_outline = _generate_new_outline(keyword, outline)
    other_keywords = _generate_keyword(keyword, new_outline)
    level = _get_funel_level()
    selected_funnel = _get_funel(level)
    full_article = _create_article(keyword, new_outline, selected_funnel, other_keywords)
    return full_article
    
def _generate_picture(article):
    global abstract, image_link
    abstract = _get_abstract(article)
    image_link = _create_blog_picture(abstract)
    return image_link

# run full article, picture link, and meta data
def run(input_link, keyword):
    global total_start_time, today_date, full_article, level, image_link, other_keywords, new_outline, metadata
    _generate_article(input_link, keyword)
    _generate_picture(full_article)
    duration = _get_duration(total_start_time)
    metadata = _create_metadata(new_outline, image_link, keyword, other_keywords, level, duration, today_date, input_link)

def get_all_resutls():
    global full_article, image_link, metadata
    print("Article: ")
    print(full_article)
    print()
    print("Picture link: ")
    print(image_link)
    print()
    print("Meta data: ")
    print(metadata)

def get_article(): 
    return full_article

def get_metadata():
    return metadata

def get_picture_link():
    return image_link

# get to know each variable now
def get_outline():
    return outline

def get_new_outline():
    return new_outline

def get_other_keywords():
    return other_keywords

def get_level():
    return level

def get_selected_funnel():
    return selected_funnel

def get_abstract():
    return abstract






