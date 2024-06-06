def increment_or_create_previous_completions(input, completion, topic_dir):
    # closest_query, sim  = find_closest_query(input) 
    # if closest_query is None: 
        # add_new_query(input)

    new_query = userinput
    matched_query, max_embedding = find_closest_query(new_query)

    if matched_query is not None:
        # INCREASE QUERY COUNT 
        query_embedding_store[matched_query][1] += 1 
        print(f"New query matches with '{matched_query}' with similarity {similarity}")

    else:
        # ADD A NEW QUERY AND INCREASE ITS COUNT TO 1 
        new_embedding = add_new_query(new_query)
        # previous_completions.append(new_completion)

    previous_completions_file = (
        f"{PROMPT_ROOT_DIR}/knowledge_bases/{topic_dir}/previous_completions.json"
    )
  
    # IS THIS NEEDED? 
    completions_sorted_by_hits = sorted(
        previous_completions, key=lambda x: x["hits"], reverse=True
    )

    # write back to file
    with open(previous_completions_file, "w") as f:
        json.dump(completions_sorted_by_hits, f, indent=4)
