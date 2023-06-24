import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

import warnings
warnings.filterwarnings("ignore")

###

from langchain.agents.agent_toolkits import create_python_agent
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0)

tools = load_tools(["llm-math","wikipedia"], llm=llm)

agent= initialize_agent(
    tools, 
    llm, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = True)

# agent("What is the 25% of 300?")

# agent("how many episodes were made of the sitcom 'Friends'?")

"""
question = "Tom M. Mitchell is an American computer scientist \
and the Founders University Professor at Carnegie Mellon University (CMU)\
what book did he write?"
result = agent(question)
"""

#### Python Agent

agent = create_python_agent(
    llm,
    tool=PythonREPLTool(),
    verbose=True
)

customer_list = [["Harrison", "Chase"], 
                 ["Lang", "Chain"],
                 ["Dolly", "Too"],
                 ["Elle", "Elem"], 
                 ["Geoff","Fusion"], 
                 ["Trance","Former"],
                 ["Jen","Ayai"]
                ]

# agent.run(f"""Sort these customers by \
# last name and then first name \
# join the first name to the last name without a space and then
# print each resulting name in reverse and in lower case: {customer_list}""") 


# View detailed outputs of the chains

# import langchain
# langchain.debug=True
# agent.run(f"""Replace all occurrences of the letter 'e' with \
# the letter 'z' and then sort these customers by \
# last name and then first name \
# and print the output: {customer_list}""") 
# langchain.debug=False

# Define your own tool

from langchain.agents import tool
from datetime import date
from datetime import timedelta

@tool
def time(text: str) -> str:
    """Returns todays date, use this for any \
    questions related to knowing todays date. \
    The input should always be an empty string, \
    and this function will always return todays \
    date - any date mathmatics should occur \
    outside this function."""
    return str(date.today())

@tool
def nextweek_time(text: str) -> str:
    """Returns date one week from today, use this for any \
    questions related to knowing the date one week from today. \
    The input should always be an empty string, \
    and this function will always return the date one week \
    from today - any date mathmatics should occur \
    outside this function."""
    return str(date.today() + timedelta(days=7))


agent= initialize_agent(
    tools + [time, nextweek_time], 
    llm, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = True)

# Note:
# The agent will sometimes come to the wrong conclusion (agents are a work in progress!).
# If it does, please try running it again.

try:
    result = agent("whats the date seven days from now?") 
except: 
    print("exception on external access")