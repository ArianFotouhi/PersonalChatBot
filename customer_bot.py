from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import datetime
memory_length = 4

prompt = (
    PromptTemplate.from_template(
        """you are a helpful customer service bot
        previous conversation: {history}
        proceed the chat based on chat history, only reply to new question and no full reply of whole chat (not creation of chat)"""
        +
        """
        new human question is: {question}
         as to the customer resolution:
        -if customer wanted to cancel membership, ask them to email: cancel@ieg.com
        -if customer wanted to extend membership, ask them to email: extend@ieg.com
        -if customer wanted to be refunded regarding membership, ask them to email: refund@ieg.com
        and before ending the chat make sure is there anything else we can help with
        if there was no new task, just say goodbye and wish a nice day
        """)
        + "\n\n , also the name of customer that you are talking is {name}"
        +"also reply in language {language}"
    
)

history = []
model = ChatOpenAI(openai_api_key="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")
chain = LLMChain(llm=model, prompt= prompt)

while True:

    question = input('Ask me: ')
    ans = chain.run(question = question, name= "Edward", history=history, language='English')
    print(ans)
    print('history', history)
    history.insert(0, {'Human user': question, 'customer bot': ans, 'time':datetime.datetime.now()})

    if len(history)>memory_length:
        history = history[-1*memory_length:]
