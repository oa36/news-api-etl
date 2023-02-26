import requests
import os
from sqlalchemy.exc import IntegrityError
import hashlib

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

def fetch_data(endpoint, params={}):
    """
    Fetches data from the News API using the specified endpoint and query parameters.

    Args:
        endpoint (str): The endpoint of the News API to call (e.g., "everything").
        params (dict): The query parameters to include in the API request.

    Returns:
        A JSON object representing the API response.
    """    
    url = BASE_URL + endpoint
    params['apiKey'] = API_KEY
    response = requests.get(url, params=params)
    response_json = response.json()
    return response_json

def clean_articles(data):
    """
    Remove articles with NULL source ID from data and compute url_hash to each article.

    Args:
        - data (dict): A dictionary containing news data retrieved from the NewsAPI
          using the fetch_data function. The dictionary should have the following keys:
        - status (str): A string indicating the status of the API request.
        - totalResults (int): The total number of articles that match the query.
        - articles (list): A list of dictionaries, where each dictionary represents
          an article containing information such as source, author, title, and content.

    Returns:
    - A list of article data dictionaries.
    """
    # filter out articles with null source ids and add url_hash
    articles_clean = []
    for article in data["articles"]:
        if article["source"]["id"] is not None:
            url_hash = hashlib.sha256(article['url'].encode('utf-8')).hexdigest()
            article_clean = {
                "url_hash": url_hash,
                "source_id": article["source"]["id"],
                "author": article.get("author", None),
                "title": article.get("title", None),
                "description": article.get("description", None),
                "url": article.get("url", None),
                "url_to_image": article.get("urlToImage", None),
                "published_at": article.get("publishedAt", None),
                "content": article.get("content", None),
            }            
            articles_clean.append(article_clean)
            
    len_total_articles = data["totalResults"]
    len_cleaned_articles = len(articles_clean)

    # create a new dictionary with the same structure as the input data
    data_clean = {
        "status": data["status"],
        "totalResults": len_cleaned_articles,
        "articles": articles_clean
    }
    
    print(f"Total number of articles returned by the API: {data['totalResults']}")
    print(f"Total number of articles deleted: {len_total_articles - len_cleaned_articles}")

    return data_clean

def insert_data(table, data, session):
    """
    Insert data into the specified table using SQLAlchemy ORM.
    
    Parameters:
        table (Base): A SQLAlchemy declarative base class representing the table to insert into.
        data (list[dict]): A list of dictionaries containing the data to insert.
        session (SQLAlchemy Session): A session object representing the current database session.
    
    Returns:
        int: The number of rows successfully inserted into the table.
    """
    # insert data into database using SQLAlchemy ORM
    insert_counter = 0
    for item in data:
        new_record = table(**item)
        session.add(new_record)
        try:
            session.flush()
            insert_counter += 1
        except IntegrityError as e:
            session.rollback()
            if "violates unique constraint" in str(e) or "duplicate key value violates unique constraint" in str(e):
                continue
            else:
                raise e

    session.commit()
    print(f"{insert_counter} records inserted to the {table.__tablename__} table.")
    return insert_counter
