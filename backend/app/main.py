import os
import sys
import time
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from langchain.document_loaders.unstructured import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain.llms import OpenAI
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.prompts import PromptTemplate
from langchain.llms import Cohere
from langchain.embeddings import CohereEmbeddings
os.environ["GOOGLE_CSE_ID"] = os.getenv("GOOGLE_CSE_ID")
os.environ["GOOGLE_API_KEY"] = os.getenv("COHERE_API_KEY")

load_dotenv()
app = FastAPI()

# API keys
api_key = os.getenv("OPENAI_API_KEY")
cohere_api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    print("OPENAI_API_KEY not found in .env file")
    sys.exit(1)

# Documents
loader = UnstructuredFileLoader('./docs/lecture1.txt')
documents = loader.load()
persist_directory = 'db'

# Prompt
prompt_template = """
{context}

Learn the textbook information above. Imagine you are a computer science professor teaching computer networking. Output a few slides in markdown format, each summarizing a part of the textbook material above, in sequence of the text material. Include a image link you found online that effectively illustrate the material in that slide.

After each slide, follow a few paragraphs on how you would talk to the students (like an experienced computer science professor) to effectively teach the material contained in the slides.
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context"]
)
chain_type_kwargs = {"prompt": PROMPT}


@app.get("/")
async def test(request: Request):
    """test"""
    return 'test'


@app.post("/")
async def generate_response(request: Request):
    # Input
    request_data = await request.json()
    user_input = request_data['user_input']

    # Index
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=100)
    split_texts = text_splitter.split_documents(documents)

    llm = Cohere(cohere_api_key=cohere_api_key, model="command-xlarge-nightly", temperature=2, max_tokens=4096)
    embeddings = CohereEmbeddings(cohere_api_key=cohere_api_key, model="command-xlarge-nightly")
    
    #llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1, max_tokens=10000)
    #embeddings = OpenAIEmbeddings(model="gpt-3.5-turbo")
    
    chroma = Chroma.from_documents(documents=split_texts, embeddings=embeddings, persist_directory=persist_directory)
    
    # Chain
    chain = load_qa_chain(llm)
    content = chroma.similarity_search(user_input)
    answer = chain.run(input_documents=content, question=user_input)
    trimmed_answer = answer.replace("\n"," ")
    
    # lec1_qa = RetrievalQA.from_chain_type(llm=llm, 
    #                                       chain_type="stuff", 
    #                                       retriever=chroma.as_retriever(), 
    #                                       chain_type_kwargs=chain_type_kwargs)

    # Agents
    # g_search = GoogleSearchAPIWrapper()
    # tools = [
    #     Tool(
    #         name = "CS118 Lec1 QA System",
    #         func=lec1_qa.run,
    #         description="useful for when you need to answer questions about the lectrue 1 of CS118 computer network. Input should be a fully formed question."
    #     ),
    #     Tool(
    #         name = "CS118 Lec1 Further Info System",
    #         func=g_search.run,
    #         description="useful for when you need to answer questions about the extra information extending the lectrue 1 content of CS118 computer network, when requesting for further information on the lecture content. Input should be a fully formed question."
    #     )
    # ]
    # agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    
    # Response
    # bot_response = lec1_qa.run(user_input)
    created_time = int(time.time())
    response_data = {
        "created": created_time,
        "model": "llm-gpt-demo-v1",
        "content": trimmed_answer
    }

    return JSONResponse(content=response_data)

# @app.post("/qa")