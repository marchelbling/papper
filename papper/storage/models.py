from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship


Base = declarative_base()

class PapperBase(Base):
    id = Column(Integer, primary_key=True)

article_author = Table('article_author',
                       Base.metadata,
                       Column('article_id', Integer, ForeignKey('article.id')),
                       Column('author_id', Integer, ForeignKey('author.id')))


article_category = Table('article_category',
                         Base.metadata,
                         Column('article_id', Integer, ForeignKey('article.id')),
                         Column('category_id', Integer, ForeignKey('category.id')))


class Article(PapperBase):
    __tablename__ = 'ppr_articles'

    source = Column(String(32), nullable=False)
    url = Column(String(128), nullable=True)
    date = Column(Date, nullable=True)
    title = Column(String, nullable=False)
    abstract = Column(Text, nullable=True)

    authors = relationship('Author', secondary=article_author,
                           backref='articles')
    categories = relationship('Category', secondary=article_category,
                              backref='articles')

    license_id = Column(Integer, ForeignKey('license.id'))
    license = relationship('License', uselist=False, backref='articles')


class Author(PapperBase):
    __tablename__ = 'ppr_authors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(32))
    middle_name = Column(String(2))
    last_name = Column(String(32))


class License(PapperBase):
    __tablename__ = 'ppr_licenses'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    url = Column(String(128))


class Category(PapperBase):
    __tablename__ = 'ppr_categories'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer)
    abbreviation = Column(String(16))
    name = Column(String(32))
