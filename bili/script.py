from datetime import datetime
from queue import Full
import requests
import logging
from time import sleep
from db.db_utils import save_dynamic_to_db  # 导入数据库操作模块

# 示例 UP 主信息
UP = {
    "mid": "525121722",  # 目标 UP 主的 mid
    "name": "莫大韭菜",
    "offset": "0",  # 偏移量，首次从 0 开始
}
headers_bili={
    'Accept': 'application/json, text/plain, */*',
    'Connection': 'keep-alive',
    'Cookie': '',
    'Host': 'api.bilibili.com',
    'Origin': 'https://space.bilibili.com',
    'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
}


# 获取并保存动态
def getAllDynamic():
    global UP

    url = f'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid={UP["mid"]}'
    if UP['offset'] and UP['offset'] != '0':  # 检查 offset 是否为空或 '0'
        url += f'&offset={UP["offset"]}'
    res = requests.get(url,headers=headers_bili).json()

    print(f"动态数据返回{res}")

    # 检查返回数据
    if "data" not in res:
        logging.info(UP["name"] + "动态：返回json不包含data字段")
        return

    dynamic_list = res["data"]["items"]
    has_more = res["data"].get("has_more", False)
    offset = res["data"].get("offset", 0)

    # 遍历获取的动态
    for dynamic in dynamic_list:
        dynamic_data = extract_dynamic_data(dynamic)
        save_dynamic_to_db(dynamic_data)

    # 如果有更多动态，递归调用以获取更多数据
    if has_more:
        UP["offset"] = offset  # 更新 offset 参数
        getAllDynamic()


# 从动态中提取所需数据
def extract_dynamic_data(dynamic):
    """根据动态类型提取数据"""
    basic = dynamic.get("basic", {})
    author = dynamic.get("modules", {}).get("module_author", {})
    stat = dynamic.get("modules", {}).get("module_stat", {})
    module_dynamic = dynamic.get("modules", {}).get("module_dynamic", {})

    # 提取基础信息
    comment_id = basic.get("comment_id_str", "")
    dynamic_type = dynamic.get("type", "")
    is_only_fans = basic.get("is_only_fans", False)  # 充电专属
    # 动态唯一id
    dynamic_id = dynamic.get("id_str", "")

    # 提取作者信息
    author_name = author.get("name", "")
    author_mid = author.get("mid", "")
    author_face = author.get("face", "")
    pub_time = datetime.fromtimestamp(author.get("pub_ts", ""))

    # 初始化内容
    dynamic_desc = ""
    media_urls = []

    if dynamic_type == "DYNAMIC_TYPE_AV":
        # 处理视频类型的动态
        archive = module_dynamic.get("major", {}).get("archive", {})

        video_title = archive.get("title", "")
        video_duration = archive.get("duration_text", "")
        video_cover = archive.get("cover", "")
        video_url = archive.get("jump_url", "")
        jump_url = f"https:{video_url}"

        # 附件：视频封面和播放数、弹幕数等
        media_urls = [video_cover]  # 仅处理封面图

        dynamic_desc = f"视频：{video_title} ({video_duration}) - {jump_url}"

        # 获取互动数据
        like_count = stat.get("like", {}).get("count", 0)
        forward_count = stat.get("forward", {}).get("count", 0)
        comment_count = stat.get("comment", {}).get("count", 0)

        return {
            "dynamic_id": dynamic_id,
            "comment_id": comment_id,
            "dynamic_type": dynamic_type,
            "jump_url": jump_url,
            "author_name": author_name,
            "author_mid": author_mid,
            "author_face": author_face,
            "dynamic_desc": dynamic_desc,
            "like_count": like_count,
            "forward_count": forward_count,
            "comment_count": comment_count,
            "is_only_fans": is_only_fans,
            "pub_time": pub_time,
            "media_urls": media_urls,
        }

    elif dynamic_type == "DYNAMIC_TYPE_WORD":
        base_url = "https://t.bilibili.com/"
        jump_url = f"{base_url}{dynamic_id}"

        print(f"跳转链接{jump_url}")
        # 处理文本类型的动态
        dynamic_desc = extract_dynamic_desc(dynamic)
        # 这里假设文本动态没有视频封面，直接处理文本数据

        # 获取互动数据
        like_count = stat.get("like", {}).get("count", 0)
        forward_count = stat.get("forward", {}).get("count", 0)
        comment_count = stat.get("comment", {}).get("count", 0)

        return {
            "dynamic_id": dynamic_id,
            "comment_id": comment_id,
            "dynamic_type": dynamic_type,
            "jump_url": jump_url,
            "author_name": author_name,
            "author_mid": author_mid,
            "author_face": author_face,
            "dynamic_desc": dynamic_desc,
            "like_count": like_count,
            "forward_count": forward_count,
            "comment_count": comment_count,
            "is_only_fans": is_only_fans,
            "pub_time": pub_time,
            "media_urls": media_urls,
        }

    elif dynamic_type == "DYNAMIC_TYPE_DRAW":
        base_url = "https://t.bilibili.com/"
        jump_url = f"{base_url}{dynamic_id}"
        # 处理绘画类型的动态
        dynamic_desc = extract_dynamic_desc(dynamic)
        pics = (
            dynamic.get("modules", {})
            .get("module_dynamic", {})
            .get("major", {})
            .get("draw", {})
            .get("items", [])
        )

        # 遍历 pics 数组，提取每个图片的 url 并添加到 media_urls 列表中
        for pic in pics:
            media_urls.append(pic["src"])

        # 获取互动数据
        like_count = stat.get("like", {}).get("count", 0)
        forward_count = stat.get("forward", {}).get("count", 0)
        comment_count = stat.get("comment", {}).get("count", 0)

        return {
            "dynamic_id": dynamic_id,
            "comment_id": comment_id,
            "dynamic_type": dynamic_type,
            "jump_url": jump_url,
            "author_name": author_name,
            "author_mid": author_mid,
            "author_face": author_face,
            "dynamic_desc": dynamic_desc,
            "like_count": like_count,
            "forward_count": forward_count,
            "comment_count": comment_count,
            "is_only_fans": is_only_fans,
            "pub_time": pub_time,
            "media_urls": media_urls,
        }

    elif dynamic_type == "DYNAMIC_TYPE_FORWARD":
        jump_url = basic.get("jump_url", "")
        # 处理转发类型的动态
        forward_dynamic = dynamic.get("orig", {})

        forward_data = extract_dynamic_data(forward_dynamic)  # 递归提取转发的动态数据

        # 提取转发的基本信息
        forward_title = forward_data.get("dynamic_desc", "")
        forward_author_name = forward_data.get("author_name", "")
        forward_url = forward_data.get("jump_url", "")

        # 获取互动数据
        like_count = stat.get("like", {}).get("count", 0)
        forward_count = stat.get("forward", {}).get("count", 0)
        comment_count = stat.get("comment", {}).get("count", 0)

        return {
            "dynamic_id": dynamic_id,
            "comment_id": comment_id,
            "dynamic_type": dynamic_type,
            "jump_url": jump_url,
            "author_name": author_name,
            "author_mid": author_mid,
            "author_face": author_face,
            "dynamic_desc": f"转发动态: {forward_data.get('dynamic_desc', '')}",
            "like_count": like_count,
            "forward_count": forward_count,
            "comment_count": comment_count,
            "is_only_fans": is_only_fans,
            "pub_time": pub_time,
            "media_urls": media_urls,
            "forward_title": forward_title,  # 转发视频的标题
            "forward_author_name": forward_author_name,  # 转发用户
            "forward_url": forward_url,  # 转发视频的跳转地址
            "forward_dynamic_data": forward_data,  # 保存转发的数据
        }

    else:
        # 对于其他类型，暂不处理，返回一个空字典或其他适合的内容
        return {}


# 提取动态描述（文字、表情）
def extract_dynamic_desc(dynamic):
    """提取动态描述的文本与表情"""
    dynamic_desc = ""

    # 逐层检查每个字段是否是字典
    modules = dynamic.get("modules", {}) if isinstance(dynamic, dict) else {}
    module_dynamic = (
        modules.get("module_dynamic", {}) if isinstance(modules, dict) else {}
    )
    # major = module_dynamic.get("major", {}) if isinstance(module_dynamic, dict) else {}
    # opus = major.get("opus", {}) if isinstance(major, dict) else {}
    # summary = opus.get("summary", {}) if isinstance(opus, dict) else {}
    desc = module_dynamic.get("desc", {}) if isinstance(module_dynamic, dict) else {}
    rich_text_nodes = desc.get("rich_text_nodes", []) if isinstance(desc, dict) else []

    # print(f"获取动态详情==={rich_text_nodes}")
    for node in rich_text_nodes:
        # 检查节点是否是字典类型，防止访问 .get 出错
        if isinstance(node, dict):
            node_type = node.get("type")
            if node_type == "RICH_TEXT_NODE_TYPE_TEXT":
                dynamic_desc += node.get("text", "")
            elif node_type == "RICH_TEXT_NODE_TYPE_EMOJI":
                dynamic_desc += f"[{node.get('text', '')}]"

    # print(f"获取动态详情{dynamic_desc}")
    return dynamic_desc


# 提取媒体信息（图片、表情等）
def extract_media(dynamic):
    """提取动态中的媒体信息（如图片、表情）"""
    media_urls = []

    # 处理动态中附带的图片（如果有）
    pics = (
        dynamic.get("modules", {})
        .get("module_dynamic", {})
        .get("major", {})
        .get("opus", {})
        .get("pics", [])
    )
    for pic in pics:
        if pic.get("url"):
            media_urls.append(pic["url"])

    # 处理表情（如果有）
    rich_text_nodes = (
        dynamic.get("modules", {})
        .get("module_dynamic", {})
        .get("major", {})
        .get("summary", {})
        .get("rich_text_nodes", [])
    )
    for node in rich_text_nodes:
        if node["type"] == "RICH_TEXT_NODE_TYPE_EMOJI":
            emoji_url = node.get("emoji", {}).get("icon_url", "")
            if emoji_url:
                media_urls.append(emoji_url)

    return media_urls
