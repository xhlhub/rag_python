from .rag_chat import build_prompt, prompt_template
from .extract_pdf import extract_text_from_pdf
from .rag_chat import get_embeddings, get_completion
from .vectorDB import MyVectorDBConnector
import os
import glob
import pdb

class RAG_Bot:
    def __init__(self, document_dir, n_results=2):
        # 创建一个向量数据库对象
        vector_db = MyVectorDBConnector("rag_demo", get_embeddings)
        self.vector_db = vector_db
        self.llm_api = get_completion
        self.n_results = n_results
        self.document_dir = document_dir
        self.init_add_documents()

    def chat(self, user_query):
        # 1. 检索
        search_results = self.vector_db.search(user_query, self.n_results)
        # 2. 构建 Prompt
        prompt = build_prompt(
            prompt_template, info=search_results['documents'][0], query=user_query)
        print("prompt：",prompt)
        # 3. 调用 LLM
        response = self.llm_api(prompt)
        return response
    
    def init_add_documents(self):
        for pdf_file in glob.glob(os.path.join(self.document_dir, '*.pdf')):
            print("add document:", pdf_file)
            self.add_document(pdf_file)

    def add_document(self, file_path):
        # pdb.set_trace()  # 在这里设置断点

        paragraphs = extract_text_from_pdf(file_path, min_line_length=10)
        # pdb.set_trace()  # 在这里设置断点

        print("add document:", paragraphs[:3])
         # 向向量数据库中添加文档
        self.vector_db.add_documents(paragraphs)