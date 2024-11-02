from sqlalchemy import UUID, Column, Integer, String, Text, \
    ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from rag.sql.engine import engine

Base = declarative_base()


class Webpage(Base):
    __tablename__ = 'webpages'
    id = Column(Text, primary_key=True)
    # Non-null text content
    text = Column(Text, nullable=False)
    # Non-null domain
    domain = Column(Text, nullable=False)
    # Nullable title
    title = Column(Text)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to the WebpageLinks class
    links_relation = relationship(
        "WebpageLink",
        back_populates="webpage"
    )


# Webpages Links Table
class WebpageLink(Base):
    __tablename__ = 'webpages_links'
    id = Column(Integer, primary_key=True)
    # Non-null link (URL)
    link = Column(Text, nullable=False)
    # Foreign key to the Webpage table
    webpage_id = Column(
        Text,
        ForeignKey('webpages.id', ondelete='CASCADE'),
        nullable=False
    )
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to the Webpage class
    webpage = relationship(
        "Webpage",
        back_populates="links_relation"
    )


# Books Table
class Book(Base):
    __tablename__ = 'books'
    id = Column(Text, primary_key=True)
    # Nullable book title
    title = Column(Text, index=True)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to books cites and books documents
    cites_relation = relationship(
        "BookCite",
        foreign_keys='[BookCite.book_id]',
        back_populates="book"
    )
    cited_by_relation = relationship(
        "BookCite",
        foreign_keys='[BookCite.cited_book_id]',
        back_populates="cited_book"
    )
    documents_relation = relationship(
        "BookDocument",
        back_populates="book"
    )
    # TODO title, author, published similarities to identify books


# Books Cites Table
class BookCite(Base):
    __tablename__ = 'books_cites'
    # Composite primary key
    # Foreign key to citing book
    book_id = Column(
        Text,
        ForeignKey('books.id', ondelete='CASCADE'),
        nullable=False,
        primary_key=True
    )
    # Composite primary key
    # Foreign key to cited book
    cited_book_id = Column(
        Text,
        ForeignKey('books.id', ondelete='CASCADE'),
        nullable=False,
        primary_key=True
    )
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to the Book class (self-referencing)
    book = relationship(
        "Book",
        foreign_keys=[book_id],
        back_populates="cites_relation"
    )
    cited_book = relationship(
        "Book",
        foreign_keys=[cited_book_id],
        back_populates="cited_by_relation"
    )


# Books Documents Table
class BookDocument(Base):
    __tablename__ = 'books_documents'

    id = Column(Text, primary_key=True)
    # Non-null document text
    text = Column(Text, nullable=False)
    # Foreign key to the Book table
    book_id = Column(
        Text,
        ForeignKey('books.id', ondelete='CASCADE'),
        nullable=False
    )
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to the Book class
    book = relationship(
        "Book",
        back_populates="documents_relation"
    )


Base.metadata.create_all(engine)
