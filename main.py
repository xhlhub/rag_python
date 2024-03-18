import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.rag.RAG_Bot import RAG_Bot
from src.common.common_chat import common_chat
import pdb
import threading


app = Flask(__name__)
CORS(app, origins='*')

# 上传文件的保存目录
UPLOAD_FOLDER = '__uploads__'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

# 创建rag bot
bot = RAG_Bot(
        n_results= 5,
        document_dir = app.config['UPLOAD_FOLDER']
    )

# 通用聊天
@app.route('/chat',methods=["POST"])
def chat():
    # 接收到一个/chat请求
    user_input = request.json['text']
    message = common_chat(user_input)
    return jsonify({'message': message})

# RAG聊天
@app.route('/rag-chat',methods=["POST"])
def rag_chat():
    # 接收到一个/chat请求
    user_input = request.json['text']
    message = bot.chat(user_input)
    return jsonify({'message': message})

# 用户添加知识库
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '没有文件上传'
    # print("file:",request.files)
    file = request.files['file']
    if file.filename == '':
        return '没有选择文件'
    if file:
        filename = file.filename
        file.path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # pdb.set_trace()
        file.save(file.path)

        # 使用多线程处理文档切割
        thread = threading.Thread(target=bot.add_document, args=(file.path,))
        thread.start()

        return '文件上传成功'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)