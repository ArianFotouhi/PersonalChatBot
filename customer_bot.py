from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

memory_length = 4

prompt = (
    PromptTemplate.from_template(
        "be a helpful and polite customer service bot and resume the chat history, only reply to current question (not creation of chat) this your chat history: {history}"
        +
        """
        current question is: {question}
         as to the customer resolution:
        -if customer wanted to cancel membership, ask them to email: cancel@ieg.com
        -if customer wanted to extend membership, ask them to email: extend@ieg.com
        -if customer wanted to be refunded regarding membership, ask them to email: refund@ieg.com
        and before ending the chat make sure is there anything else we can help with (except when you goodbye)
        """)
    + "\n\n , also the name of customer that you are talking is {name}"
    +"also reply in language {language}"
    
)

history = []
model = ChatOpenAI(openai_api_key="")
chain = LLMChain(llm=model, prompt= prompt)

while True:

    question = input('Ask me: ')
    ans = chain.run(question = question, name= "Edward", history=history, language='French')
    print(ans)
    print('history', history)
    history.insert(0, {'Human user': question, 'AI model': ans})

    if len(history)>memory_length:
        history = history[-1*memory_length:]
