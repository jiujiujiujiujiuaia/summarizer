from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import AzureOpenAI
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import DirectoryLoader
import time
import os 
import tiktoken

tiktoken.model.MODEL_TO_ENCODING["gpt-35-turbo"] = "cl100k_base"

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"

# 1.choose LLm model

use_GPT35 = True
if use_GPT35 :
    os.environ["OPENAI_API_BASE"] = "https://xxxx.openai.azure.com/"
    os.environ["OPENAI_API_KEY"] = "xxxxxx"
    model = 'gpt-35-turbo'
else:
    os.environ["OPENAI_API_BASE"] = "https://xxxxx.openai.azure.com/"
    os.environ["OPENAI_API_KEY"] = "key"
    model = 'gpt-4-32k'

llm = AzureOpenAI(model_name=model,engine=model)

# 2.Choose trained dataset, single file or multiple files

use_directory = False
if use_directory:
    # load all csv files from a directory
    # loader = DirectoryLoader('./datasets/subsets/', glob='*.csv')
    loader = DirectoryLoader('./datasets/subsets_txt/', glob='*.txt')
    # convert to document, each document is a csv file
    split_documents = loader.load()
else:
    # import datatset
    with open('.\AllCountries.csv') as f:
        all_countries = f.read()

    # initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 10000,
        chunk_overlap = 0
    )

    # split document
    split_documents = text_splitter.create_documents([all_countries])
print(f'documents:{len(split_documents)}')


# 3.Load chain

time_start=time.time()
# create map_reduce chain
chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
res = chain({"input_documents": split_documents}, return_only_outputs=False)
# write to json
with open(f'.\report_{model}_refine_{time.strftime("%H_%M_%S", time.localtime())}.txt', 'w') as f:
    f.write(str(res))

time_end=time.time()
print('time cost',time_end-time_start,'s')
