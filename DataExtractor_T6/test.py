import urllib.parse
import os
import streamlit as st
from langchain.llms.openai import OpenAI
from langchain_openai import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv(".\\Env_Variables.txt")

# Getting values from Env_Variables file:
username = os.getenv("db_username")
password = os.getenv("db_password")
hostname = os.getenv("db_hostname")
dbname = os.getenv("dbname")
# print(username, "...", password, "...", hostname, "and", dbname)
openai_api_key = os.getenv("OPENAI_API_KEY")


# Function to create SQL agent
def create_sql_agent_with_streamlit(db):
    # Initialize ChatOpenAI model
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    # llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
    # Create SQLDatabaseToolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # Create SQL agent executor
    agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)
    return agent_executor


# Declaring Main Method
def main():
    # Set the page title
    st.set_page_config(page_title="Data Extractor")

    # Add an icon image
    icon = "./Cognizant_logo.png"
    # st.image(icon, width=70, caption="Cognizant")
    st.image(icon, width=350)
    st.markdown("\n")
    # To Display an animated GIF
    # st.image("./CognizantGIF.gif", width=450)
    # st.caption("Aetna")

    # st.title("COGNIZANT")
    ## Font setup
    # st.markdown(
    #     """
    #     <style>
    #     .title {
    #         width: 40%;
    #         font-family: Arial;
    #         font-size: 20px;
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )

    # Display the title
    st.title("Data Extractor")

    # To Display Database connection details in Browser
    # st.sidebar.header("Database Connection")
    # username = st.sidebar.text_input("Username", value="postgres")
    # password = st.sidebar.text_input("Password", type="password", value="Test1234")
    # hostname = st.sidebar.text_input("Hostname", value="localhost")
    # dbname = st.sidebar.text_input("Database Name", value="TestDB_Trail1")

    # Connection URI setup
    encoded_password = urllib.parse.quote_plus(password)
    uri = f"postgresql://{username}:{encoded_password}@{hostname}:5432/{dbname}"
    db = SQLDatabase.from_uri(uri)

    # Create SQL agent
    agent_executor = create_sql_agent_with_streamlit(db)

    # User input
    user_input = st.text_input("Enter the description of data you are looking for: ")

    if st.button("Submit"):
        # Execute user query
        result = agent_executor.run(user_input)
        st.write("Relevant Data you have requested:", result)

# Execute Main method directly
if __name__ == "__main__":
    main()

