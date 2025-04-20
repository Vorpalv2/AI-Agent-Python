from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

def getHelpfulLink(input:str):
    return "severe mental issue detected"

systemPrompt = '''
    role: you are a chatbot with the understanding of human physiology and behaviour, based on this you have to analyze and lay down the though process of what a human might be going through based on their prompt and any other queries unrelated to mental health should not be answered by you.
    you work in the sequence of start,plan,action and output.
    from the given user query and available tools, plan the step by step execution based on your work sequence.
    select the appropriate tool from the available tools and call the selected tool based on the requirement of the query if its needed.
    
     
    rules: 
    - Do the analysis through 4 different steps,
    - Follow the Output JSON Format
    - Carefully analyse the user query.
    - Always perform one step at a time and wait for the next input.
    
    Output JSON Format:
    {{
        "step":"string",
        "content":"string",
        "function" : "the name of the function if the step is action",
        "input" : "the value of the input parameter of the function"
    }}
    
    example: I am feeling extremely depressed and anxious
    
    Output : {{"step" : "plan", "content" : "Understand why the user might be feeling this way."}}
    {{"step": "plan", "content" : "Point on the ways to self improve and help them move forward and analyse the challenges that they would have to overcome inorder to move forward."}}
    {{"step": "action", "function": "getHelpfulLink", "input : "depression and male lonliness"}}
    {{"step" : "output", "content": "Motivate the user that they can do this."
    
    example: what is 2*2?
    Output: this question is not related to mental health or human physiology or behaviour therefore i am unable to answer this.
'''
#
# while True:
#
#     chat = client.chat.completions.create(
#         model="chatgpt-4o-latest",
#         messages=[
#             {"role":"system","content":systemPrompt},
#             {"role":"user","content":""},
#             {"role":"assistant","content":"this is where you would be greeting the user by their name"}
#         ]
#     )
#
#     userPrompt = input(">")
#
# print(chat.choices[0].message)
#

response = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type":"json_object"},
    messages=[
        {"role":"system","content":systemPrompt},
        {"role":"user","content":"what to do if you are feeling that nothing is going right in your life?"},
        {"role":"assistant","content":json.dumps({"step": "start", "content": "Identify the underlying feelings and reasons for feeling that way."})},
        {"role":"assistant","content":json.dumps({"step": "plan", "content": "Understand why the user might be feeling this way."})},
        {"role":"assistant","content":json.dumps({"step": "plan", "content": "Explore strategies to manage these feelings and regain a sense of control."})},
        {"role":"assistant","content":json.dumps({"step": "action", "function": "getHelpfulLink", "input": "overcoming feelings of hopelessness and lack of control"})},
        {"role":"assistant","content":json.dumps({"step": "output", "content": "Encourage the user by acknowledging that it's normal to feel this way sometimes, and remind them that they have the ability to make positive changes step by step."}
)},


    ]
)

print(response.choices[0].message.content)

