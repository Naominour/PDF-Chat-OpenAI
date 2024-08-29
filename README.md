## Chat with PDF using LangChain and Streamlit
This project is a **web application** built using Streamlit that allows users to **upload PDF files and interact with them** through a chat interface. The application uses **LangChain**, a powerful framework for building applications with **large language models (LLMs)**, along with **Cassandra** for **vector storage**. Users can ask questions about the content of the PDF, and the application will provide responses based on the document's content.


![GPT](https://img.shields.io/badge/Skill-GPT-yellow)
![LLM](https://img.shields.io/badge/Skill-LLM-blueviolet)
![Gen AI](https://img.shields.io/badge/Skill-Gen%20AI-orange)
![Cassandra ](https://img.shields.io/badge/Skill-Cassandra-lightgreen)
![Vector Database](https://img.shields.io/badge/Skill-Vector%20Database-black)
![Conversational Bot](https://img.shields.io/badge/Skill-Conversational%20Bot-green)


## Features
- **PDF Upload:** Users can upload one or multiple PDF files to the application.
- **PDF Display:** Uploaded PDFs are displayed directly in the browser for easy reference.
- **Text Extraction:** The content of the PDFs is extracted and split into manageable chunks for processing.
- **Cassandra Integration:** The application stores the PDF content as vector embeddings in a Cassandra database for efficient retrieval.
- **OpenAI GPT Integration:** Leverages OpenAI's GPT models to answer questions about the uploaded PDFs.
- **Suggested Questions:** Automatically generates insightful questions based on the content of the PDF to guide user interaction.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.8 or higher
- A valid OpenAI API key
- An Astra DB account with a valid application token and database ID
- Streamlit installed (pip install streamlit)
- Required Python packages listed in requirements.txt

  ## Installation
1. **Prerequisites**:
   - Python 3.8 or higher
   - LLama 2 Model

2. **Clone the Repository**:
```bash
git clone https://github.com/yourusername/chat-with-pdf.git
cd chat-with-pdf
```
3. **Set Up Virtual Environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
4. **Install Dependencies**:
```bash
pip install -r requirements.txt
```
5. **Configure your environment**:
   - Update the ASTRA_DB_APPLICATION_TOKEN and ASTRA_DB_ID constants in app.py with your Cassandra credentials.
   - 
6. **Running the Application**:
   - Run the Streamlit application using the following command:
```bash
streamlit run app.py
```

## Usage
- **Open the Application** Once the app is running, open the URL provided by Streamlit in your web browser.
- **Enter OpenAI API Key:** Provide your OpenAI API key to enable the language model features.
- **Upload PDF Files** Drag and drop one or more PDF files into the provided area on the left side of the app.
- **Interact with the PDF:**
- View the uploaded PDF directly in the app.
- Explore suggested questions generated from the content of the PDF.
- Enter your own questions in the input box and get answers based on the PDF content.
