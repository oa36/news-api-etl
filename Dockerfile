#python image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DATABASE_URL postgresql://user:password@db:5432/news

#working directory
WORKDIR /app

#pipenv files are required to install the needed packages and dependencies
COPY Pipfile Pipfile.lock /app/

#install dependencies
RUN pip install pipenv && \
  apt-get update && \
  apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
  pipenv install --deploy --system && \
  apt-get remove -y gcc python3-dev libssl-dev && \
  apt-get autoremove -y && \
  pip uninstall pipenv -y

# Copy the code
COPY . /app/

ENV PYTHONPATH /app

# run etl pipeline
CMD ["python", "src/news_etl.py"]