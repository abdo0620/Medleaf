from google import genai
import dotenv
import os 


os.load_dotenv()

client = genai.Client()
while True :
    print("How can i help you today?")
    query = input()