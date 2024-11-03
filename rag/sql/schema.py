from sqlalchemy import UUID, Column, Integer, String, Text, \
    ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from rag.sql.engine import engine

Base = declarative_base()


class Webpage(Base):
    __tablename__ = 'webpages'
    id = Column(Text, primary_key=True)
    # # Non-null text content
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
    # Relationship to the WebpageDocuments class
    documents_relation = relationship(
        "WebpageDocument",
        back_populates="webpage"
    )


# Webpages Links Table
class WebpageLink(Base):
    __tablename__ = 'webpages_links'
    id = Column(UUID, primary_key=True)
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


# WebPages Documents Table
class WebpageDocument(Base):
    __tablename__ = 'webpages_documents'

    id = Column(UUID, primary_key=True)
    # Non-null document text
    text = Column(Text, nullable=False)
    # Foreign key to the Book table
    webpage_id = Column(
        Text,
        ForeignKey('webpages.id', ondelete='CASCADE'),
        nullable=False
    )
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to the WebpageRaft class
    raft = relationship(
        "WebpageRaft",
        back_populates="webpage_document_relation"
    )

    # Relationship to the Webpage class
    webpage = relationship(
        "Webpage",
        back_populates="documents_relation"
    )


# Webpages Rafts Table
class WebpageRaft(Base):
    __tablename__ = 'webpages_rafts'
    id = Column(UUID, primary_key=True)
    input = Column(Text, nullable=False)
    output = Column(Text, nullable=False)
    webpage_document_id = Column(
        UUID,
        ForeignKey('webpages_documents.id', ondelete='CASCADE'),
        nullable=False
    )
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to the Webpage class
    webpage_document_relation = relationship(
        "WebpageDocument",
        back_populates="raft"
    )


# Books Table
class Book(Base):
    __tablename__ = 'books'
    id = Column(Text, primary_key=True)
    authors = Column(Text)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to the BookCite class
    cites_relation = relationship(
        "BookCite",
        back_populates="book"
    )

    documents_relation = relationship(
        "BookDocument",
        back_populates="book"
    )


# Books Cites Table
class BookCite(Base):
    __tablename__ = 'books_cites'
    # primary key
    id = Column(UUID, primary_key=True)
    cited_book_title = Column(Text, nullable=False)
    cited_book_authors = Column(Text)
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
        back_populates="cites_relation"
    )


# Books Documents Table
class BookDocument(Base):
    __tablename__ = 'books_documents'

    id = Column(UUID, primary_key=True)
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

    # Relationship to the BookRaft class
    raft = relationship(
        "BookRaft",
        back_populates="book_document_relation"
    )

    # Relationship to the Book class
    book = relationship(
        "Book",
        back_populates="documents_relation"
    )


# Books Rafts Table
class BookRaft(Base):
    __tablename__ = 'books_rafts'
    id = Column(UUID, primary_key=True)
    input = Column(Text, nullable=False)
    output = Column(Text, nullable=False)
    book_document_id = Column(
        UUID,
        ForeignKey('books_documents.id', ondelete='CASCADE'),
        nullable=False
    )
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger)
    deleted_at = Column(BigInteger)

    # Relationship to the Webpage class
    book_document_relation = relationship(
        "BookDocument",
        back_populates="raft"
    )


Base.metadata.create_all(engine)
