# moat-bot

This is a [Q&A sample](https://python.langchain.com/en/latest/modules/chains/index_examples/vector_db_qa.html) that uses [Langchain](https://python.langchain.com/en/latest/) and OpenAI's APIs to carry on a conversation
with Nas and Alan's new book.

To get this up and running, you'll first need an API key, available from OpenAI 

Once obtained, export your Open AI API key as an environment variable

```
export OPENAI_API_KEY=<YOUR_KEY>
```

Next, make sure that you're running Python 3.8+ (`python --version`) and install the requirements: 

```
pip install -r requirements.txt
```

Finally, run the file! 

```
streamlit run main.py
```