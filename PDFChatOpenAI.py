import streamlit as st
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.cassandra import Cassandra
from langchain.llms import OpenAI
from PyPDF2 import PdfReader
import cassio
import base64

# Constants for Cassandra initialization
ASTRA_DB_APPLICATION_TOKEN = "YOUR_TOKEN"
ASTRA_DB_ID = "YOUR_ID"

# Custom CSS for styling
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .reportview-container .main .block-container{
        max-width: 80%;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
    }
    header, .stApp {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .block-container {
        padding: 1rem;
    }
    .pdf-container {
        background-color: #f0f0f0;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
    .pdf-container iframe {
        border-radius: 10px;
        width: 100%;
        height: 800px;
    }
    .suggested-questions-container {
        background-color: #edf4ff;
        padding: 1.5rem;
        border-radius: 10px;
    }
    .suggested-questions-title {
        font-weight: bold;
        color: #1a73e8;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    .suggested-questions-title:before {
        content: '⭐';
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    .suggested-questions p {
        margin: 0;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        color: #333;
        background-color: #fff;
        border-radius: 5px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        border: 1px solid #ddd;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .suggested-questions p:hover {
        background-color: #f1f5ff;
    }
    .suggested-questions p:after {
        content: '➔';
        font-size: 1.2rem;
        color: #1a73e8;
    }
    .message-input-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: white;
        border-radius: 10px;
        padding: 0.5rem;
        margin-top: 1rem;
        border: 1px solid #1a73e8;
    }
    .message-input {
        border: 1px solid #1a73e8 !important;
        border-radius: 10px !important;
        font-size: 1rem;
        width: 100%;
        padding: 0.5rem;
        outline: none;
    }
    .submit-button {
        background-color: white;
        color: #1a73e8;
        border-radius: 10px;
        border: 2px solid #1a73e8 !important;
        padding: 0.5rem 1rem;
        cursor: pointer;
        font-size: 1.2rem;
        margin-left: 0.5rem;
    }
    .submit-button:hover {
        background-color: #1a73e8;
        color: white;
    }
    .stTextInput>div>input {
        border: 2px solid #1a73e8 !important;
        border-radius: 10px !important;
    }
    .stFileUpload>label {
        border: 2px solid #1a73e8 !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True
)

# Header
st.markdown("<h1 style='text-align: left; color: #333;'>Chat with PDF</h1>", unsafe_allow_html=True)

# Layout: Left side for PDF, Right side for chat and suggested questions
col1, col2 = st.columns([3, 2])

# Left side: PDF display and file upload
with col1:

    # Let the user input their OpenAI API Key
    user_openai_api_key = st.text_input("Enter your OpenAI API Key", type="password", key='user-openai-api-key')

    st.markdown("<div class='upload-title'>Upload your PDF file</div>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Drag and drop files here", type="pdf", accept_multiple_files=True)
    
    st.markdown("<div class='pdf-container'>", unsafe_allow_html=True)
    
    if uploaded_files and user_openai_api_key:
        for uploaded_file in uploaded_files:
            # Convert uploaded file to a base64 encoded string
            base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Cassandra initialization
    cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

    # Create the langChain embedding and LLM objects using the user's API key
    if user_openai_api_key:
        llm = OpenAI(openai_api_key=user_openai_api_key)
        embedding = OpenAIEmbeddings(openai_api_key=user_openai_api_key)

        # Create LangChain vector store
        astra_vector_store = Cassandra(
            embedding=embedding,
            table_name="qa_table",
            session=None,
            keyspace=None,
        )

        if uploaded_files:
            raw_text = ""
            for uploaded_file in uploaded_files:
                pdfreader = PdfReader(uploaded_file)
                for page in pdfreader.pages:
                    content = page.extract_text()
                    if content:
                        raw_text += content

            # Split the text into chunks
            text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=800,
                chunk_overlap=200,
                length_function=len,
            )
            texts = text_splitter.split_text(raw_text)

            # Load the dataset into the vector store
            astra_vector_store.add_texts(texts)
            st.write(f"Inserted {len(texts)} text chunks into the vector store.")

            # Create the VectorStoreIndexWrapper
            astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

# Right side: Suggested questions and chat input
with col2:
    st.markdown("<div class='suggested-questions-container'>", unsafe_allow_html=True)
    st.markdown("<div class='suggested-questions-title'>Suggested questions:</div>", unsafe_allow_html=True)
    if uploaded_files and user_openai_api_key:
        # Use the language model to generate suggested questions based on the PDF content
        prompt = "Generate 3 insightful questions that can be asked based on the following content:\n" + raw_text[:1000]
        suggested_questions = llm(prompt).strip().split('\n')
        
        st.markdown("<div class='suggested-questions'>", unsafe_allow_html=True)
        for question in suggested_questions:
            if question:
                st.markdown(f"<p>{question.strip()}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<p>No PDF uploaded yet.</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Message input and submit button
    query_text = st.text_input("Hey! Ask me anything about your PDF.", key='input-unique-key')
    if st.button("Submit", key='submit-button'):
        if query_text and astra_vector_index:
            answer = astra_vector_index.query(query_text, llm=llm).strip()
            st.markdown(f"**Q:** {query_text}", unsafe_allow_html=True)
            st.markdown(f"**A:** {answer}", unsafe_allow_html=True)
