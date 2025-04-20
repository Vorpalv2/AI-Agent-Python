import os

from dotenv import load_dotenv
from openai import OpenAI
import json
import requests

load_dotenv()

client = OpenAI()

def getWeatherUpdate(input:str):
    print(f"function called get weather update with input {input}")
    url = f"https://wttr.in/{input}?format=%c+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"the weather in city {input} is {response.text}"
    return "something went wrong"

def executeCommand(commandName : str):
    print(f"function execute Command called with the input {commandName}")
    result = os.system(command=commandName)
    return result


available_tools= {
    "getWeatherUpdate":{
        "fn": getWeatherUpdate,
        "description":"Takes a city name as an input and returns the current weather of that city"
    },
    "executeCommand":{
        "fn":executeCommand,
        "description":"Takes a command as an input and return the result and also to keep in mind that we are on a windows platform"
    }
}

system_prompt = """
design : you are a bot specialized in resolving the user query based on what input they've provided in

rules:
    -Output should always be in JSON object format.
    -carefully analyse the user query before proceeding.
    
output JSON object format:
  
  {{
        "step":"string",
        "content":"string",
        "function":"name of the function which was called during action step",
        "input":"what was the input value inside the function which was called during action step"
  }}

thought process : you work through a series of steps like start, plan, action, observe and output

available tools:
    -getWeatherUpdate - Takes a city name as an input and returns the current weather of that city.
    -executeCommand - Takes a command as an input and returns the result and also to keep in mind that we are on windows platform.

    example:
        user Input : What is the weather today in New York?
        Output : 
        {{"step":"start", "content": "user seems to be asking for today's weather of New York"}},
        {{"step":""plan", "content": "look into our avaliable tools and see if there's a tool which would let us check the current weather of a place"}},
        {{"step":"action": "function":"getWeatherUpdate", "input":"New York"}},
        {{"step":"observe": "output":"12 degree celsius"}},
        {{"step":"output": "content":"the weather of new york is 12 degree celsius"}}
     
     
     example:
        user Input : what is 2*2?
        Output:"this question does not relate to weather, therefore i am unable to answer this" 

"""

messages =[
    {"role":"system","content":system_prompt}
]

userInput = input("> ")
messages.append({"role":"user","content":userInput})
while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type":"json_object"},
        messages=messages
    )

    parsedOutput = json.loads(response.choices[0].message.content)
    messages.append({"role":"assistant","content":json.dumps(parsedOutput)})

    if parsedOutput.get("step") =="start":
            print(f"🧠:{parsedOutput.get("content")}")
            continue

    if parsedOutput.get("step") == "plan":
            print(f"🧠:{parsedOutput.get("content")}")
            continue

    elif parsedOutput.get("step") =="action":
        toolName = parsedOutput.get("function")
        toolInput = parsedOutput.get("input")

        if available_tools.get(toolName):
            tool_called = available_tools[toolName].get("fn")(toolInput)
            messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":tool_called})})
            continue

    if parsedOutput.get("step") == "output":
            print(f"🤖{parsedOutput.get("content")}")
            break


#
# gptResponse = client.chat.completions.create(
#     model="gpt-4o",
#     response_format={"type":"json_object"},
#     messages=[
#         {"role":"system","content":system_prompt},
#         {"role":"user","content":"what is the weather in Delhi?"},
#         {"role":"assistant","content":json.dumps({"step":"start","content": "user seems to be asking for the current weather of Delhi"})},
#         {"role":"assistant","content":json.dumps({"step": "plan", "content": "look into our available tools and see if there's a tool which would let us check the current weather of a place"})},
#         {"role":"assistant","content":json.dumps({"step": "action", "function": "getWeatherUpdate", "input": "Delhi"})},
#         {"role":"assistant","content":json.dumps({"step": "observe", "output": "32 degree celsius"})},
#     ]
# )

