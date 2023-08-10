from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import datetime

from langchain.llms import OpenAI

memory_length = 20

prompt = (
    PromptTemplate.from_template(
        """you are a customer service bot who is nice (please do not explain something that is not asked, keep replies short)
        previous conversation: {history}
        proceed the chat (eg do not say hello/hi/greeting when chat history in not empty) based on chat history, only reply to new question and based on chat history (not creation of chat)"""
        +
        """
        new human question is: {question}
         as to the customer resolution:

        -if customer wanted to extend service, ask them to email: extend@ieg.com (do not mention it if not asked)
        -if customer wanted to be refunded regarding service, ask them to email: refund@ieg.com (do not mention it if not asked)
        -if customer wanted to cancel service, ask them to email: cancel@ieg.com (do not mention it if not asked)

        also if the does not know reason of anything, sincerely it should say i am not aware of that but you can contact info@ieg.com to ask (do not mention it if not asked)
        for only information of customer bot, do not make up new email addresses
 
        """)
        + "\n\n , also the name of customer that you are talking is {name}"
        +"also reply in language {language}"
    
)

history = []
model = OpenAI(temperature=0, openai_api_key="")
chain = LLMChain(llm=model, prompt= prompt)

while True:

    question = input('Ask me: ')
    ans = chain.run(question = question, name= "Edward", history=history, language='Spanish')
    print(ans)
    print('history', history)
    history.insert(0, {'Human user': question, 'customer bot': ans, 'time':datetime.datetime.now()})

    if len(history)>memory_length:
        history = history[:memory_length]
