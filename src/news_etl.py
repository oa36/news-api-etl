from src.utils import *
from data_models import *
from config.db_config import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

EVERYTHING_ENDPOINT = os.getenv("EVERYTHING_ENDPOINT")
SOURCES_ENDPOINT = os.getenv("SOURCES_ENDPOINT")

def sources_etl():
    print(f"extracting all sources from news API..")
    sources_raw_data = fetch_data(SOURCES_ENDPOINT)
    insert_data(Source ,sources_raw_data["sources"], session=session)

def articles_etl():
    params = {
        "q": "Commerzbank",
    }
    print(f"extracting {params['q']} articles from news API..")
    everything_raw_data = fetch_data(EVERYTHING_ENDPOINT, params=params)
    print("Deleting empty articles..")
    everything_data_cleaned = clean_articles(everything_raw_data)
    insert_data(Article ,everything_data_cleaned["articles"], session=session)

if __name__ == '__main__':
    #docker will have access to the db image and not localhost
    db_config["host"] = "db"
    engine = create_engine(URL.create(**db_config))
    Session = sessionmaker(bind=engine)
    session = Session()
    sources_etl()
    articles_etl()
    session.close()