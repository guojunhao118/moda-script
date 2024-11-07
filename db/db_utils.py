import MySQLdb
import json
import logging

# 配置 MySQL 数据库连接
db = MySQLdb.connect(
    host="127.0.0.1", user="root", passwd="8819667wc", db="moda", port=3306
)
cursor = db.cursor()


def execute_query(query, params=None):
    """执行数据库查询操作，返回结果"""
    try:
        cursor.execute(query, params or ())
        db.commit()
        return cursor.fetchall()
    except Exception as e:
        db.rollback()
        logging.error(f"执行查询时发生错误: {e}")
        return None


def check_existing_dynamic(dynamic_id):
    """检查动态是否已经存在于数据库中"""
    query = "SELECT COUNT(*) FROM dynamic WHERE dynamic_id = %s"
    result = execute_query(query, (dynamic_id,))
    return result[0][0] > 0 if result else False


def save_dynamic_to_db(dynamic):
    """保存动态到数据库"""
    if check_existing_dynamic(dynamic["dynamic_id"]):
        logging.info(f"动态 {dynamic['dynamic_id']} 已存在，跳过保存")
        return

    # 将图片列表转化为 JSON 字符串
    images_json = json.dumps(dynamic["media_urls"])

    sql = """INSERT INTO dynamic (dynamic_id, comment_id, dynamic_type, jump_url, author_name, author_mid, author_face, dynamic_desc, like_count, forward_count, comment_count, is_only_fans, pub_time, media_urls, forward_title, forward_author_name, forward_url, forward_dynamic_data)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    params = (
        dynamic["dynamic_id"],
        dynamic["comment_id"],
        dynamic["dynamic_type"],
        dynamic["jump_url"],
        dynamic["author_name"],
        dynamic["author_mid"],
        dynamic["author_face"],
        dynamic["dynamic_desc"],
        dynamic["like_count"],
        dynamic["forward_count"],
        dynamic["comment_count"],
        dynamic["is_only_fans"],
        dynamic["pub_time"],
        images_json,
        dynamic.get("forward_title", ""),
        dynamic.get("forward_author_name", ""),
        dynamic.get("forward_url", ""),
        dynamic.get("forward_dynamic_data", {}),
    )

    execute_query(sql, params)
    logging.info(f"动态 {dynamic['dynamic_id']} 已保存")
