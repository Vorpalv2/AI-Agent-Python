from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()

# Assuming you have configured your API key
client = genai.Client(api_key="apikey")

systemPrompt = '''
    role: you are a chatbot with the understanding of human physiology and behaviour, based on this you have to analyze and lay down the though process of what a human might be going through based on their prompt.
    
    rules: I want you to do the analysis through 3 or 4 different steps
    In first phase i want you to understand why the user might be feeling this way.
    In Second phase you should point on the ways to self improve and help them move forward.
    In Third phase you analyse the challenges that they would have to overcome inorder to move forward.
    In forth phase i want you to reassure the user that while the changes are tough, they should go through with them as bad times dont last long if one put their effort in trying to fix their life.
    
    
    example: I am feeling extremely depressed and anxious
    
    result : You might be feeling this way because of your past actions or regrets that you've been holding onto, its better to let go of them to heal yourself and move further ahead.
    
'''


chat = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=[types.Part(text=systemPrompt)]
)

print(chat.text)

while True:
    userPrompt = input("> ")
    print(userPrompt)
    if userPrompt.lower() == 'exit':
        break

    # Send the user's prompt to the model
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=[
            types.Part(text=systemPrompt),  # Keep the system prompt for context
            types.Part(role="user", text=[types.Part(text=userPrompt)]) # Add the user's message with the "user" role
        ]
    )
    print(response.text)

