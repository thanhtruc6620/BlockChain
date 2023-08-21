from flask import Flask, request, jsonify, render_template
import requests
from blockchain import create_new_block, create_genesis_block
from flask import Flask, request, jsonify, render_template

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
app = Flask(__name__,template_folder='C:/Truc/blockchain/template')

problem_data = None

# Gán giá trị 0 cho biến walletValue trong localStorage
@app.route("/", methods=["GET"])
def index():
    walletValue = 0
    return render_template("node.html",walletValue = walletValue)

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
# @app.route("/get_wallet", methods=["POST"])
# def get_wallet():
#     global get_wallet
#     wallet = request.get_json()
#     get_wallet = wallet
#     return jsonify({"message": "Tiền đã vào ví"})
def new_problem():
    global problem_data
    data = request.get_json()
    problem_data = data
    return jsonify({"message": "Đã nhận bài toán mới từ server"})
def receive_problem_from_server(problem):
    global problem_data
    problem_data = problem

if __name__ == "__main__":
    app.run(debug=True, port=5001)
