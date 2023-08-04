# ChatBot to reply based on personal SQL DB

In order to develop a chatbot capable of responding to user queries extracted from a database, two distinct approaches, named "app_auto.py" and "app_manual.py," have been devised. The primary objective of this project involves effectively categorizing incoming questions into either specific inquiries requiring database retrieval or general questions encompassing greetings and general knowledge topics. To achieve this, the model must seamlessly address general queries without resorting to SQL queries, while also responding to database-specific questions by generating SQL-based outputs.

The first approach, "app_auto.py," leverages the agent toolkit of Langchain. This method necessitates minimal effort from the development side. However, it exhibits certain limitations such as inefficient utilization of OpenAI credits and latency concerns. Furthermore, its performance in accurately distinguishing between general and query-based questions has proven to be unreliable.

Conversely, the manual approach demonstrates superior accuracy in its outcomes, coupled with quicker response times (lower latency) and reduced API credit consumption. Nevertheless, this alternative demands more extensive development efforts and the implementation of tailored prompt engineering practices to refine its outputs according to project requirements.

NB: as of August 4, 2023, it's worth noting that the "app_auto.py" code encounters compatibility issues when executed on Windows platforms. This complication arises from challenges related to the Langchain library, particularly the failure to import "create_sql_agent" from "langchain.agents." It is important to mention that the code is functional within a Unix environment.

