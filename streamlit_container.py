import streamlit as st
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS
from colorama import Fore

class StreamlitContainer:
    def __init__(self):
        # Storing the chat
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []
        if 'past' not in st.session_state:
            st.session_state['past'] = []

    def run(self):
        st.write("Hi! I'm MOAT Bot! A bot trained to answer questions from the 1536th dimension (of Alan and Naz's new book)!")

        user_input = st.text_input("Ask a question:", key="input")

        if user_input == "":
            introduction = "To get me started, introduce yourself and provide a couple of questions you can answer"
        else:
            qa = self.get_chain()
            result = qa({"query": user_input})

            st.session_state.past.append(user_input)
            st.session_state.generated.append(result)

            self.format_conversation()

    def format_conversation(self):
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated']) - 1, -1, -1):
                response = st.session_state["generated"][i]
                self.format_response(response)
                # Don't show the first message we used to seed the bot
                if i > 0:
                    question = st.session_state['past'][i]
                    self.format_question(i,question)

    # Result contains source docs and the actual results
    def format_response(self,result):
        st.markdown(result["result"])
#        print(Fore.BLUE + textwrap.fill(result["result"], width=150))
        sources = result["source_documents"]
        for index, source in enumerate(sources):
            page_num = source.metadata["page"]
            page_content = source.page_content
            with st.expander(label=f"SOURCE {index +1}"):
                st.markdown(f"""Page: {page_num}""")
                st.markdown(page_content)
        st.markdown("---")


    def format_question(self,index,question):
        key = str(index) + '_user'
        st.markdown("![person](https://api.dicebear.com/5.x/personas/svg?seed=Bella&size=48) " + question)
        st.markdown("---")

    def get_chain(self):
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

        # db = Chroma.from_documents(pages, embeddings)
        # retriever = db.as_retriever()

        retriever = faiss_index.as_retriever()

        llm = OpenAI(temperature=0, max_tokens=512)

        return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

    def clear_session(self):
        st.session_state.input = ""
        st.cache_resource.clear()
        st.session_state['generated'] = []
        st.session_state['past'] = []
        self.convo.reset()
