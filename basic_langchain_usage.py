from langchain.llms import AzureOpenAI
import os

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"
os.environ["OPENAI_API_BASE"] = "xxx"
os.environ["OPENAI_API_KEY"] = "xxx"
model = 'gpt-35-turbo'

llm = AzureOpenAI(
    model_name=model,
    engine=model)
print(llm("what's the AI"))
