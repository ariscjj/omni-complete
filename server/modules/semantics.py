import time

from gptcache import Cache, Config
from gptcache.adapter import openai
from gptcache.adapter.api import init_similar_cache
from gptcache.embedding import Onnx
from gptcache.manager import manager_factory
from gptcache.processor.post import random_one
from gptcache.processor.pre import last_content
from gptcache.similarity_evaluation import OnnxModelEvaluation

openai_complete_cache = Cache()
encoder = Onnx()
sqlite_faiss_data_manager = manager_factory(
    "sqlite,faiss",
    data_dir="openai_complete_cache",
    scalar_params={
        "sql_url": "sqlite:///./openai_complete_cache.db",
        "table_name": "openai_chat",
    },
    vector_params={
        "dimension": encoder.dimension,
        "index_file_path": "./openai_chat_faiss.index",
    },
)
onnx_evaluation = OnnxModelEvaluation()
cache_config = Config(similarity_threshold=0.75)

init_similar_cache(
    cache_obj=openai_complete_cache,
    pre_func=last_content,
    embedding=encoder,
    data_manager=sqlite_faiss_data_manager,
    evaluation=onnx_evaluation,
    post_func=random_one,
    config=cache_config,
)

questions = [
    "what's github",
    "can you explain what GitHub is",
    "can you tell me more about GitHub",
    "what is the purpose of GitHub",
]

for question in questions:
    start_time = time.time()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}],
        cache_obj=openai_complete_cache,
    )
    print(f"Question: {question}")
    print("Time consuming: {:.2f}s".format(time.time() - start_time))
    print(f'Answer: {response["choices"][0]["message"]["content"]}\n')
