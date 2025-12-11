# db_handler.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# ---------------------------
# Database init (SQLite)
# ---------------------------
DATABASE_URL = "sqlite:///crawler.db"

Base = declarative_base()
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)
SessionLocal = sessionmaker(bind=engine)


# ---------------------------
# Table Model
# ---------------------------
class CrawlerPost(Base):
    __tablename__ = "crawler_posts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String(400), nullable=False)
    link = Column(String(1000), nullable=False, unique=True)
    author = Column(String(255), nullable=True)
    time = Column(DateTime, nullable=True)
    content = Column(Text, nullable=True)
    source = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


# ---------------------------
# Create table if not exist
# ---------------------------
def init_database():
    Base.metadata.create_all(bind=engine)


# ---------------------------
# Save post function
# ---------------------------
def save_post(data: dict):
    """
    data example:
    {
        "title": "...",
        "link": "...",
        "author": "...",
        "time": "2025-01-12T15:28:00",
        "content": "...",
        "source": "leakbase.la"
    }
    """
    session = SessionLocal()

    # Convert time
    try:
        parsed_time = datetime.fromisoformat(data["time"])
    except:
        parsed_time = None

    post = CrawlerPost(
        title=data["title"],
        link=data["link"],
        author=data.get("author"),
        time=parsed_time,
        content=data.get("content"),
        source=data.get("source", "unknown"),
    )

    try:
        session.add(post)
        session.commit()
        print(f"[DB] Saved: {post.title}")
    except IntegrityError:
        session.rollback()
        print(f"[DB] Duplicate skipped: {data['link']}")
    except Exception as e:
        session.rollback()
        print("[DB] Error:", e)
    finally:
        session.close()
