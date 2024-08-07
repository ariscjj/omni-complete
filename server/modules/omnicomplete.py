import json
import os
import greet

PROMPT_ROOT_DIR = os.getenv("PROMPT_ROOT_DIR")

def build_omni_complete_prompt(input_value, topic="Vue.js", topic_dir="vuejs"):
    PROMPT_ROOT_DIR = "/Users/ariszhu/Documents/__Instalily/omni-complete/prompt_tests/omnicomplete"
    prompt = open(f"{PROMPT_ROOT_DIR}/prompt.txt", "r").read()

    previous_completions = open(
        f"{PROMPT_ROOT_DIR}/knowledge_bases/{topic_dir}/previous_completions.json", "r"
    ).read()

    domain_knowledge = open(
        f"{PROMPT_ROOT_DIR}/knowledge_bases/{topic_dir}/domain_knowledge.txt", "r"
    ).read()

    prompt = prompt.replace("{{topic}}", topic)
    prompt = prompt.replace("{{previous_completions}}", previous_completions)
    prompt = prompt.replace("{{domain_knowledge}}", domain_knowledge)
    prompt = prompt.replace("{{input_value}}", input_value)
    return prompt

# UNCOMMENT FOR EMBEDDINGS 
# def increment_or_create_previous_completions(input, completion, topic_dir):
    # new_query = input 

    # UNCOMMENT FOR EMBEDDINGS  
    # matched_query, max_embedding = find_closest_query(new_query)
    
    # matched_query = 1 

    # if matched_query is not None:
        # INCREASE QUERY COUNT 
        # query_embedding_store[matched_query]["completions"][completion][1] += 1 
        # print(f"New query matches with '{matched_query}' with similarity {similarity}")

    # else:
        # new_embedding = add_new_query(new_query, new_completion)

    # previous_completions_file = (
        # f"{PROMPT_ROOT_DIR}/knowledge_bases/{topic_dir}/previous_completions.json"
    # )
  
    # IS THIS NEEDED? 
    # completions_sorted_by_hits = sorted(
        # previous_completions, key=lambda x: x["hits"], reverse=True
    # )

    #write back to file
    # with open(previous_completions_file, "w") as f:
        # json.dump(completions_sorted_by_hits, f, indent=4)


def increment_or_create_previous_completions(input, completion, topic_dir):
    previous_completions_file = (
        f"{PROMPT_ROOT_DIR}/knowledge_bases/{topic_dir}/previous_completions.json"
    )

    """
    [
        {
            "input": "style this button with",
            "completions": [
                "tailwindcss and make it look like a switch",
                "unocss and make it look like a switch"
            ],
            "hits": [5, 3] 
        },
    ...
    ]
    """
    previous_completions = open(previous_completions_file, "r").read()

    previous_completions = json.loads(previous_completions)
    for item in previous_completions: 
        if item["input"].lower() == input.lower(): 
            complist = item["completions"] 
            hitlist = item["hits"] 
            found = False
            for i in range(len(complist)):
                if completion.lower() == complist[i].lower(): 
                    print("Previous completion matched!!") 
                    found = True 
                    hitlist[i] += 1
                    
                    #sort completions based on popularity only if
                    # if new hit count is higher 
                    if i > 0: 
                        if hitlist[i] > hitlist[i-1]: 
                            paired = list(zip(hitlist, complist))
                            sorted_paired = sorted(paired, key=lambda x: x[0]) 
                            sorted_phrases = [phrase for count, phrase in sorted_paired] 
                            sorted_counts = [count for count, phrase in sorted_paired] 
                            item["completions"] = sorted_phrases 
                            item["hits"] = sorted_counts 
                            print(sorted_phrases) 
                    break 

            if not found: 
                item["completions"].append(completion) 
                item["hits"].append(1) 
    else:
        print("completely new completion") 
        new_completion = {"input": input, "completions": [completion], "hits": [1]}
        previous_completions.append(new_completion)

    # completions sorted by top hit 
    completions_sorted_by_hits = sorted(
        previous_completions, key=lambda x: x["hits"][0], reverse=True
    )

   # write back to file
    with open(previous_completions_file, "w") as f:
        json.dump(completions_sorted_by_hits, f, indent=4)
