from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
import sqlite3


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

# Create an SQLite connection
con = sqlite3.connect("chinook.db")
tables_columns_sqlite = get_tables_and_columns_sqlite(con)

print('tables', tables_columns_sqlite)

template = """
-if the question is about a query: 
only show the SQLite query  for -> assume in {tables_columns_sqlite}, the tables are keys and values are their columns.

-if the question is not about a query: 
forget about query and without mentioning query concept, just relpy noramlly (eg greeting, answering a general knowledge question) and do not say anything about mt database and table.
"""

prompt = PromptTemplate(template=template, input_variables=["tables_columns_sqlite"])

llm = OpenAI(openai_api_key="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")

llm_chain = LLMChain(prompt=prompt, llm=llm)

# question = "What is the tallest mountain of world?"
# question = "When was the max of age where volume is between 10 to 20"

while True:
    question = input('Ask me: ')
    reply = llm_chain.run(question)

    try:

        cur = con.cursor()
        print(str(reply))
        cur.execute(str(reply))

        tables = cur.fetchall()


        # Print the names of the tables
        for table in tables:
            print(table)

        # Close the cursor and the connection
        cur.close()
        con.close()
    except Exception as e:
        print(reply)
        print(e)
