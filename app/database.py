from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Config

# 创建 SQLAlchemy 引擎
engine = create_engine(Config.DATABASE_URI, echo=True)

# 创建会话
Session = sessionmaker(bind=engine)

# 创建基本模型
Base = declarative_base()

def get_session():
    """返回一个新的 session 实例"""
    return Session()

def init_db():
    """初始化数据库，包括创建表"""
    Base.metadata.create_all(bind=engine)
