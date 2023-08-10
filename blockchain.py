import hashlib
import time
import requests
import json
from datetime import datetime

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = datetime.now()
        self.data = data
        self.hash = hash
        self.nonce = nonce

def calculate_hash(index, previous_hash, timestamp, data, nonce):
    return hashlib.sha256(f"{index}{previous_hash}{timestamp}{data}{nonce}".encode()).hexdigest()

def proof_of_work(block, difficulty):
    target = "0" * difficulty
    while block.hash[:difficulty] != target:
        block.nonce += 1
        block.hash = calculate_hash(block.index, block.previous_hash, block.timestamp, block.data, block.nonce)
    print("Khối:",block.index,"||", block.previous_hash,"||",  block.hash ,"||",  block.timestamp,"||",  block.data,"||")

def create_genesis_block():
    return Block(0, "0", time.time(), "Genesis Block", "", 0)

def create_new_block(data, blockchain):
    data = f"{data}"
    previous_block = blockchain[-1]
    new_index = previous_block.index + 1
    new_timestamp = time.time()
    new_hash = calculate_hash(new_index, previous_block.hash, new_timestamp, data, 0)
    new_block = Block(new_index, previous_block.hash, new_timestamp, data, new_hash, 0)
    proof_of_work(new_block, 4)  # 4 là một số khó (difficulty) tùy chọn
    return new_block

def is_chain_valid(chain, difficulty):
    for i in range(1, len(chain)):
        current_block = chain[i]
        previous_block = chain[i - 1]

        # Kiểm tra tính toàn vẹn của khối hiện tại
        if current_block.hash != calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data, current_block.nonce):
            return False

        # Kiểm tra tính toàn vẹn của chuỗi
        if current_block.previous_hash != previous_block.hash:
            return False

        # Kiểm tra cơ chế PoW
        target = "0" * difficulty
        if current_block.hash[:difficulty] != target:
            return False

    return True

from flask import Flask, request, jsonify, render_template
# class Node:
#     def __init__(self):
#         self.chain = [create_genesis_block()]
#         self.pending_transactions = []
#         self.server_url = 'http://127.0.0.1:5000'
#
#     def mine_block(self,data):
#         data = f"{data}"
#         previous_block = self.chain[-1]
#         new_index = previous_block.index + 1
#         new_timestamp = time.time()
#         new_hash = calculate_hash(new_index, previous_block.hash, new_timestamp, data, 0)
#         new_block = Block(new_index, previous_block.hash, new_timestamp, data, new_hash, 0)
#         self.chain.append(new_block)
#         self.pending_transactions = []
#
#         # Gửi khối mới đến server để nạp vào blockchain chung
#         self.send_block_to_server(new_block.__dict__)
#
#     def add_transaction(self, transaction):
#         self.pending_transactions.append(transaction)
#
#     def send_block_to_server(self, block_data):
#         url = f'{self.server_url}/add_block'
#         headers = {'Content-Type': 'application/json'}
#         response = requests.post(url, json=block_data, headers=headers)
#         if response.status_code == 200:
#             print('Block added to server successfully')
#         else:
#             print('Error adding block to server')

# import random
# problem_data = {
#         "description": "Giải phương trình bậc 2",
#         "data": {
#             "a": random.randint(1, 10),
#             "b": random.randint(1, 10),
#             "c": random.randint(1, 10)
#         },
#         "reward" : random.randint(20,200)
#     }
# data = f"{problem_data}"

# new_block = create_new_block(data,blockchain)
# blockchain.append(new_block)
# difficulty = 4  # Độ khó của cơ chế PoW
# if is_chain_valid(blockchain, difficulty):
#     print("Hợp lệ")
# else:
#     print("Không hợp lệ")