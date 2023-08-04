from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
import sqlite3

template = """
-if the question is about a query: only show the SQLite query (eg SELECT * FROM ...) for -> assume i have a table named invoices and  columns are 
['InvoiceId', 'CustomerId', 'InvoiceDate', 'BillingAddress', 'BillingCity', 'BillingState', 'BillingCountry', 'BillingPostalCode', 'Total']

-if the question is not about a query: forget about query just relpy noramlly (eg greeting, answering a general knowledge question) and do not say anything about mt database and table

Question: {question}
"""

prompt = PromptTemplate(template=template, input_variables=["question"])

llm = OpenAI(openai_api_key="")

llm_chain = LLMChain(prompt=prompt, llm=llm)


# question = "What is the tallest mountain of world?"
# question = "When was the max of age where volume is between 10 to 20"

while True:
    question = input('Ask me: ')
    reply = llm_chain.run(question)
    
    try: 

        con = sqlite3.connect("chinook.db")
        cur = con.cursor()
        cur.execute(reply)

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