from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# 加载环境变量
_ = load_dotenv(find_dotenv())

# 创建OpenAI客户端
client = OpenAI()