from openai import OpenAI
from flask import Flask, render_template, request, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri="mongodb+srv://PavSuppPar:NehaNishika@tablet.sqv9f.mongodb.net/?retryWrites=true&w=majority&appName=Tablet"

# Create a new client and connect to the server
MONGO_CLIENT = MongoClient(uri, server_api=ServerApi('1'))
DATABASE = MONGO_CLIENT['tablets']  
COLLECTION_TABLETS = DATABASE['medicine']

#@app.route('/')
#def home():
#    return "Hi"

#@app.route('/getdoctor', methods=['POST'])
#def get_doctor():
#    pass

@app.route('/fetch_health_data', methods=['POST'])
def fetch_health_data():

    # return "Hi Codelingo"
    #get the data from the request
    tablet_name = request.args.get('tablet_name')
    duration = request.args.get('duration')
    weight = request.args.get('weight')
    height = request.args.get('height')
    age = request.args.get('age')
    gender = request.args.get('gender')

    tablet_query = {
            "tablet_name_mongo": tablet_name
        }
    
    tablet_info = COLLECTION_TABLETS.find_one(tablet_query)

    side_effects = tablet_info['side_effects']

    # initialize the openai client
    openAIClient = OpenAI(api_key='')

    # Promting openai
    prompt = (f'A person with the following details:{weight} {height} {age} {gender} has taken {tablet_name} for {duration} days. The side effects of the medicine are {side_effects}.'
              f'Please give a brief summary of the person\'s health condition and any potential issues that may arise.'
              f'Also please suggest alternative medicines that may help the person.')

    response = openAIClient.chat.completions.create(
        model="gpt-4o",  # You can use different engines like 'text-curie-001' or 'text-ada-001'
        messages = [{
            "role": "user",
            "content": prompt
            }],
        max_tokens=100,  # Adjust the number of tokens as needed
        n=1,  # Number of responses you want
        stop=None,  # Define stopping criteria if needed
        temperature=0.8)

    generated_response = response.choices[0].message.content

    #print(generated_response)

    return generated_response

if __name__ == "__main__":
    app.run(debug=True)
