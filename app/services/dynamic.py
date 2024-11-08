import json
from app.database import get_session
from app.models.dynamic import Dynamic


def get_dynamic_list_from_db(page=1, page_size=10):  # 改名为 get_dynamic_list_from_db
    """
    获取动态列表，按发布时间倒序排序，支持分页
    :param page: 当前页数，默认为1
    :param page_size: 每页的动态数量，默认为10
    :return: 返回动态列表
    """
    offset = (page - 1) * page_size

    print(f"接口====={offset}")

    # 获取 session 实例
    session = get_session()

    try:
        # 获取数据总数
        total = session.query(Dynamic).count()

        result = (
            session.query(Dynamic)
            .order_by(Dynamic.pub_time.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

        dynamic_list = []
        for row in result:
            dynamic = {
                "dynamic_id": row.dynamic_id,
                "comment_id": row.comment_id,
                "dynamic_type": row.dynamic_type,
                "jump_url": row.jump_url,
                "author_name": row.author_name,
                "author_mid": row.author_mid,
                "author_face": row.author_face,
                "dynamic_desc": row.dynamic_desc,
                "like_count": row.like_count,
                "forward_count": row.forward_count,
                "comment_count": row.comment_count,
                "media_urls": json.loads(row.media_urls) if row.media_urls else [],
                "is_only_fans": row.is_only_fans,
                "pub_time": row.pub_time,
                "forward_title": row.forward_title,
                "forward_author_name": row.forward_author_name,
                "forward_url": row.forward_url,
                "forward_dynamic_data": (
                    json.loads(row.forward_dynamic_data)
                    if row.forward_dynamic_data
                    else None
                ),
            }
            dynamic_list.append(dynamic)

        return dynamic_list, total
    finally:
        # 确保 session 在完成后关闭
        session.close()
