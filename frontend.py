import requests

import streamlit as st

FASTAPI_URL = "http://54.252.167.248:8000"

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

    try:
        response = requests.post(
            f"{FASTAPI_URL}/upload",
            files=files
        )

        response.raise_for_status()

        st.success(response.json()["message"])

    except requests.exceptions.HTTPError:
        try:
            st.error(response.json()["detail"])
        except Exception:
            st.error("Failed to upload document.")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend server.")

    except requests.exceptions.Timeout:
        st.error("Request timed out.")

    except Exception as e:
        st.error(f"Unexpected error: {e}")

question = st.text_input(
    "Ask Question"
)

if st.button("Submit"):

    try:
        response = requests.post(
            f"{FASTAPI_URL}/ask",
            data={
                "question": question
            }
        )

        response.raise_for_status()

        result = response.json()

        st.subheader("Answer")
        st.write(result["answer"])

        if "chunks" in result:
            with st.expander("Retrieved Chunks"):
                for chunk in result["chunks"]:
                    st.write(chunk)
                    st.divider()

    except requests.exceptions.HTTPError:
        try:
            st.error(response.json()["detail"])
        except Exception:
            st.error("Failed to get answer.")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend server.")

    except requests.exceptions.Timeout:
        st.error("Request timed out.")

    except Exception as e:
        st.error(f"Unexpected error: {e}")