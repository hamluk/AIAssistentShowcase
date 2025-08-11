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

st.markdown("""
Welcome to my **AI Assistant Showcase**!  
This demo showcases how AI Agents, enhanced with modern LLM integration and equipped with database-access tools, can autonomously decide which of the available tools to use in order to complete a given task.

Enter your question/ task below and see how my AI Assistant responds in real time.
""")

# --- Call to Action ---
st.subheader("📩 Interested for more?")
st.markdown("""
If you enjoyed this showcase and want to explore **AI solutions** for your business or project,  
feel free to reach out:
""")

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.markdown("[🌐 Visit my Website](https://lukashamm.dev)")
with col2:
    st.markdown("[💬 Visit my LinkedIn Profile](https://www.linkedin.com/in/lukashamm-dev)")
with col3:
    st.markdown("[👨‍💻 View my GitHub](https://github.com/hamluk)")
with col4:
    st.markdown("[📧 Send me an Email](mailto:lukas@lukashamm.dev)")

st.divider()

st.write("Please choose form the following supported models and provider your own API Key to use the AI Agent.")

st.selectbox(
        key="api_model_input", 
        label="Select AI Model:", 
        options=["mistral:mistral-small-latest"], 
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
        llm_mistral_model=llm_model_full_str[1],
        mistral_api_key=st.session_state.api_key,
        active_model=llm_model_full_str[0],
        tavily_api_key=st.secrets["TAVILY_API_KEY"])

    st.subheader("Ask the AI Assistant")
    user_input = st.text_area("Your question:", "")

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