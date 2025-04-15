import requests
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv("API.env")

#GROQ_API_KEY = 'GROQ_API_KEY' # from https://console.groq.com/keys

# Google Custom Search API (REQUIRED)
GOOGLE_API_KEY = 'GOOGLE_API_KEY' # From https://console.cloud.google.com/apis/dashboard?inv=1&invt=Abs6FQ&project=liquid-folio-439508-i9
GOOGLE_CSE_ID = "GOOGLE_SEARCH_ID"  # from https://programmablesearchengine.google.com/controlpanel/all


# Function to search images using Google Custom Search
def search_images(query, max_results=3):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query + " infographic",  # Directly using topic + infographic
        "cx": GOOGLE_CSE_ID,
        "key": GOOGLE_API_KEY,
        "searchType": "image",
        "num": max_results
    }
    
    response = requests.get(search_url, params=params)
    data = response.json()
    
    image_urls = [item["link"] for item in data.get("items", [])]
    return "\n".join(image_urls) if image_urls else "No relevant images found."

# Initialize LangChain LLM
llm = ChatGroq(model="llama3-8b-8192", temperature=0)

# Prompt for educational explanation
prompt = PromptTemplate(
    input_variables=["topic"],
    template="""You are an AI tutor helping students learn about {topic}. 
    Provide a clear, structured explanation in 3-5 paragraphs. 
    Use bullet points for key takeaways and mention real-world applications."""
)

# Explanation Chain
explanation_chain = LLMChain(llm=llm, prompt=prompt)

# Function to generate both explanation and images
def generate_learning_material(topic):
    explanation = explanation_chain.run({"topic": topic})
    images = search_images(topic)  # Use the topic directly, not LLM output
    return f"**Explanation:**\n{explanation}\n\n**Infographics:**\n{images}"

# Run the final function
output = generate_learning_material("Deep Learning")
print(output)
