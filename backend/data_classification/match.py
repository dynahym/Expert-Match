import os
import json
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
application = get_wsgi_application()
from database.models import Expert
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API key must be set in the environment variable API_KEY.")

genai.configure(api_key=api_key)

def propose_experts_using_ai(thesis_title: str, num_experts: int = 3) -> list[dict]:
    """
    Use the generative AI model to propose experts based on their keywords (mot_cles).
    
    Args:
        thesis_title (str): The title of the thesis for which experts are being proposed.
        num_experts (int): The number of experts to propose (default is 3).

    Returns:
        list[dict]: A list of dictionaries, each containing 'name', 'keywords', and 'explanation' of an expert.
    """
    # Fetch all experts with their keywords
    experts = Expert.objects.all()

    # Prepare prompt asking for the response as a list of dictionaries
    expert_entries = []
    for expert in experts:
        keywords = ', '.join([keyword.mot_cle for keyword in expert.mots_cles.all()])
        expert_entries.append(f"Expert: {expert.nom} {expert.prenom}, Keywords: {keywords}")

    prompt = (
        f"Given the thesis title: '{thesis_title}', propose {num_experts} experts from the list below. "
        "Return the response as a JSON array of dictionaries where each dictionary contains 'name', 'keywords', and 'explanation':\n\n"
        + "\n".join(expert_entries)
    )

    # Use the model to generate a structured response
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Clean the response
    cleaned_response = response.text.strip("`")[5:]

    # Ensure response is a valid JSON string
    try:
        # Parse the cleaned response as JSON
        return json.loads(cleaned_response)
    except json.JSONDecodeError:
        raise ValueError("The response from the AI model is not valid JSON.")

# Example usage
# thesis_title = "Advanced Machine Learning for Natural Language Processing"
# recommended_experts = propose_experts_using_ai(thesis_title, num_experts=3)

# # Print the experts in a structured way
# for expert in recommended_experts:
#     print(f"Name: {expert['name']}")
#     print(f"Keywords: {expert['keywords']}")
#     print(f"Explanation: {expert['explanation']}\n")
