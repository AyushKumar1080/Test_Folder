import requests

import streamlit as st

FASTAPI_URL = "https://doc-rag-1.onrender.com"

st.title("Hybrid RAG")

uploaded_file = st.file_uploader(

    "Upload Document",

    type=["pdf","txt","csv","docx"]

)

if uploaded_file:

    files = {

        "file":(

            uploaded_file.name,

            uploaded_file.getvalue()

        )

    }

    response = requests.post(

        f"{FASTAPI_URL}/upload",

        files=files

    )

    st.success(

        response.json()["message"]

    )


question = st.text_input(

    "Ask Question"

)

if st.button("Submit"):

    response = requests.post(

        f"{FASTAPI_URL}/ask",

        data={

            "question":question

        }

    )

    result = response.json()

    st.subheader("Answer")

    st.write(result["answer"])

    if "chunks" in result:

        with st.expander("Retrieved Chunks"):

            for chunk in result["chunks"]:

                st.write(chunk)

                st.divider()