from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from openai import OpenAI

import streamlit as st
import time

#defining the page title
st.title("Chat with Ollama")
st.divider()

## defiing the model client
ollama_model = OllamaChatCompletionClient(model="llama3.2")

#defining llm input message
if "input_msg" not in st.session_state:
    st.session_state.input_msg = ""

#defining the output msg
if "output" not in st.session_state:
    st.session_state.output = ""

#function to call LLM agent
def llm_call(msg:str)-> str:
    sys_message = [{"role":"system","content":"You are a good assistant who responds with intellegent and polite sentences."}]
    message = [{"role":"user", "content":msg}]
    llm_msg = sys_message+message 
    print(msg)
    ollama = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
    model = "llama3.2"
    response = ollama.chat.completions.create(
        model=model,
        messages=llm_msg
    )
    st.session_state.output = response.choices[0].message.content
    return response.choices[0].message.content
    

with st.form(key="Chat_form"):
    st.session_state.input_msg = st.text_input("Let's Chat", icon="🐙")
    reply = st.form_submit_button("send", icon="🚀")
    if reply:
        output = llm_call(st.session_state.input_msg)
        st.write(output)