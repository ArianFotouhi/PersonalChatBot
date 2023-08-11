import json
import openai
from datetime import datetime
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

my_openai_key = ""
openai.api_key = my_openai_key


def get_flight_info(origin, destination):

    # Example output returned from an API or database
    flight_info = {
        "origin": origin,
        "destination": destination,
        "datetime": str(datetime.now()),
        "airline": "Qatar Airways",
        "flight": "Q491",
    }

    return json.dumps(flight_info)

function_descriptions = [
    {
        "name": "get_flight_info",
        "description": "Get flight information between two locations",
        "parameters": {
            "type": "object",
            "properties": {
                "origin": {
                    "type": "string",
                    "description": "The departure airport, e.g. DUS",
                },
                "destination": {
                    "type": "string",
                    "description": "The destination airport, e.g. HAM",
                },
            },
            "required": ["origin", "destination"],
        },
    }
]


llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0, openai_api_key= my_openai_key)

while True:

    user_prompt = input('ask me: ')
    first_response = llm.predict_messages(
        [HumanMessage(content=user_prompt)], functions=function_descriptions
    )

    
    try:
        params = first_response.additional_kwargs["function_call"]["arguments"]
        params = params.strip()
        params = json.loads(params)

        chosen_function = eval(first_response.additional_kwargs["function_call"]["name"])
        func_output = chosen_function(**params)

        second_response = llm.predict_messages(
        [
            HumanMessage(content=user_prompt),
            AIMessage(content=str(first_response.additional_kwargs)),
            AIMessage(
                role="function",
                additional_kwargs={
                    "name": first_response.additional_kwargs["function_call"]["name"]
                },
                content= func_output,
            ),
        ],
            functions=function_descriptions,
        )

        print(second_response.content)
    except:
        print(first_response.content)
