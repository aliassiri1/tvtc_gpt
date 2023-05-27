from flask import Flask, render_template, request
import requests
import json
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    # Process the search query and generate the search result
    system = '''You are TVTC_GPT designed to answer user queries. You are not allowed to answer questions related to politics. Reply in a way that make user query as a topic and your reponse as answer
    Example respone:
    Topic: query_topic
    Response: your_response'''
    context = [{"role": "system", "content":system},
               {"role": "user", "content":query}]
    
    search_result = get_response(context)  # Replace with your search function
    if "<class 'dict'>" in str(type(search_result)):
        return render_template('index.html', search_result= search_result["Response"], search_title = search_result["Topic"])
    
    return render_template('index.html', search_result= str(search_result), search_title = "Not Allowed")

@app.route('/random', methods=['POST'])
def random():
    query = "Give me every run different examples of past tense in English"
    # Process the search query and generate the search result
    system = '''You are TVTC_GPT designed to answer user queries. You are not allowed to answer questions related to politics.'''
    context = [{"role": "system", "content":system},
               {"role": "user", "content":query}]
    
    search_result = get_response(context)  # Replace with your search function
    if "<class 'dict'>" in str(type(search_result)):
        return render_template('index.html', search_result= search_result["Response"], search_title = search_result["Topic"])
    
    return render_template('index.html', search_result= str(search_result), search_title = "Past Tense Examples")

def get_response(context):
    # Replace YOUR_API_KEY with your actual API key
    api_key = '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'

    # Set the API endpoint
    url = "https://api.openai.com/v1/chat/completions"

    # Set the request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Set the request body
    data = {
        "model": "gpt-3.5-turbo",
        "messages": context,
        "max_tokens": 1000,
        "temperature": 0
    }

    try:
        # Send the request and get the response
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Parse the response JSON and return the generated text
        response_data = json.loads(response.text)
        pattern = r'Topic:\s*([^:]+)\nResponse:\s*([\s\S]*)'

        match = re.search(pattern, response_data["choices"][0]['message']['content'])
        print(response_data["choices"][0]['message']['content'])
        
        if match:
            topic = match.group(1)
            response = match.group(2).strip()

            result_dict = {'Topic': topic, 'Response': response}
            print(result_dict)
            return result_dict
        else:
            return response_data["choices"][0]['message']['content']
    except:
        return {'Topic': 'API ERROR', "Response": "There was an error while fetching results from API make sure you have stable internet connection.\n\nTry again.."}


if __name__ == '__main__':
    app.run(debug=True)
