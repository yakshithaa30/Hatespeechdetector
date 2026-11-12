'''import logging
logging.getLogger("passlib").setLevel(logging.ERROR)
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# 1. Tells Python to create a local database file named 'moderation.db'
DATABASE_URL = "sqlite:///./moderation.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Tool to securely encrypt (hash) passwords so they aren't stored in plain text
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 3. Create the 'Users' table layout
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user") # Can be 'user' or 'admin'

# 4. Create the 'Scan History' table layout
class ScanHistory(Base):
    __tablename__ = "scan_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    input_text = Column(Text, nullable=False)
    prediction_label = Column(String, nullable=False) # 'hate' or 'normal'
    raw_analysis = Column(Text, nullable=False)       # Detailed reason breakdown

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# 5. This initializes the database and creates a ready-to-use Admin account automatically
def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    admin_exists = db.query(User).filter(User.email == "admin@moderator.com").first()
    if not admin_exists:
        admin_user = User(
            username="admin",
            email="admin@moderator.com",
            hashed_password=hash_password("admin123"),
            role="admin"
        )
        db.add(admin_user)
        db.commit()
    db.close()'''
import hashlib
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./hate_speech.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DATABASE TABLES
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user") # 'admin' or 'user'

'''class ScanLog(Base):
    __tablename__ = "scan_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    text_content = Column(Text)
    prediction_label = Column(String) # 'hate' or 'normal'
    raw_analysis = Column(Text)       # Detailed factors breakdown explanation'''
class ScanHistory(Base):
    __tablename__ = "scan_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    input_text = Column(Text)          # Changed from text_content to match main.py
    prediction_label = Column(String)  # 'hate' or 'normal'
    raw_analysis = Column(Text)        # Detailed factors breakdown explanation

# CUSTOM PASSWORD SECURE HASHING (Bypasses passlib compatibility issues)
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

# SYSTEM DATABASE BOOTSTRAPPER
def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if default admin account exists, if not, establish it
    admin_user = db.query(User).filter(User.email == "admin@moderator.com").first()
    if not admin_user:
        new_admin = User(
            username="administrator",
            email="admin@moderator.com",
            hashed_password=hash_password("admin123"),
            role="admin"
        )
        db.add(new_admin)
        db.commit()
    db.close()