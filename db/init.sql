-- Create schema for news data
CREATE SCHEMA IF NOT EXISTS news;
CREATE SCHEMA IF NOT EXISTS ANALYTICS;

-- Create table for sources
CREATE TABLE news.sources (
  id VARCHAR(255) NOT NULL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  url TEXT,
  category VARCHAR(255),
  language VARCHAR(255),
  country VARCHAR(255)
);

-- Create table for news articles
CREATE TABLE IF NOT EXISTS news.articles (
  id SERIAL,
  url_hash VARCHAR(64) NOT NULL PRIMARY KEY,
  source_id VARCHAR(255) NOT NULL REFERENCES news.sources(id),
  author VARCHAR(255),
  title TEXT,
  description TEXT,
  url TEXT,
  url_to_image TEXT,
  published_at TIMESTAMP,
  content TEXT
);

-- Create table for news articles
CREATE VIEW analytics.articles_with_sources AS
SELECT 
  a.id,
  a.published_at,
  a.title as article_title,
  a.description as article_description,
  a.content as article_content,
  s.name as source_name,
  s.description as source_description,
  s.category as source_category,
  s.language as source_language,
  s.country as source_country
FROM news.articles a
INNER JOIN news.sources s
ON a.source_id = s.id;