# from langchain.agents import AgentExecutor, create_agent
# from mistralai.client import ChatMistralAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from tools import web_search, scrape_url
# from dotenv import load_dotenv
# import os

# load_dotenv()

# llm=mistral_client=ChatMistralAI(
#     api_key=os.environ["MISTRAL_API_KEY"],temperature=0)

# def build_search_agent():
#   return create_agent(
#     llm=llm,
#     tools=[web_search]
#   )

# def build_reader_agent():
#   return create_agent(
#     llm=llm,
#     tools=[scrape_url]
#   )

# #writer chain lcel pipeline
# writer_prompt=ChatPromptTemplate.from_messages([
#   ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
#     ("human", """Write a detailed research report on the topic below.

# Topic: {topic}

# Research Gathered:
# {research}

# Structure the report as:
# - Introduction
# - Key Findings (minimum 3 well-explained points)
# - Conclusion
# - Sources (list all URLs found in the research)

# Be detailed, factual and professional."""),
# ])

# writer_chain = writer_prompt | llm | StrOutputParser()

# #critic prompt
# critic_prompt = ChatPromptTemplate.from_messages([
#      ("system", "You are a sharp and constructive research critic. Be honest and specific."),
#     ("human", """Review the research report below and evaluate it strictly.

# Report:
# {report}

# Respond in this exact format:

# Score: X/10

# Strengths:
# - ...
# - ...

# Areas to Improve:
# - ...
# - ...

# One line verdict:
# ..."""),
# ])

# critic_chain = critic_prompt | llm | StrOutputParser()




# agents.py
from langgraph.prebuilt import create_react_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatMistralAI(
    model="mistral-small-latest",
    api_key=os.environ["MISTRAL_API_KEY"],
    temperature=0,
)

def build_search_agent():
    return create_react_agent(
        model=llm,
        tools=[web_search],
    )

def build_reader_agent():
    return create_react_agent(
        model=llm,
        tools=[scrape_url],
    )

# writer chain - LCEL pipeline
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# critic chain - LCEL pipeline
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()


