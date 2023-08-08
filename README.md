# ChatBot to reply based on personal SQL DB

In order to develop a chatbot capable of responding to user queries extracted from a database, two distinct approaches, named "app_auto.py" and "app_manual.py," have been devised. The primary objective of this project involves effectively categorizing incoming questions into either specific inquiries requiring database retrieval or general questions encompassing greetings and general knowledge topics. To achieve this, the model must seamlessly address general queries without resorting to SQL queries, while also responding to database-specific questions by generating SQL-based outputs.

The first approach, "app_auto.py," leverages the agent toolkit of Langchain. This method necessitates minimal effort from the development side. However, it exhibits certain limitations such as inefficient utilization of OpenAI credits and latency concerns. Furthermore, its performance in accurately distinguishing between general and query-based questions has proven to be unreliable.

Conversely, the manual approach demonstrates superior accuracy in its outcomes, coupled with quicker response times (lower latency) and reduced API credit consumption (based on below tests, 5 to 8 times less credit usuage). Nevertheless, this alternative demands more extensive development efforts and the implementation of tailored prompt engineering practices to refine its outputs according to project requirements. Despite its various advantages, this method is particularly recommended in scenarios where the database contains a relatively modest number of tables and columns. This recommendation stems from the fact that this approach necessitates the provision of descriptions for each of these elements. It's important to note that an inadequate or inefficient description has the potential to confuse the model. This stands in contrast to the automated process employed by "app_auto.py," which handles this aspect automatically.

NB: as of August 4, 2023, it's worth noting that the "app_auto.py" code encounters compatibility issues when executed on Windows platforms. This complication arises from challenges related to the Langchain library, particularly the failure to import "create_sql_agent" from "langchain.agents." It is important to mention that the code is functional within a Unix environment.

Here are some test results of two approaches:

app_auto.py
Answer - Correct!
```
Prompt: Describe the the oldest invoice in Canada in invoices table
```

```
Thought: I should query the oldest invoice date in Canada
Action: sql_db_query
Action Input: SELECT MIN(InvoiceDate) FROM invoices WHERE BillingCountry = 'Canada'
Observation: [('2009-01-06 00:00:00',)]
```

```
Final Answer: The oldest invoice date in Canada is 2009-01-06 00:00:00.
```

app_auto.py
Answer - False!
```
Prompt: Hey how you doing?
```

```
Thought:  I should query the albums table for the title of the album with AlbumId = 3
Action: sql_db_query
Action Input: SELECT Title FROM albums WHERE AlbumId = 3
Observation: [('Restless and Wild',)]

```

```
Final Answer: The title of the album with AlbumId = 3 is Restless and Wild.
```



app_manual.py
Answer - Correct!

Note: in this test, only one table of database and its corresponding columns are described to the model. Therefore, it is not able to reply the questions regarding whole tables.
```
Prompt: Give me the highest Total rate of 2012 
```

```
Answer: 23.86
```

app_manual.py
Answer - Correct!
```
Prompt: Hi 
```

```
Answer: Hi there! How can I help you?
```

<hr>

The upgraded version of "app_manual.py" is now known as "app_manual_memory.py," introducing a significant change in how it operates. In this new version, the model's responses are noticeably impacted by the chat history. To illustrate this point:
