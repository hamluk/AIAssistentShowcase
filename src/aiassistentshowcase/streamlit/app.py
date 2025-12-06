import pandas as pd
from supabase import create_client
from aiassistentshowcase.agents.action_agent import ActionAgent

import streamlit as st

from aiassistentshowcase.agents.data_models.dependencies import DBDependencies
from aiassistentshowcase.agents.tools.database_connection import DatabaseConnection
from aiassistentshowcase.config import AIAssistentShowcaseSettings
from pydantic_ai.exceptions import ModelHTTPError

st.set_page_config(page_title="AI Smart Customer Assitent Demo", page_icon="🤖")

# session vars
if "api_model" not in st.session_state:
    st.session_state.api_model = None
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "locked" not in st.session_state:
    st.session_state.locked = False 
if "show_customers" not in st.session_state:
    st.session_state.show_customers = False
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""

example_prompts = [
    "How can you assits me?",
    "Which customers need special support and how can I help them?",
    "I had my first meeting with Arnold Schwarzenegger. Arnold is 78 and a senior developer whose intrests are AI for building muscles and shooting movies."
]

url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase_client = create_client(url, key)

def set_api_model_and_key():
    if st.session_state.api_model_input and st.session_state.api_key_input:
        st.session_state.api_model = st.session_state.api_model_input
        st.session_state.api_key = st.session_state.api_key_input
        st.session_state.locked = True

def unlock_fields():
    st.session_state.locked = False

def toggle_view_customer():
    st.session_state.show_customers = not st.session_state.show_customers

st.title("AI Smart Customer Assistent")

with st.expander("Read Me:"):
    st.markdown("""
            ##### Disclaimer: This demo is not another ChatGPT clone, but rather an autonomously deciding AI agent 🧠💬
                        
            *Q: What does this mean?*  
            A: This showcase demonstrates how an AI Agent is capable of autonomously deciding which tool to use in order to complete a given task.\
            In this particular case, the AI agent can access a database to not only answer your questions but also take care of data management tasks.\
                
    
            *Q: How does it work?*  
            A: Find out for yourself — try starting by asking how it can help you.
                
            #### 📩 Interested in more?
            If you enjoyed this showcase and want to explore custom **AI solutions** for your business or project,  
            feel free to reach out:
                
            | [🌐 Visit my Website](https://lukashamm.dev) | [💬 Visit my LinkedIn Profile](https://www.linkedin.com/in/lukashamm-dev) | [👨‍💻 View my GitHub](https://github.com/hamluk) | [📧 Send me an Email](mailto:lukas@lukashamm.dev) |
            |---|---|---|---|
            """)

st.divider()

st.write("Please choose form the following supported models and provider your own API Key to use the AI Agent.")

st.selectbox(
        key="api_model_input", 
        label="Select AI Model:", 
        options=["mistral:mistral-small-latest", "openai:gpt-4o-mini"],
        index=0,
        disabled=st.session_state.locked)

st.text_input(
        key="api_key_input", 
        label="API Key:", 
        type="password",
        disabled=st.session_state.locked)

if st.session_state.locked:
    st.button(
        key="unlock_button",
        label="Update Model and API Key",
        on_click=unlock_fields)
else:
    st.button(
        key="set_model_api_key",
        label="Set Model and API Key",
        on_click=set_api_model_and_key)

if not st.session_state.api_key:
    st.warning("This Demo only works if you provide your API Key.")
    st.stop()

if not st.session_state.locked:
    st.warning("New Model and API Key will be set after you click the button above.")
else:
    llm_model_full_str = str(st.session_state.api_model).split(":")
    settings = AIAssistentShowcaseSettings(
        llm_model=llm_model_full_str[1],
        model_api_key=st.session_state.api_key,
        active_model=llm_model_full_str[0],
        tavily_api_key=st.secrets["TAVILY_API_KEY"])

    st.subheader("Ask the AI Assistant")
    with st.expander("See example prompts"):
        for prompt in example_prompts:
            if st.button(prompt, type="tertiary"):
                st.session_state.prompt_input = prompt
    
    user_input = st.text_area("Your question:", value=st.session_state.prompt_input)

    if st.button("Ask"):
        if user_input.strip():
            try:
                agent = ActionAgent(settings=settings)
                db_connection = DatabaseConnection()
                db_deps = DBDependencies(db=db_connection)

                with st.spinner("Processing your request..."):
                    answer = agent.run(query=user_input, deps=db_deps)
                st.markdown(f"**Answer:** {answer}")
            except Exception:
                st.error("There was an error processing your request. Please check your API Key and try again.")
        else:
            st.warning("Please enter a question.")

st.button("Hide Customers from Database" if st.session_state.show_customers else "Show Customers from Database", on_click=toggle_view_customer)

if st.session_state.show_customers:
    response = supabase_client.table("customer").select("*").execute()
    if response.data:
        df = pd.DataFrame(response.data)
        st.dataframe(df)
    else:
        st.warning("No customers found in the database.")