import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv, find_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.utilities import PythonREPL
from langchain.chat_models import AzureChatOpenAI

# get configurations
load_dotenv(find_dotenv())
api_key  = os.getenv('OPENAI_API_KEY')
ps_specs = os.getenv('SPECS')
model = os.getenv('LLM_MODEL')
api_version = os.getenv('OPENAI_API_VERSION')
base_url = os.getenv('OPENAI_API_BASE')

# get path for static files
static_dir = os.path.join(os.path.dirname(__file__), 'static')  
if not os.path.exists(static_dir): 
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# initialise the agent
def initAgent():
    # read the specifications from file
    specs = ""
    with open(ps_specs, 'r') as file:
        specs = file.read()

    # this is the in-context prompt
    sys_prompt = f"""
You are a helpful assistant who can execute PromptScript scripts. The
specifications for the PromptScript language are in triple square brackets.
[[[ {specs} ]]]
"""
    python_repl = PythonREPL()
    repl_tool = Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. \
            Input should be a valid python command. If you want to see the \
            output of a value, you should print it out with `print(...)`.",
        func=python_repl.run
    )
    tools = [repl_tool]

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = AzureChatOpenAI(
        temperature=0.0,
        openai_api_base=base_url,
        openai_api_version=api_version,
        deployment_name=model,
        openai_api_key=api_key,
        openai_api_type = "azure",
        
    )    

    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
        verbose=True, 
        memory=memory,
        handle_parsing_errors="Check your output and make sure it conforms!")

    agent.run(sys_prompt)
    return agent

# start server
server = Flask(__name__, static_folder=static_dir, template_folder=static_dir)
agent = initAgent()

# server landing page
@server.route('/')
def landing():
    return render_template('index.html')

# run the promptscript
@server.route('/run', methods=['POST'])
def run():
    data = request.json
    user_prompt = f"""
Execute the PromptScript script in triple angle brackets.
<<< {data['input']} >>>. Output the results of the execution 
and nothing else. Do not provide any preamble or post execution 
comments. When executing Python code, just output the results 
of the execution only.
"""
    response = agent.run(user_prompt)    
    return jsonify({'input': data['input'],
                    'response': response})

if __name__ == '__main__':
    # start server
    server.run("127.0.0.1", 7477, debug=False)
    

