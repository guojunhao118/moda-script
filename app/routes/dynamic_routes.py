from flask import Blueprint, request, jsonify
from app.services.dynamic import get_dynamic_list_from_db

dynamic_routes = Blueprint("dynamic_routes", __name__)


@dynamic_routes.route("/list", methods=["GET"])
def get_dynamic_list():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    try:
        dynamic_list, total = get_dynamic_list_from_db(page, page_size)
        # 包装返回结果为统一格式
         # 包装返回结果为统一格式
        response = {
            "msg": "Success",
            "code": 200,
            "data": {
                "list": dynamic_list,
                "total": total,
                "page": page,
                "page_size": page_size
            }
        }
        return jsonify(response), 200
    except Exception as e:
        # 错误返回格式
        response = {"msg": str(e), "code": 500, "data": None}
        return jsonify(response), 500
