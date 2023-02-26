# News API ETL

This project is an ETL (Extract, Transform, Load) pipeline for the News API: https://newsapi.org/. It extracts news articles and sources from the News API, transforms it, and loads it into a PostgreSQL database.

## Prerequisties
- Docker

## Getting started
1. Clone the repository

    ```bash
    git clone https://github.com/oa36/news-api-etl.git
    ```
2. Create a `.env` file based on the provided `env.example` file.  
   -  You need to update your `API_KEY` in `.env`, the reset of required variables are already defined in `env.example`.
   -  `DOCKER_DEFAULT_PLATFORM=linux/amd64` is needed if you have M1-Based mac: [check here](https://stackoverflow.com/questions/62807717/how-can-i-solve-postgresql-scram-authentication-problem)  

    ```bash
    cp env.example .env
    ```   
3. Run the following command to start the application:
   
    ```bash
    docker-compose up --build
    ```
4. The PostgreSQL database will be initialized with the schema and tables defined in `db/init.sql`. Connect to the database using database client tool (e.g. TablePlus) using the credentials specified in `.env`.  

## Project structure  
- Dockerfile: Dockerfile for the ETL pipeline service.
- Pipfile: Pipfile for the ETL pipeline service.
- Pipfile.lock: Pipfile lock file for the ETL pipeline service.
- README.md: This file.
- config: Directory containing configuration files for the ETL pipeline
  - db_config.py: Configuration file for the database connection.
- db: Directory containing the database initialization SQL file.
  - init.sql: SQL file for initializing the PostgreSQL database.
- docker-compose.yml: Docker Compose file for running the ETL pipeline and database service.
- env.example: Example environment file containing required environment variables for the ETL pipeline service.
- src: Directory containing source code for the ETL pipeline service.
  - data_models.py: Contains data model definitions for SQLAlchemy.
  - news_etl.py: Contains the ETL pipeline code.
  - utils.py: Contains utility functions used by the ETL pipeline.