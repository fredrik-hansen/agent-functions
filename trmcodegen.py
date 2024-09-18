"""
An easy way to execute code generation, and optionally also execution
directly from the commandline.

I use the below for a convenient and quick access to generate functions, references and whatnot.
Add to your .bashrc file:
alias ½='python ~/code/trmcodegen.py'

Usage: ½ generate an empty html page
Usage: ½ create python code for a terminal calculator, comment the code, write all error handling and input validation
Usage: ½ generate prompt for an expert french cook that loves to inspire child-friendly dinners for the whole family

pip install pyautogen

"""

from autogen import AssistantAgent, UserProxyAgent
from sys import argv

prompt_price_per_1k = 0
completion_token_price_per_1k = 0

config_list = [{
    "model": "llama3.1:70b",
    "base_url": "http://ollama.dc.int:11434/v1",
    "api_key": "ollama",
    "price": [prompt_price_per_1k, completion_token_price_per_1k],
    "frequency_penalty": 0.5,
    "max_tokens": 2048,
    "presence_penalty": 0.2,
    "temperature": 0.2,
    "top_p": 0.2,
  }]

assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False})
user_proxy.initiate_chat(assistant, message=' '.join(argv[1:]))
