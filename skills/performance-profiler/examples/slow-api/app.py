"""基准示例用的慢接口。"""

import time

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/api/items")
def items():
    time.sleep(0.05)  # 模拟慢接口
    return jsonify({"count": 100})


if __name__ == "__main__":
    app.run(port=8001)
