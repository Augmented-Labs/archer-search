import json
import os
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import requests
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI
os.environ["OPENAI_API_KEY"] = "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"
'''
This sample makes a call to the Bing Web Search API with a query and returns relevant web search.
Documentation: https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
'''

os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY'] = '51e3cda4698846cf83a9a76b5a498c2b'
os.environ['BING_SEARCH_V7_ENDPOINT'] = 'https://api.bing.microsoft.com'
# Add your Bing Search V7 subscription key and endpoint to your environment variables.
subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/bing/v7.0/search"

# Query term(s) to search for.
# query = '''site:linkedin.com inurl:posts "Jordan Crawford" "I Scale Founder-Led Sales (Outbound by Pain, not Persona)"'''
query = 'https://www.linkedin.com/in/roybahat/'


def bing_search(query):
    # Construct a request
    mkt = 'en-US'
    params = {'q': query, 'mkt': mkt}
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    # Call the API
    try:
        response = requests.get(
            'https://api.bing.microsoft.com/v7.0/search', headers=headers, params=params)
        response.raise_for_status()
        results = response.json()['webPages']
        return results
    except Exception as ex:
        raise ex


# converting "https://www.linkedin.com/in/aaronmmichel" to aaronmmichel
def get_username(url):
    parts = url.split('/')
    # Remove trailing slash if present
    if parts[-1] == '':
        parts.pop()
    username = parts[-1]
    return username


def get_post_link(profile):
    query = f'site:linkedin.com/posts {profile}'
    results = bing_search(query)
    page_results_list = results['value']
    # print(page_results_list)
    # iterate through page results to find a linkedin post for the profile input
    found_url = None
    username = get_username(profile)
    for result in page_results_list:
        current_result_url = result['url']
        if (username+'_' in current_result_url):
            found_url = current_result_url
            break
    if found_url == None:
        raise Exception("No URL found")
    return found_url


def get_posts(profile):
    post_link = get_post_link(profile)
    response = requests.get(post_link)
    if response.status_code == 200:
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div element with the specific class, for example 'my-class'
        div_element = soup.find(
            'div', class_='core-section-container__content break-words')
        articles = div_element.find_all('article') if div_element else []
        posts_dict_list = []
        for article in articles:
            url = article.find_previous_sibling().attrs.get('href')
            time = ''.join(article.find('time').get_text(
            ).strip().split()).replace('Edited', '')
            text = ''
            if article.find(attrs={'data-test-id': 'main-feed-activity-card__commentary'}) or article.find(attrs={'data-test-id': 'main-feed-card'}):
                text = article.find(
                    attrs={'data-test-id': 'main-feed-activity-card__commentary'}).get_text()
                if not text:
                    text = article.find(
                        attrs={'data-test-id': 'main-feed-card'}).get_text()
                posts_dict_list.append(
                    {'time': time, 'text': text, 'url': url})
        return posts_dict_list
    else:
        print(f"Error: {response.status_code}")


def get_relevancy(post, query):
    template = "You are a helpful assistant that answers yes or no."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = '''Given the following text and query, tell me whether the text is relevant to the query. Let's think step by step.
Text:
{text}
Query:
{query}

Relevant (Answer Yes or No):
'''
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt, HumanMessage(content="Answer only Yes or No with no punctuation")])
    # get a chat completion from the formatted messages
    chat = ChatOpenAI(temperature=0)
    output = chat(chat_prompt.format_prompt(
        text=post, query=query).to_messages())

    return output.content


def get_relevancy_score(posts, problem):
    score_count = 0
    relevant_posts = []
    for post in posts:
        is_relevant = get_relevancy(post['text'], problem)

        if (is_relevant == 'Yes'):
            score_count += 1
            relevant_posts.append(post)
        else:
            pass

    return {"score": score_count, "relevant_posts": relevant_posts}


def calculate_linkedin_relevancy(url, query, searchType):
    posts = get_posts(url)
    relevancy_dict = get_relevancy_score(
        posts, query)
    relevancy_dict['all_posts'] = posts
    relevancy_dict['linkedin_profile_url'] = url
    relevancy_dict['searchType'] = searchType
    return relevancy_dict


# calculate_linkedin_relevancy(
#     '"https://www.linkedin.com/in/aaronmmichel/', "We help startups book meetings")
# , data_dict['searchType']
URL = "https://api.apollo.io/v1/mixed_people/search"


def get_people_from_apollo_page(organization_domain, page, person_titles=[]):
    data = {
        "api_key": "mHMEY6VFo4-HDes_4gfHpw",
        "q_organization_domains": organization_domain,
        "person_titles": person_titles,
        "page": page,
        "per_page": 200,
    }
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", URL, headers=headers, json=data)
    if (response.headers['x-minute-requests-left'] == '0'):
        time.sleep(60)
    response_obj = response.json()
    return response_obj


def get_people_from_apollo(organization_domain, segment_roles):
    res = []
    response_obj = get_people_from_apollo_page(
        organization_domain, 1, segment_roles)
    num_pages = response_obj['pagination']['total_pages']
    print(response_obj['pagination'])

    if (response_obj['pagination']['total_entries'] > 10000):
        response_obj = get_people_from_apollo_page(
            organization_domain, 1, segment_roles)
        num_pages = response_obj['pagination']['total_pages']

    res = res + response_obj['people']
    for i in range(2, num_pages + 1):
        response_array = get_people_from_apollo_page(
            organization_domain, i)['people']
        result_obj = list(map(lambda x: {'name': x['name'], 'title': x['title'],
                                         'linkedin_url': x['linkedin_url']}, response_array))

        res = res + result_obj

    return res


def get_posts_company(url, query):
    people_array = get_people_from_apollo(
        url, ['CISO', 'CEO', 'Security Engineer', 'CTO', 'Founder'])
    final_people_array = []
    for person in people_array:
        try:
            result = calculate_linkedin_relevancy(
                person['linkedin_url'], query, "Company Search")
            result['name'] = person['name']
            result['title'] = person['title']
            final_people_array.append(result)
        except Exception as e:
            pass
    return final_people_array
