from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import sqlite3

memory_length = 4

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

# Create a temp SQLite connection
with sqlite3.connect("chinook.db") as con:
    table_info = get_tables_and_columns_sqlite(con)

prompt = (
    PromptTemplate.from_template(
        """
        your question is: {question}
        -if the question is about a query: ONLY return the {sql_type} query without extra words show it like eg SELECT * FROM ...

        -if the question is not about a query: forget about query just relpy noramlly (eg greeting, answering a general knowledge question) and do not say anything about mt database and table)
        """)
    + "\n\n , for query  assume i have my tables (key) and columns (their value) as {table_info}"
    + "also this your chat history: {history}"
)


history = []
model = ChatOpenAI(openai_api_key="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")
chain = LLMChain(llm=model, prompt=prompt)


while True:
    
    question = input('Ask me: ')
    ans = chain.run(question = question,sql_type="SQLite", table_info=table_info, history=history)
    print(ans)
    print('history', history)
    history.insert(0, {'Human': question, 'AI model': ans})
    
    if len(history)>memory_length:
        history = history[-1*memory_length:]
    try:

        con = sqlite3.connect("chinook.db")
        cur = con.cursor()
        cur.execute(ans)

        tables = cur.fetchall()


        # Print the names of the tables
        for table in tables:
            print(table)

        # Close the cursor and the connection
        cur.close()
        con.close()
    except Exception as e:
        print(e)
