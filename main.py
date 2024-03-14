import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.rag.bot import create_bot
from src.common.common_chat import common_chat

app = Flask(__name__)
CORS(app, origins='*')

# 上传文件的保存目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

bot = create_bot(document_url = "__local_doc__/物理安全规定.pdf")

@app.route('/rag-chat',methods=["POST"])
def rag_chat():
    # 接收到一个/chat请求
    user_input = request.json['text']
    message = bot.chat(user_input)
    return jsonify({'message': message})

@app.route('/chat',methods=["POST"])
def chat():
    # 接收到一个/chat请求
    user_input = request.json['text']
    message = common_chat(user_input)
    return jsonify({'message': message})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '没有文件上传'
    
    file = request.files['file']

    if file.filename == '':
        return '没有选择文件'

    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return '文件上传成功'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)