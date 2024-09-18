"""
Used to get quick oneliners from Ollama from the terminal

Add this to .bashrc:
alias §='python ~/code/myllama.py'

pip install asyncio colorama ollama
(colorama is optional, it's just for the fancy colors)

"""
import asyncio
import colorama
from ollama import AsyncClient
from sys import argv


async def chat():
    input = ' '.join(argv[1:])
    message = {'role': 'user', 'content': input}
    print(colorama.Fore.GREEN)
    async for part in await AsyncClient(host='http://ollama.dc.int:11434').chat(model='llama3.1:70b', messages=[message], stream=True):
        print(part['message']['content'], end='', flush=True)
asyncio.run(chat())
print(colorama.Style.RESET_ALL)
