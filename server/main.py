from dotenv import load_dotenv
from flask import Flask, request, jsonify 
from modules import llm, omnicomplete, omnicomplete_flag
from flask_cors import CORS
import time 

# connecting to OpenAI for moderations
import os
from openai import OpenAI 
load_dotenv()
apikey = os.getenv("ORGANIZATION_OPENAI_KEY") 
print("API KEY HERE", apikey) 
client = OpenAI( api_key=apikey )

app = Flask(__name__)
CORS(app)

topics = [("Vue.js", "vuejs")]
topic_index = 0

# check if moderated
# in get_autocomplete  -- do not autocomplete if
# start of prompt is inappropriae
def check_moderation(input_data): 
    print("INPUT DATA", input_data)
    response = client.moderations.create(input=input_data)
    output = response.results[0]
    # print("HEREEEEEEEE")
    # print("OUTPUT", output)
    print("Flagged:", output.flagged)
    return output.flagged


@app.route("/get-autocomplete", methods=["POST"])
def get_autocomplete():
    start_time = time.time() 
    input_data = request.json["input"]
    
#    flagged = check_moderation(input_data)
    flagged = False 
    if not flagged: # check_moderation(input_data):  
        print("NOT MODERATED")
        
        print("topics[topic_index][0])", topics[topic_index][0]) 
        print("topic_dir" , topics[topic_index][1])

        prompt = omnicomplete.build_omni_complete_prompt(
            input_data, topic=topics[topic_index][0], topic_dir=topics[topic_index][1]
        )

        # print("prompt", prompt)

        response = llm.prompt_json(prompt)
        # print("Prompt: " , prompt)
        # print("Response: ", response)

        end_time = time.time() 
        run_time = str(int((end_time - start_time) * 100)/100)

        # print("Getting new autocomplete " + run_time)
        print("RESPONSE", response)

        return jsonify(response)
    else: 
        print("MODERATED")

    return 


@app.route("/use-autocomplete", methods=["POST"])
def do_autocomplete():
    start_time = time.time() 
    autocomplete_object = request.json
    # print(autocomplete_object)
    input_data = autocomplete_object["input"]
    completion = autocomplete_object["completion"]
    print(f"Received autocomplete object: input={input_data}, completion={completion}")
    #print("INCREMENT COMPLETIONS") 
    # True if appropriate 
    if_appropriate = check_flagged(input_data + completion) 
    if if_appropriate: 
        omnicomplete.increment_or_create_previous_completions(
            input_data, completion, topics[topic_index][1]
        )
        return jsonify(success=True)
        print("Flagged as appropriate")
    else: 
        print("Flagged as not appropriate")
    return jsonify(success=False)


def check_flagged(input_data):
    prompt = omnicomplete_flag.build_flag(
    input_data, topic=topics[topic_index][0], topic_dir=topics[topic_index][1]
)
    response = llm.prompt_json_flag(prompt)
    print("THIS RESPONSE") 
    print(response) 
    if "True" in response: 
        return True
    return False 

if __name__ == "__main__":
    app.run(debug=True)
