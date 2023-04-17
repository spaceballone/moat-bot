from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS
from colorama import Fore
import textwrap
from langchain.memory import ConversationBufferMemory


loader = PyPDFLoader("~/Downloads/merchant_prince.pdf")
pages = loader.load_and_split()

embeddings = OpenAIEmbeddings()

db = Chroma.from_documents(pages, embeddings)
retriever = db.as_retriever()

faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
retriever = faiss_index.as_retriever()

llm=OpenAI(temperature=0,max_tokens=512)

#memory = ConversationBufferMemory()

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

print(Fore.GREEN + "Hi! I'm AlanBot! A bot trained to answer questions from the 1536th dimension (of Alan and Naz's new book)!")

while True:
    query = input(Fore.GREEN + "Ask me anything:\n")
    result = qa({"query": query})
    print(Fore.BLUE + textwrap.fill(result["result"],width=150))
    print(Fore.CYAN + textwrap.fill(result["source_documents"], width=150))
