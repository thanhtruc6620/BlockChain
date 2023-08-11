import json
import random
import blockchain
from blockchain import create_new_block
import requests
from flask import Flask, request, jsonify
import hashlib
import time
from flask import Flask, request, jsonify, render_template
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
app = Flask(__name__,template_folder='C:/Truc/blockchain/template')
jinja_env = Environment(loader=FileSystemLoader('template'))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
@app.route("/get_problem", methods=["GET"])
def get_problem():
    # Định nghĩa bài toán (ví dụ: giải phương trình bậc 2)
    global reward
    reward = random.randint(10, 100)
    problem_data = {
        "description": "Tính: ",
        "data": "1+1=",
        "reward": reward
    }
    return jsonify(problem_data)
@app.route("/get_problem2", methods=["GET"])
def get_problem2():
    # Định nghĩa bài toán (ví dụ: giải phương trình bậc 2)
    problem_data = {
        "description": "problem 2 ",
        "data": "1+1=",
        "reward": random.randint(2, 100)
    }
    return jsonify(problem_data)
@app.route("/submit_solution", methods=["POST"])
def submit_solution():
    if check() == 1:
        return jsonify({"message": "Đáp án chính xác!"})
    else:
        return jsonify({"message": "Đáp án không chính xác!"})
from blockchain import Block
@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    solution = data.get("solution")
    if int(solution) == 2:
        return 1
        #return jsonify({"message": "Đáp án chính xác!"})
    else:
        return 2
        #return jsonify({"message": "Đáp án không chính xác!"})
blockchain = [blockchain.create_genesis_block()]
@app.route('/mine', methods=['GET'])  # Định nghĩa route /mine
def mine():
    # Tạo chuỗi blockchain và thêm một số khối vào đó (giống như trong ví dụ trước)
    print(reward)
    data = f"{reward}"
    new_block = create_new_block(data, blockchain)
    blockchain.append(new_block)
    # Chuyển đổi dữ liệu từ Python thành một danh sách JSON để gửi cho trình duyệt

    return jsonify({"message": "hihi"})

@app.route("/get_reward", methods = ['GET'])
def get_reward():
    return jsonify(reward)
@app.route("/display", methods = ["GET"])
def display():
    # Chuyển đổi dữ liệu từ Python thành một danh sách JSON để gửi cho trình duyệt
    blockchain_data = []
    for block in blockchain:
        blockchain_data.append({
            'index': block.index,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'data': block.data,
            'hash': block.hash
        })
    # Trả về dữ liệu dạng JSON
    return jsonify(blockchain_data)
@app.route("/new_problem", methods=["POST"])
def new_problem():
    data = request.get_json()

    # Forward the problem to the node through the "/new_problem" route
    node_url = "http://localhost:5001/new_problem"
    headers = {"Content-Type": "application/json"}
    response = requests.post(node_url, headers=headers, json=data)

    if response.status_code == 200:
        return jsonify(reward)
    else:
        return jsonify({"message": "Lỗi khi gửi bài toán cho node!"})

@app.route("/new_problem2", methods=["POST"])
def new_problem2():
    data = request.get_json()

    # Forward the problem to the node through the "/new_problem" route
    node_url = "http://localhost:5002/new_problem"
    headers = {"Content-Type": "application/json"}
    response = requests.post(node_url, headers=headers, json=data)

    if response.status_code == 200:
        return jsonify(reward)
    else:
        return jsonify({"message": "Lỗi khi gửi bài toán cho node!"})
if __name__ == "__main__":
    app.run(debug=True)
