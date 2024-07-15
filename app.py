from flask import Flask , request , jsonify
from gradio_client import Client
import json
import google.generativeai as genai
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def step1(query):

    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash",
      generation_config=generation_config,
      system_instruction="you are a Course maker who makes index pages of courses based on the topi of the course , you take the main topic name of the course and generate a list of subtopics in json format\n\nhere is structure of json you should generate, \n{maintopic : name of the main topic , subtopics:[subtopic1 , subtopic2 , subtopic3 , .....]}",
    )
    
    chat_session = model.start_chat(
      history=[
      ]
    )
    
    response = chat_session.send_message(query)
    
    result = response.text
    j_str = result.replace('\n' , '')

    sind = 0
    eind = 0
    for i in range(0 , len(j_str)):
        if j_str[i] == '{':
            sind = i
            break;

    for i in range(0, len(j_str)+1):

        if j_str[i*-1] == '}':
            eind = -1*i
            break;

    json_obj = json.loads(j_str[sind:eind+1])
    return jsonify(json_obj)


def step2(query):

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash",
      generation_config=generation_config,
      # safety_settings = Adjust safety settings
      # See https://ai.google.dev/gemini-api/docs/safety-settings
      system_instruction="you are a AI Course Crafter , who create courses on a given topic , the courses you make are very nice clear and would give a clear understanding to both complete beginners and experts , the course you generate should contain topic name , explanation , syntax of the topic , and an example\n\nhere is structure of json you should generate, \n{maintopic: topic name should be here , explanation : content explaining the topic   , syntax: syntax of topic , example : example of the topic you are explaining }\n\nfollow the json structure and generate a nice course in json format see that the json you generate is valid and is having a structured format as mentioned see that you donot dicturbe the structure of json , or else we will be getting parsing erros , the json you generate should be same as i mentioned dont add or remove anything or create extra inner key value pairs even if it is required , The user will just provide you the topic name you should genrate the content for it in the mentioned json struture, Dont ask for any extra things or anything just genrate the suitable and perfect course content for user mentioned topic",
    )
    
    chat_session = model.start_chat(
      history=[
      ]
    )
    
    response = chat_session.send_message(content= query)
    
    result =  response.text

    j_str = result.replace('\n' , '')
    
    

    sind = 0
    eind = 0
    for i in range(0 , len(j_str)):
        if j_str[i] == '{':
            sind = i
            break;

    for i in range(0, len(j_str)+1):

        if j_str[i*-1] == '}':
            eind = -1*i
            break;
    
    if eind == -1:
        eind = -2

    print(j_str[sind:eind+1] , '================================================================================================')    
    try:
     json_obj = json.loads(j_str[sind:eind+1])
     return jsonify(json_obj)
    except:
     json_obj = {"maintopic" : "unable to generate" , "explanation": "Please wait we are working on it" , "syntax": "json parsing error" , "example" : "we are in beta version and looking to solve this error"}
     json_obj = json.loads(json_obj)
     return jsonify(json_obj)

app = Flask(__name__)

CORS(app , origins=["http://localhost:3000" , "https://coursecrafter-nine.vercel.app"])
@app.route('/generate_topics', methods=['POST'])
def generate_sts():
    user_query = request.form['query']
    step1_output = step1(user_query)
    return step1_output


@app.route('/generate_contents/<user_query>')
def generate_st_content(user_query):
    step2_output = step2(user_query)
    return step2_output       



if __name__ == '__main__':
    app.run(host = '0.0.0.0' , debug=True)