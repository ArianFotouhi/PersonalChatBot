import json
import openai
from datetime import datetime
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

import sqlite3
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


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


def db_query(user_prompt):

    prompt = (
        PromptTemplate.from_template(
            """
            your question is: {user_prompt}
            ONLY return the {sql_type} query without extra words show it like eg SELECT * FROM ...

            """)
        + 
        "\n\n , for query  assume i have my tables (key) and columns (their value) as {table_info}"
    )
   
    model = ChatOpenAI(temperature=0, openai_api_key= my_openai_key)
    chain = LLMChain(llm=model, prompt= prompt)

    ans = chain.run(user_prompt = user_prompt, sql_type= "SQLite", table_info=table_info)
#    print('sql in function', ans)
    try:

        con = sqlite3.connect("chinook.db")
        cur = con.cursor()
        cur.execute(ans)

        tables = cur.fetchall()

#        for table in tables:
#            print(table)

        # Close the cursor and the connection
        cur.close()
        con.close()
        return str(tables)
    except Exception as e:
        print('Sorry the search was unsuccessful, could you please try again with more specific information')
        print(e)
        return None


def get_tables_and_columns_sqlite(connection):
        tables_columns = {}

        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]
            tables_columns[table_name] = column_names

        return tables_columns


with sqlite3.connect("chinook.db") as con:
    table_info = get_tables_and_columns_sqlite(con)

function_descriptions_multiple = [
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
    },
    {
        "name": "db_query",
        "description": f"To make a SQL query and return the results in case of a question about search",
        "parameters": {
            "type": "object",
            "properties": {
                "user_prompt": {
                    "type": "string",
                    "description": "This is the question that user has asked and SQL results will be based on that, e.g. what is the last billing record from 2020",
                },
            },
            "required": ["user_prompt"],
        },
    },
    ]



llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0, openai_api_key= my_openai_key)
while True:

    user_prompt_ = input('ask me: ')
    first_response = llm.predict_messages(
        [HumanMessage(content=user_prompt_)], functions=function_descriptions_multiple
    )

    
    try:
        params = first_response.additional_kwargs["function_call"]["arguments"]
        params = params.strip()
        params = json.loads(params)

        chosen_function = eval(first_response.additional_kwargs["function_call"]["name"])
        func_output = chosen_function(**params)

        second_response = llm.predict_messages(
        [
            HumanMessage(content=user_prompt_),
            AIMessage(content=str(first_response.additional_kwargs)),
            AIMessage(
                role="function",
                additional_kwargs={
                    "name": first_response.additional_kwargs["function_call"]["name"]
                },
                content= func_output,
            ),
        ],
            functions=function_descriptions_multiple,
        )
        print(second_response.content)
    
    except:
        print(first_response.content)
