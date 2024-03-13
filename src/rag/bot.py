from .extract_pdf import extract_text_from_pdf
from .rag_chat import get_embeddings, get_completion
from .vectorDB import MyVectorDBConnector
from .RAG_Bot import RAG_Bot



# for para in results['documents'][0]:
#     print(para+"\n")
# for para in paragraphs:
#     print(para+"\n")

# 创建一个RAG机器人
# bot = RAG_Bot(
#     vector_db,
#     llm_api=get_completion,
#     n_results= 5
# )

def create_db(document_url):
    paragraphs = extract_text_from_pdf(document_url, min_line_length=10)
    print("正在切割文档")
    # 创建一个向量数据库对象
    vector_db = MyVectorDBConnector("demo", get_embeddings)
    # 向向量数据库中添加文档
    vector_db.add_documents(paragraphs)
    return vector_db

def create_bot(document_url): 
    vector_db = create_db(document_url)
    # 创建一个RAG机器人
    bot = RAG_Bot(
        vector_db,
        llm_api=get_completion,
        n_results= 5
    )
    return bot