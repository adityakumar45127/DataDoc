from dotenv import load_dotenv
import os
import streamlit as st


load_dotenv()


def get_google_api_key():

    api_key = os.getenv(
        "GOOGLE_API_KEY"
    )

    if not api_key:

        api_key = st.secrets.get(
            "GOOGLE_API_KEY"
        )

    return api_key