Travel Guru: Travel Planning Assistant with Vertex AI and Google Cloud Functions
================================================================================



Introduction
============

Planning a trip can be overwhelming, but it doesn’t have to be. With the power of AI , you can now generate a personalized, budget-friendly travel itinerary using a simple chat interface. In this article, we’ll walk through how to build a **smart travel assistant** that not only suggests destinations, accommodations, and local experiences but also incorporates **budget constraints**, **travel preferences**, and **real-time information** to create the perfect trip plan for you.

We’ll be using **Vertex AI**, **Google Cloud Functions**, and **Firestore** to achieve this, ensuring everything runs smoothly on Google Cloud.

Overview of the Project
=======================

Our goal is to create an **AI-powered travel planner** that:

*   Takes input from the user about their travel preferences (e.g., budget, destination, duration, travel style).
*   Generates a personalised travel itinerary, including **places to visit**, **local food**, **activities**, and **budget estimations**.
*   Provides recommendations for apps and tips to save costs on the trip.
*   Uses **Google Cloud Functions** to deploy the solution as a scalable, serverless API.

We will also make use of **Firestore** to store the generated travel plans and easily retrieve them for later use.

Step 1: Setting Up Google Cloud
===============================

Google Cloud Project & Enable APIs
----------------------------------

1.  Create a new project on Google Cloud Console.
2.  Enable the **Vertex AI**, **Cloud Functions**, and **Firestore** APIs in your project.
3.  Set up billing for the project, as these services require an active billing account.

Set Up Google Cloud SDK
-----------------------

*   Install the **Google Cloud SDK**: Install the gcloud SDK.
*   Authenticate using your Google account:

```
gcloud auth log
```

Initialize Firebase & Firestore
-------------------------------

1.  Set up Firebase in your project by navigating to the **Firebase Console** and connecting it with your Google Cloud project.
2.  Initialize Firebase Admin SDK in your Cloud Functions:

```
import firebase_admin from firebase_admin import credentials, firestore firebase_admin.initialize_app(credentials.Certificate('path_to_your_service_account_key.json')) db = firestore.client()
```

Step 2: Leveraging Vertex AI for Travel Plan Generation
=======================================================

Vertex AI’s **Generative Models** provide an excellent foundation for creating dynamic, customized content. For our travel assistant, we’ll use **Gemini Flash** — a language model specialized in text generation tasks like creating itineraries and offering travel recommendations.

Setting Up Vertex AI
--------------------

To begin using Vertex AI, you need to initialize it with your Google Cloud project and region:py

```
import vertexai
from vertexai.language_models import TextGenerationModel
# Vertex AI initialization
vertexai.init(project="your-project-id", location="asia-south1")
model = GenerativeModel(
    "gemini-1.5-flash-001",
    generation_config=GenerationConfig(temperature=0),
)
```

Travel Plan Generation Logic
----------------------------

The core of our assistant is its ability to take user inputs and generate a detailed travel plan. The model takes in a prompt, which includes:

*   **Destination**: Where the user wants to go.
*   **Travel Type**: Solo, family, group, etc.
*   **Budget**: How much the user is willing to spend.
*   **Duration**: How long they want to stay.
*   **Weather preferences**: If they want a specific climate, like snow.

Here’s a function to get the plan:

```
def get_travel_plan(input_prompt):
    system_prompt = "You are a budget travel advisor that suggests the most affordable yet fun travel plans..."
    prompt = system_prompt + " " + input_prompt
    
    response = model.generate_text(prompt)
    return response.text
```

This function will return a text-based itinerary with details about:

*   **Day-wise itinerary**.
*   **Suggested local food**.
*   **Must-try activities**.
*   **Budget estimations**.

Step 3: Deploying as Cloud Functions
====================================

With **Google Cloud Functions**, you can deploy the travel planner as a **serverless API**. This allows you to trigger the function via HTTP requests without worrying about managing infrastructure.

Writing the Cloud Function
--------------------------

Here’s how the cloud function can be structured:

```
import functions_framework
import json
from vertexai import TextGenerationModel
from firebase_admin import firestore
# Initialize model and Firestore
model = TextGenerationModel.from_pretrained("gemini-2.0-flash-exp")
db = firestore.client()
@functions_framework.http
def get_travel_plan(request):
    # Get input from the request
    request_json = request.get_json(silent=True)
    input_prompt = request_json.get('input_prompt', '')
    
    # Generate travel plan
    travel_plan = generate_travel_plan(input_prompt)
    
    # Save plan to Firestore
    user_id = request_json.get('user_id', 'default_user')
    db.collection('travel_plans').add({
        'user_id': user_id,
        'input_prompt': input_prompt,
        'travel_plan': travel_plan
    })
    
    # Return the generated plan
    return json.dumps({'travel_plan': travel_plan}), 200
```

Deploying the Function
----------------------

To deploy the function, use the following command:

```
gcloud functions deploy get_travel_plan \
  --runtime python310 \
  --trigger-http \
  --allow-unauthenticated
```

Step 4: Adding sample images of places/food
===========================================

```
import math
import matplotlib.pyplot as plt
# An auxiliary function to display images in grid
def display_images_in_grid(images):
    """Displays the provided images in a grid format. 4 images per row.
    Args:
        images: A list of PIL Image objects representing the images to display.
    """
    # Determine the number of rows and columns for the grid layout.
    nrows = math.ceil(len(images) / 4)  # Display at most 4 images per row
    ncols = min(len(images) + 1, 4)  # Adjust columns based on the number of images
    # Create a figure and axes for the grid layout.
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(12, 6))
    for i, ax in enumerate(axes.flat):
        if i < len(images):
            # Display the image in the current axis.
            ax.imshow(images[i]._pil_image)
            # Adjust the axis aspect ratio to maintain image proportions.
            ax.set_aspect("equal")
            # Disable axis ticks for a cleaner appearance.
            ax.set_xticks([])
            ax.set_yticks([])
        else:
            # Hide empty subplots to avoid displaying blank axes.
            ax.axis("off")
    # Adjust the layout to minimize whitespace between subplots.
    plt.tight_layout()
    # Display the figure with the arranged images.
    plt.show()
// Generating images
from vertexai.preview.vision_models import ImageGenerationModel
image_generation_model = ImageGenerationModel.from_pretrained("imagen-3.0-fast-generate-001")
```

Step 5: Integration with Front-End (Optional)
=============================================

While we are focused on the back-end logic, you can integrate this API into a **web application** or a **Colab notebook** using simple **HTTP requests**.

Example of making a call from a Colab notebook:

```
import requests
import json
# Cloud Function URL
url = "https://asia-south1-bnb-blr-444504.cloudfunctions.net/get_travel_plan"
# The prompt you want to send to the cloud function
input_prompt = "Plan a solo trip to Delhi and around for 5 days with a budget of INR 200000."
# Data to be sent in the request
def generate_trip_plan_api(prompt):
    data = {
      "prompt": prompt,
      "user_id": "vamshi"
    }
    # Send the POST request to the Cloud Function
    response = requests.post(url, json=data)
    # Check the response status and print the result
    if response.status_code == 200:
        # If the request was successful, print the result (formatted response from the function)
        # print("Travel Plan Generated:")
        # print(response.json().get("message"))
        return response.json().get("message")
        store_travel_plan(user_id, prompt, plan)
    else:
        # If there's an error, print the error message
        # print(f"Error: {response.status_code}")
        # print(response.json().get("error"))
        return response.json().get("error")
def plan_trip(prompt):
  plan = generate_trip_plan_api(prompt)
  display(Markdown(plan))
  show_images(plan, True, 3)
```

User interface to take input and show output

```
import ipywidgets as widgets
from IPython.display import display, clear_output
# Define widgets
use_custom_query = widgets.Checkbox(
    value=False,
    description="Use Custom Query",
    style={'description_width': 'initial'}
)
custom_query = widgets.Text(
    value="Plan a luxury family trip to Paris for 7 days with a budget of 2,00,000 INR.",
    description="Custom Query:",
    style={'description_width': 'initial'}
)
start = widgets.Text(
    value="Bengaluru",
    description="Start Location:",
    style={'description_width': 'initial'}
)
destination = widgets.Text(
    value="Vietnam",
    description="Destination:",
    style={'description_width': 'initial'}
)
trip_type = widgets.Dropdown(
    options=["solo", "family", "friends", "couple"],
    value="solo",
    description="Trip Type:",
    style={'description_width': 'initial'}
)
budget = widgets.Text(
    value="100000 INR",
    description="Budget:",
    style={'description_width': 'initial'}
)
duration = widgets.Text(
    value="10 days",
    description="Duration:",
    style={'description_width': 'initial'}
)
budget_level = widgets.Dropdown(
    options=["low budget", "mid-range", "luxury"],
    value="low budget",
    description="Budget Level:",
    style={'description_width': 'initial'}
)
weather = widgets.Text(
    value="normal",
    description="Preferred Weather:",
    style={'description_width': 'initial'}
)
# Container to hold dynamic content
output = widgets.Output()
# Function to update UI based on checkbox
def update_ui(change):
    with output:
        clear_output()  # Clear previous outputs
        if use_custom_query.value:
            display(custom_query)
        else:
            display(start, destination, trip_type, budget, duration, budget_level, weather)
# Attach the observer
use_custom_query.observe(update_ui, names='value')
# Initial display
display(use_custom_query)
with output:
    display(start, destination, trip_type, budget, duration, budget_level, weather)
display(output)
# Button to generate the query
generate_button = widgets.Button(description="Generate Travel Plan")
# Function to generate the query
def generate_query(_):
    if use_custom_query.value:
        query = custom_query.value
    else:
        query = (
            f"Plan a {trip_type.value} trip from {start.value} to {destination.value} for {duration.value}. "
            f"The budget is {budget.value}, focusing on a {budget_level.value} experience. "
            f"Prioritize destinations with {weather.value} weather"
        )
    with output:
        clear_output()
        print("Trip Query:")
        print(query)
        print("\n")
        print("Packing your virtual suitcase with epic adventures and local delicacies...")
        plan_trip(query)
generate_button.on_click(generate_query)
# Display the generate button
display(generate_button)
```

![captionless image](https://miro.medium.com/v2/resize:fit:1000/format:webp/1*Ofxkbq9VWFWcvfoP5e6PKQ.png)![captionless image](https://miro.medium.com/v2/resize:fit:1000/format:webp/1*p-1wG3wVIVYhCD-PNkQb6A.png)

![captionless image](https://miro.medium.com/v2/format:webp/1*SsWjDRPOKvu0RTpJdtJj2g.png)

Step 5: Adding More Features (Optional)
=======================================

To further enhance the assistant, you can add:

*   **Multi-language support**: Let users plan trips in their preferred language.
*   Integrating with flight booking APIs, hotel booking, places reviews and tour operators.

Conclusion
==========

Building a smart travel assistant with **Google Cloud Functions** and **Vertex AI** makes it easier to generate personalized travel plans with minimal effort. By combining **AI-based text generation** and **serverless computing**, you can provide users with a highly dynamic and cost-effective way to plan their next adventure.

Deploying such solutions on **Google Cloud** ensures scalability and reliability while keeping the system maintenance-free, all while delighting your users with AI-driven insights.

**Call to Action**:

*   Give this travel assistant a try!
*   Add more features like flight booking or transportation integration to make it even more powerful!
