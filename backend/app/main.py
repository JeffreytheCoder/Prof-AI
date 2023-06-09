import os
import sys
import time
import asyncio
import random
import requests
import subprocess
import re

from dotenv import load_dotenv
from dotenv import load_dotenv

from fastapi import FastAPI, File, UploadFile
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from langchain.document_loaders.unstructured import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.prompts import PromptTemplate
from langchain.llms import Cohere
from langchain.embeddings import CohereEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import LLMChain
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT

load_dotenv()
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API keys
api_key = os.getenv("OPENAI_API_KEY")
cohere_api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    print("OPENAI_API_KEY not found in .env file")
    sys.exit(1)


# loader = UnstructuredFileLoader("./input-docs/2.7.1.txt")
# documents = loader.load()
persist_directory = 'db'
slide_hash = ""
saved_slides= ""
# Documents
# file_name = ""
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_name = "input-docs/"+file.filename
    with open(file_name, "wb") as buffer:
        while True:
            data = await file.read(1024)
            if not data:
                break
            buffer.write(data)
        asyncio.create_task(file.close())
    global loader, documents
    loader = UnstructuredFileLoader(file_name)
    documents = loader.load()
    #documents = loader()
    
    return {"message": f"File '{file.filename}' uploaded successfully"}



# Prompt
slides_prompt = """ 
    The following is the given textbook material:
    
    {text}
    
    For the textbook material above:
    1. Break this text into chunks of concepts, with each chunck contains pieces of text speaking about the same one concept. 
    2. For each such chunks, summarize the content, give online title about the core concept, with two to three bullet points about the details of the concept, each bullet point must not exceed 15 words.
    3. With this title, bullet, description for each chunk, wirte a slides for each chunk in Marp format. 
    
    Rules for slides in Marp format:
    1. Each --- indicates a new slide. Limit 50 words within each slides.
    2. # is for the title of each slide.
    3. - is for bullet point. 1., 2., 3. are numbered points.
    4. <image> (keyword: xxx) is an image illustrating the keyword "xxx". You must include one image for each slide. Make sure keyword "xxx" for each slide is different enough. The keyword "xxx" must be at least 10 words that summarize the entire slide.
    5. `` is for code.

    Following is an example for the above rules for the format:
    # Introduction to Marp

    Marp is a powerful tool that allows you to create presentations using simple Markdown syntax. You can easily create slides and format text with Marp.
    <image> (keyword: what is Marp)

    ---

    # Installing Marp

    To get started with Marp, you can install the Marp CLI or use Marp for Visual Studio Code extension.

    1. Marp CLI: `npm install -g @marp-team/marp-cli`
    2. Marp for Visual Studio Code: Install the extension from the Visual Studio Code marketplace.
    
    <image> (keyword: how to install Marp)

    Now ends with format introduction. 
    
    Output all the slides in 1100 tokens, but make sure they still cover all things in the input text.
    Make sure there are no space or tab before any line of your output.
    Here is your output of slides:
    """

SLIDES_PROMPT = PromptTemplate(
    template=slides_prompt, input_variables=["text"]
)

# chat history
chat_history = []


@app.get("/")
async def test(request: Request):
    """test"""
    return 'test'


@app.get("/slides")
async def generate_response():
    # Split doc into texts
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_texts = text_splitter.split_documents(documents)
    
    MODEL = "OPENAI"  # COHERE
    if MODEL == "COHERE":
        llm = Cohere(cohere_api_key=cohere_api_key, model="command-xlarge-nightly", temperature=0.5, max_tokens=2800)
    else:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5, max_tokens=1100)
    
    # Summarization chain
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=SLIDES_PROMPT)
    slides = chain.run(split_texts)
    print(slides)
    global saved_slides 
    saved_slides = slides

    global slide_hash
    slide_hash = convert_md(slides)
    
    created_time = int(time.time())
    response_data = {
        "created": created_time,
        "model": "prof-ai-v1",
        "content": slide_hash
    }

    return JSONResponse(content=response_data)

transcripts_prompt = """ 
    The following is the given textbook:
    
    {text}

    Textbook ends.

    The following is the given slides:

    """ + saved_slides + """

    Slides ends.
    
    Suppose you are a professor teaching a lecture using the given textbook and slides.
    You are humorous, yet professional in your way of teaching.
    
    You are going to write a speech draft for your lecture. 
    Each slide in the given slides start with --- and the title for this slides starts with #.
    Format your speech draft into sections where each section corresponds to a slide in the given slides. Each section starts with #section_number.
    For each bullet point in a slide, write two to three sentence using related information in the given textbook to explain what the bullet point means, and give example.
    
    Output your speech draft in 1000 tokens, but make sure they still cover all things in the input text.
    Write your speech draft here:
    """

TRANSCRIPTS_PROMPT = PromptTemplate(
    template=transcripts_prompt, input_variables=["text"]
)

@app.get("/transcripts")
async def generate_response_for_transcripts():
    print(transcripts_prompt)
    # Split doc into texts
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_texts = text_splitter.split_documents(documents)
    
    MODEL = "OPENAI"  # COHERE
    if MODEL == "COHERE":
        llm = Cohere(cohere_api_key=cohere_api_key, model="command-xlarge-nightly", temperature=1, max_tokens=2800)
    else:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1, max_tokens=1000)

    # Combine textbook and slides
    # prompt_input = split_texts + ["Textbook ends", "The following is the given slides:" + saved_slides]
    
    # Summarization chain
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=TRANSCRIPTS_PROMPT)
    transcripts = chain.run(split_texts)
    print(transcripts)

    # Parse transcripts
    pattern = r"#section_\d+\n(.+?)(?=\n#section_\d+|\Z)"
    transcript_sections = re.findall(pattern, transcripts, flags=re.DOTALL)

    created_time = int(time.time())
    response_data = {
        "created": created_time,
        "model": "prof-ai-v1",
        "content": transcript_sections
    }

    return JSONResponse(content=response_data)


QA_prompt_template = """Text: {context}

Question: {question}

Answer the question based on the text provided. If the text doesn't contain the answer, reply that the answer is not available."""

@app.post("/qa")
# async def generate_response(request: Request):
async def generate_response_for_qa(request: Request):
    MODEL = "OPENAI"  # COHERE
    
    # Input
    request_data = await request.json()
    user_input = request_data['user_input']
    # user_input = "based on what you know, give me a summary for the text"

    
    # Split doc into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_texts = text_splitter.split_documents(documents)

    # Convert chunks into Chroma vectorized index
    if MODEL == "COHERE":
        llm = Cohere(cohere_api_key=cohere_api_key, model="command-xlarge-nightly", temperature=0.5, max_tokens=2800)
        embeddings = CohereEmbeddings(cohere_api_key=cohere_api_key, model="command-xlarge-nightly")
    else:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5, max_tokens=2800)
        embeddings = OpenAIEmbeddings(model="gpt-3.5-turbo")
    
    chroma = Chroma.from_documents(documents=split_texts, embeddings=embeddings, persist_directory=persist_directory)
    question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
    doc_chain = load_qa_chain(llm, chain_type="map_reduce")
    
    # Chain
    lec1_qa = ConversationalRetrievalChain(
                                          retriever=chroma.as_retriever(),
                                          question_generator=question_generator,
                                          combine_docs_chain=doc_chain,
                                          )
    bot_response = lec1_qa({"question": user_input, "chat_history": chat_history})
    chat_history.append((user_input, bot_response["answer"]))

    # Response 
    created_time = int(time.time())
    response_data = {
        "created": created_time,
        "model": "prof-ai-v1",
        "content": bot_response
    }

    return JSONResponse(content=response_data)


def convert_md(file_string):
    replaced_file_string = replace_image_with_url(get_images_by_keywords(find_image_keywords(file_string)), file_string)
    hash = random.getrandbits(128)
    print("hash value: %032x" % hash)
    f = open(f"../frontend/public/{hash}.md", "w")
    f.write(replaced_file_string)
    f.close()
    subprocess.run(["marp", f"../frontend/public/{hash}.md", "-o", f"../frontend/public/{hash}.pdf"])
    return str(hash)

def replace_image_with_url(res, file_string):
    for key in res:
        side = "left"
        url = res[key][0]
        if random.randint(0, 1) == 0:
            side = "right"
        if res[key][1] > res[key][2]:
            format_image = f"bg fit {side}:{random.randint(20,40)}%"
        else:
            format_image = f"bg fit {side}"
        file_string = file_string.replace(f"<image> (keyword: {key})", f"![{format_image}]({url})")
        print(f"{key}: {url}")
    return file_string


def find_image_keywords(file_string):
    return re.findall(r'<image> \(keyword: (.*?)\)', file_string)


def get_images_by_keywords(queries):
    res = {}
    for query in queries:
        res[query] = get_image(query)
    return res


# Fetch an image from Google Custom Search API
def get_image(query):
    load_dotenv()
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        print("GOOGLE_API_KEY not found in .env file")
        sys.exit(1)
    pse_id = '86382df91391748a6'
    params = {
        'cx': pse_id,
        'num': '5',
        'q': query + ' concept explained',
        'searchType': 'image',
        'key': key,
        'imgSize': 'medium',
    }
    response = requests.get('https://www.googleapis.com/customsearch/v1', params=params)
    data = response.json()
    res = random.choice(data['items'])
    return res['link'], res['image']['height'], res['image']['width']