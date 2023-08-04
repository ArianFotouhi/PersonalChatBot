# ChatBot to reply based on personal SQL DB

To create a chatbot able to reply questions interpreted from retrieved info of database, there are two short solutions named app_auto.py and app_manual.py. In terms of project requirements, it is expected to distinguish the questions to figure out whether they are specific questions needed to be retrieved from db or general questions (greeting, general knowledge, etc.). In fact, the model should reply general inquiries casually (not SQL query) and db specific ones with result of SQL query.

The former one method (app_auto.py), is based on agent toolkit of langchain wherein the lower amount of effort is required from developing side; however, in terms of openai credit usage and latency this solution is not efficient. Plus, it did not show reliable performance in distinguishing general questions from query ones. 

On the other hand, the manual solution is showing more accuracy in results as well as higher speed (lower latency) and reduction in credit usage of API. Whereas, it needs more development and prompt engineering related practices to tailor its output.

NB: as of 4 Aug 2023,  app_auto.py code is not able to be run on Windows due to issue with Langchain library (from langchain.agents import create_sql_agent does not being imported), and the code can be run on Unix environment.
