from google import genai

client = genai.Client(api_key="AIzaSyD8XOsUxGkWdLQvWRL6gauE_VWZguHtbLU")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello"
)

print(response.text) 