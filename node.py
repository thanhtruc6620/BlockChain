from flask import Flask, request, jsonify, render_template
import requests
from blockchain import create_new_block, create_genesis_block
from flask import Flask, request, jsonify, render_template
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
app = Flask(__name__,template_folder='C:/Truc/blockchain/template')

problem_data = None

@app.route("/", methods=["GET"])
def index():
    return render_template("node.html")

@app.route("/get_problem", methods=["GET"])
def get_problem():
    global problem_data
    if problem_data is not None:
        return jsonify(problem_data)
    else:
        return jsonify({"message": "Không có bài toán"})

@app.route("/submit_solution", methods=["POST"])
def submit_solution():
    data = request.get_json()
    solution = data.get("solution")
    # Gửi giải pháp lên Server qua yêu cầu POST
    server_url = "http://localhost:5000/submit_solution"
    headers = {"Content-Type": "application/json"}
    response = requests.post(server_url, headers=headers, json=data)
    solution_status = response.json()
    return jsonify(solution_status)
@app.route("/new_problem", methods=["POST"])
def new_problem():
    global problem_data
    data = request.get_json()
    problem_data = data
    return jsonify({"message": "Đã nhận bài toán mới từ server"})

blockchain = [create_genesis_block()]
@app.route('/mine', methods=['GET'])  # Định nghĩa route /mine
def mine():
    # Tạo chuỗi blockchain và thêm một số khối vào đó (giống như trong ví dụ trước)
    data = f"heloo"
    new_block = create_new_block(data, blockchain)
    blockchain.append(new_block)
    return jsonify({"message": "kkk"})

    # # Chuyển đổi dữ liệu từ Python thành một danh sách JSON để gửi cho trình duyệt
    # blockchain_data = []
    # for block in blockchain:
    #     blockchain_data.append({
    #         'index': block.index,
    #         'previous_hash': block.previous_hash,
    #         'timestamp': block.timestamp,
    #         'data': block.data,
    #         'hash': block.hash
    #     })
    #
    # # Trả về dữ liệu dạng JSON
    # return jsonify(blockchain_data)
def receive_problem_from_server(problem):
    global problem_data
    problem_data = problem

if __name__ == "__main__":
    app.run(debug=True, port=5001)
