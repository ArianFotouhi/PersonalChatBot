from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
import sqlite3


llm = OpenAI(openai_api_key="",
    temperature=0)
# Here it is by default set to "AI"
# Now we can override it and set it to "AI Assistant"


template = """
The following is a friendly conversation between a human and an AI. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
Human: {input}
AI Assistant:

-if the question is about a query: ONLY return the SQLite query without extra words show it like eg SELECT * FROM ..., for -> assume i have a table named invoices and  columns are 
['InvoiceId', 'CustomerId', 'InvoiceDate', 'BillingAddress', 'BillingCity', 'BillingState', 'BillingCountry', 'BillingPostalCode', 'Total']

-if the question is not about a query: forget about query just relpy noramlly (eg greeting, answering a general knowledge question) and do not say anything about mt database and table

"""

PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
conversation = ConversationChain(
    prompt=PROMPT,
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
)
print('hi')

while True:
    question = input('Ask me: ')
    ans = conversation.predict(input=question)
    
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
