import json
import firebase_admin
# from firebase_admin import credentials, firestore
import vertexai
from vertexai.language_models import TextGenerationModel
from vertexai.generative_models import GenerationConfig, GenerativeModel
from google.cloud import firestore
from google.auth import compute_engine
import functions_framework


from markupsafe import escape


# Initialize Vertex AI
vertexai.init(project="bnb-blr-444504", location="asia-south1")

# Initialize Firebase Admin SDK
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {'projectId': 'bnb-blr-444504'})
# db = firestore.client()


# Vertex AI initialization
model = GenerativeModel(
    "gemini-1.5-flash-001",
    generation_config=GenerationConfig(temperature=0),
)

# @app.route('/get-travel-plan', methods=['POST'])
@functions_framework.http
def get_travel_plan(request):
    # Parse the incoming request
    request_json = request.get_json(silent=True)
    user_id = request_json.get('user_id')

    if not request_json:
        return json.dumps({'error': 'No JSON payload provided'}), 400

    input_prompt = request_json.get('prompt', '')
    if not input_prompt:
        return json.dumps({'error': 'Input prompt is missing in the request'}), 400

    # Define system prompt
    system_prompt = (
        "You are a budget travel ticket advisor specializing in finding the most affordable transportation options for your clients. "
        "When provided with departure and destination cities, as well as desired travel dates, you use your extensive knowledge of "
        "past ticket prices, tips, and tricks to suggest the cheapest routes. Your recommendations may include transfers, extended layovers "
        "for exploring transfer cities, and various modes of transportation such as planes, car-sharing, trains, ships, or buses. "
        "Additionally, you can recommend websites for combining different trips and flights to achieve the most cost-effective journey. "
        "Mention the places/local food/local languages frequently used sentences, etc. Mention approx budget (INR) for each thing and total budget (INR) at the end."
    )

    chat = model.start_chat(response_validation=False)
    prompt = system_prompt + " " + input_prompt

    response = chat.send_message(prompt)
    response_text = response.candidates[0].content.parts[0].text

    # Format and return the response
    formatted_response = "### Suggested Travel Itinerary\n"
    formatted_response += "\n".join([f"{line.strip()}" for line in response_text.split("\n")])
    print(formatted_response)
    return json.dumps({'message': formatted_response}), 200


# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Define the Cloud Function to handle HTTP requests
# @functions_framework.http
# def get_travel_plan(request):
#     # """HTTP function to generate travel plan and store it in Firestore"""
    
#     # Parse the JSON body of the request
#     request_json = request.get_json(silent=True)
    
#     if request_json:
#         user_id = request_json.get('user_id')
#         prompt = request_json.get('prompt')
        
#         # Generate the travel plan using Vertex AI
#         model = TextGenerationModel.from_pretrained("gemini-2.0-flash-exp")
#         response = model.predict(prompt)
        
#         # Save response in Firestore
#         # doc_ref = db.collection('travel_plans').document(user_id)
#         # doc_ref.set({
#         #     'prompt': prompt,
#         #     'response': response.text,
#         #     'timestamp': firestore.SERVER_TIMESTAMP
#         # })
        
#         # Return the generated travel plan
#         return jsonify({
#             "response": response.text
#         }), 200
#     return jsonify({
#         "error": "Invalid request. Please provide 'user_id' and 'prompt'."
#     }), 400
