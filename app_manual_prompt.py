from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import sqlite3

prompt = (
    PromptTemplate.from_template(
        """
        your question is: {question}
        -if the question is about a query: ONLY return the {sql} query without extra words show it like eg SELECT * FROM ...

        -if the question is not about a query: forget about query just relpy noramlly (eg greeting, answering a general knowledge question) and do not say anything about mt database and table)
        """)
    + "\n\n , for query  assume i have a table named invoices and  columns are {columns}"
)



columns = ['InvoiceId', 'CustomerId', 'InvoiceDate', 'BillingAddress', 'BillingCity', 'BillingState', 'BillingCountry', 'BillingPostalCode', 'Total']
model = ChatOpenAI(openai_api_key="")
chain = LLMChain(llm=model, prompt=prompt)




while True:
    question = input('Ask me: ')
    ans = chain.run(question = question,sql="SQLite", columns=columns)
    print(ans)
    
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
        print(ans)
        print(e)
