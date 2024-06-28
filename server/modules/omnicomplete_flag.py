import json
import os

PROMPT_ROOT_DIR = os.getenv("PROMPT_ROOT_DIR")

def build_flag(input_value, topic, topic_dir):
    prompt = open(f"{PROMPT_ROOT_DIR}/validity.txt", "r").read()
    domain_knowledge = open(
        f"{PROMPT_ROOT_DIR}/knowledge_bases/{topic_dir}/domain_knowledge.txt", "r"
    ).read()
    prompt = prompt.replace("{{domain_knowledge}}", domain_knowledge)
    prompt = prompt.replace("{{input_value}}", input_value)
    return prompt

