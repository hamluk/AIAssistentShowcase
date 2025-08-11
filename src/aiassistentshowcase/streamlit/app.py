from aiassistentshowcase.agents.action_agent import ActionAgent

import streamlit as st

from aiassistentshowcase.agents.data_models.dependencies import DBDependencies
from aiassistentshowcase.agents.tools.database_connection import DatabaseConnection
from aiassistentshowcase.config import AIAssistentShowcaseSettings
from pydantic_ai.exceptions import ModelHTTPError

st.set_page_config(page_title="AI Smart Customer Assitent Demo", page_icon="🤖")

st.title("AI Smart Customer Assistent")
st.write("Please choose form the following supported models and provider your own API Key to use the AI Agent.")

# session vars
if "api_model" not in st.session_state:
    st.session_state.api_model = None
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "locked" not in st.session_state:
    st.session_state.locked = False 

def set_api_model_and_key():
    if st.session_state.api_model_input and st.session_state.api_key_input:
        st.session_state.api_model = st.session_state.api_model_input
        st.session_state.api_key = st.session_state.api_key_input
        st.session_state.locked = True

def unlock_fields():
    st.session_state.locked = False

# AI Model selection
st.selectbox(
        key="api_model_input", 
        label="Select AI Model:", 
        options=["mistral:mistral-small-latest"], 
        index=0,
        disabled=st.session_state.locked)

# AI API Key input
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

# Prüfen, ob Key vorhanden ist
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

    # Chat-Funktionalität
    st.subheader("Ask the AI Assistant")
    user_input = st.text_area("Your question:", "")

    if st.button("Senden"):
        if user_input.strip():
            try:
                    # AI Agent mit Key initialisieren
                agent = ActionAgent(settings=settings)
                db_connection = DatabaseConnection()
                db_deps = DBDependencies(db=db_connection)

                with st.spinner("Processing your request..."):
                    # Run the agent with the user input and database dependencies
                    answer = agent.run(query=user_input)
                st.markdown(f"**Answer:** {answer}")
            except ModelHTTPError:
                st.error("There was an error processing your request. Please check your API Key and try again.")
        else:
            st.warning("Please enter a question.")