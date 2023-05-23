from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS
from colorama import Fore
import textwrap

index_dir = "./index"
embeddings = OpenAIEmbeddings()

try:
    faiss_index = FAISS.load_local(folder_path=index_dir, embeddings=embeddings)
except Exception as e:
    print(Fore.RED + "Couldn't load index from disk. Recreating")
    loader = PyPDFLoader("~/Downloads/merchant_prince.pdf")
    pages = loader.load_and_split()
    faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
    faiss_index.save_local(folder_path=index_dir)

#db = Chroma.from_documents(pages, embeddings)
#retriever = db.as_retriever()


retriever = faiss_index.as_retriever()

llm=OpenAI(temperature=0,max_tokens=512)

#memory = ConversationBufferMemory()

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

print(Fore.GREEN + "Hi! I'm MOAT Bot! A bot trained to answer questions from the 1536th dimension (of Alan and Naz's new book)!")

while True:
    query = input(Fore.GREEN + "Ask me anything:\n")
    result = qa({"query": query})
    print(Fore.BLUE + textwrap.fill(result["result"],width=150))
    sources = result["source_documents"]
    for index, source in enumerate(sources):
        page_num = source.metadata["page"]
        page_content = source.page_content
        print(Fore.CYAN, f"=========== SOURCE {index+1} ===========")
        print(Fore.CYAN + textwrap.fill(f"""Page: {page_num}""", width=150))
        print(Fore.CYAN + textwrap.fill(page_content, width=150))
        print(Fore.CYAN + f"\n")

