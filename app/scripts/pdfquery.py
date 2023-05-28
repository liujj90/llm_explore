# setup envrionment
import sys
from typing import Any
sys.path.insert(0, '..')
import os
from scripts.constants import keys

# llm
from langchain import OpenAI

# langchain pdf loader and vectorstore
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
# OpenAI embeddings
from langchain.embeddings.openai import OpenAIEmbeddings

# we can use a retreival question and answer api to query the document
from langchain.chains import RetrievalQA
# set API KEYS here
os.environ['openai_api_key'] = keys['openai']

# constants
OPENAI_MODEL =  "gpt-3.5-turbo" # "text-ada-001" #  
# initialize openai model 
llm = OpenAI(model_name=OPENAI_MODEL)  

class QApipeline():

    def __init__(self, filename, persist = True):
        self.llm = OpenAI(model_name=OPENAI_MODEL)  
        self.filename = filename
        self.embeddings = OpenAIEmbeddings()
        self.pages = None
        self.index = None
        self.qa = None
        self.persist = persist
        dbpath = filename.split('\\')[-1]
        self.db_path = f'db/{dbpath}/'
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
            # should extend this to load db if exists
        
        
    def load_documents(self):
        loader = PyPDFLoader(self.filename)
        splitter = CharacterTextSplitter(chunk_size = 500, chunk_overlap = 100)
        self.pages = loader.load_and_split(text_splitter = splitter)
        
    def get_index(self):
        self.index = Chroma.from_documents(self.pages, self.embeddings, persist_directory=self.db_path)
        if self.persist:
            self.index.persist() 
        
    def get_qa_pipeline(self):
        self.qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=self.index.as_retriever(), verbose = True)

    def run(self, query):
        if self.qa is None:
            self.load_documents()
            self.get_index()
            self.get_qa_pipeline()
        result = self.qa.run(query)
        print(result)
        return result
