from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    __table_args__ = {'schema': 'news'}
    url_hash = Column(String(64), primary_key=True, unique=True)
    source_id = Column(String(255), ForeignKey('news.sources.id'))
    author = Column(String(255))
    title = Column(Text)
    description = Column(Text)
    url = Column(Text)
    url_to_image = Column(Text)
    published_at = Column(TIMESTAMP)
    content = Column(Text)
    
class Source(Base):
    __tablename__ = 'sources'
    __table_args__ = {'schema': 'news'}
    id = Column(String(255), primary_key=True, unique=True)
    name = Column(String(255))
    description = Column(Text)
    url = Column(Text)
    category = Column(String(255))
    language = Column(String(255))
    country = Column(String(255))