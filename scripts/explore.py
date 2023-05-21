
from constants import keys
from langchain.llms import OpenAI
from langchain.chains import APIChain
from langchain.prompts.prompt import PromptTemplate

import os
# set API KEYS here
os.environ['openai_api_key'] = keys['openai']

## Calling openAI LLM via API
"""
llm = OpenAI(model_name="text-ada-001", n=2, best_of=2)
print(llm("tell me a joke"))
"""
## Calling a weather API
"""
from langchain.chains.api import open_meteo_docs #Weather API

llm = OpenAI(temperature=0)
chain_new = APIChain.from_llm_and_api_docs(llm, open_meteo_docs.OPEN_METEO_DOCS, verbose=True)
chain_new.run('What is the weather like right now in Singapore in degrees Celsius?')
"""

## store document in transient vector database. Search through it using LLM to query
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain

from langchain.document_loaders import TextLoader
loader = TextLoader("./data/THESIS TO PRINT_FINAL_txt.txt")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), vectorstore.as_retriever(), memory=memory)

query = "Summarise this document for me"
result = qa({"question": query})
print(result)

query = "What are the behavioural studies conducted in this thesis?"
result = qa({"question": query})
print(result)