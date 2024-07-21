import os
from langchain.chat_models import ChatOpenAI

def init_llm(model_name="gpt-4o-mini",
             temperature=0.5,
             max_tokens=10000,
             model_kwargs={'frequency_penalty':0.7, 'presence_penalty':0.5, }):

    llm = ChatOpenAI(model_name=model_name,
                     temperature=temperature,
                     max_tokens=max_tokens,
                     model_kwargs=model_kwargs,
                     
                     openai_api_key=os.getenv('OPENAI_API_KEY'))

    return llm