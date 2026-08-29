"""示例 API:登录接口。仅供 api-tester 技能演示。"""

from flask import Flask, jsonify, request

app = Flask(__name__)

USERS = {
    "admin": "correct-password",
}


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"code": 400, "message": "username 和 password 必填"}), 400
    if USERS.get(username) != password:
        return jsonify({"code": 401, "message": "账号或密码错误"}), 401
    return jsonify({"code": 0, "token": "demo-token-123"}), 200


if __name__ == "__main__":
    app.run(port=8000)
