from gradio_client import Client
import json


def step1(user_query):

    client = Client("kskkoushik135/coursecrafter" , hf_token ='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')
    result = client.predict(
            fn_name="step1",
            query= user_query,
            api_name="/predict"
    )
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
    return json_obj



print(step1('python'))