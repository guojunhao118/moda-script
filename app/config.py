import os

class Config:
    DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+mysqlconnector://root:8819667wc@localhost:3306/moda')  # 默认端口3306
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
