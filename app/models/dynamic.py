# app/models/dynamic.py
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from app.database import Base


class Dynamic(Base):
    __tablename__ = "dynamic"

    dynamic_id = Column(String(255), primary_key=True, comment="动态的唯一 ID")
    comment_id = Column(String(255), nullable=False, comment="动态的评论 ID")
    dynamic_type = Column(String(50), nullable=False, comment="动态的类型")
    jump_url = Column(String(255), nullable=False, comment="跳转 URL")
    author_name = Column(String(255), nullable=False, comment="作者姓名")
    author_mid = Column(Integer, nullable=False, comment="作者 MID")
    author_face = Column(String(255), nullable=False, comment="作者头像 URL")
    dynamic_desc = Column(Text, nullable=False, comment="动态描述")
    like_count = Column(Integer, default=0, comment="点赞数")
    forward_count = Column(Integer, default=0, comment="转发数")
    comment_count = Column(Integer, default=0, comment="评论数")
    media_urls = Column(Text, nullable=False, comment="多媒体链接")
    is_only_fans = Column(Boolean, default=False, comment="是否仅限粉丝查看")
    pub_time = Column(DateTime, nullable=False, comment="发布时间")
    forward_title = Column(Text, nullable=False, comment="转发动态标题")
    forward_author_name = Column(String(255), nullable=False, comment="转发作者姓名")
    forward_url = Column(String(255), nullable=False, comment="转发跳转 URL")
    forward_dynamic_data = Column(JSON, nullable=True, comment="转发动态数据")
