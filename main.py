# from dotenv import load_dotenv
# import os

# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_astradb import AstraDBVectorStore
# from langchain. agents import create_tool_calling_agent
# from langchain. agents import AgentExecutor
# from langchain. tools. retriever import create_retriever_tool
# from langchain import hub
# from github import fetch_github_issues

# load_dotenv()

# # connecting to vector store (astradb)

# def connect_to_vstore():
#     # embedding is a method of changing the textual data to a vector 
#     embeddings = OpenAIEmbeddings()
#     ASTRA_DB_ENDPOINT = os.getenv("ASTRA_DB_ENDPOINT")
#     ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
#     desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")
    
#     # checking if this is an empty string or not 
#     if desired_namespace:
#         ASTRA_DB_KEYSPACE =desired_namespace
#     else:
#         ASTRA_DB_KEYSPACE = None
        
#     vstore = AstraDBVectorStore(
#         embedding=embeddings,
#         collection_name="github",
#         api_endpoint="ASTRA_DB_ENDPOINT",
#         token="ASTRA_DB_APPLICATION_TOKEN",
#         namespace="ASTRA_DB_KEYSPACE"
#     )
#     return vstore()
# vstore = connect_to_vstore()
# # Adding Documents to vstore 
# add_to_vstore = input("Do you want to update the issues? (y/n): ").lower() in ["yes","y"]

# if add_to_vstore :
#     owner = "moharir-pinak"
#     repo = "multiple_diseases_prediction"   
#     issues = fetch_github_issues(owner,repo)      
     
#     try:
#         vstore.delete_collection()  # clearing the previous issues in the collection 
#     except :
#         pass
    
#     vstore = connect_to_vstore() # as we have deleted the collection so we have to connect to vstore once againg to create it 
#     vstore.add_documents(issues)
    
#     results = vstore.similarity_search("flash messages" , k=3) # k is the number of documents
#     for res in results:
#         print(f"* {res.page_content} {res.metadata}")


#2 Ai given code 

from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from github import fetch_github_issues
from note import note_tool

load_dotenv()


def connect_to_vstore():
    embeddings = OpenAIEmbeddings()
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")

    if desired_namespace:
        ASTRA_DB_KEYSPACE = desired_namespace
    else:
        ASTRA_DB_KEYSPACE = None

    vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="github",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )
    return vstore


vstore = connect_to_vstore()
add_to_vectorstore = input("Do you want to update the issues? (y/N): ").lower() in [
    "yes",
    "y",
]

if add_to_vectorstore:
    owner = "techwithtim"
    repo = "Flask-Web-App-Tutorial"
    issues = fetch_github_issues(owner, repo)

    try:
        vstore.delete_collection()
    except:
        pass

    vstore = connect_to_vstore()
    vstore.add_documents(issues)

    # results = vstore.similarity_search("flash messages", k=3)
    # for res in results:
    #     print(f"* {res.page_content} {res.metadata}")

retriever = vstore.as_retriever(search_kwargs={"k": 3})
retriever_tool = create_retriever_tool(
    retriever,
    "github_search",
    "Search for information about github issues. For any questions about github issues, you must use this tool!",
)

prompt = hub.pull("hwchase17/openai-functions-agent")
llm = ChatOpenAI()

tools = [retriever_tool, note_tool]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

while (question := input("Ask a question about github issues (q to quit): ")) != "q":
    result = agent_executor.invoke({"input": question})
    print(result["output"])