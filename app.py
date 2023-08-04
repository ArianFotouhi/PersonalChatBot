from config import openai_api

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

db = SQLDatabase.from_uri("sqlite:///chinook.db")
toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(openai_api_key=openai_api, temperature=0))

agent_executor = create_sql_agent(
    llm=OpenAI(openai_api_key=openai_api, temperature=0),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

agent_executor.run("Describe the employees table")