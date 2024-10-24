import streamlit as st
import qdrant_client
from langchain.vectorstores.qdrant import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import T5ForConditionalGeneration, AutoTokenizer, pipeline

# Set page configuration
st.set_page_config(
    page_title="Infosys AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS with professional background and enhanced styling
st.markdown("""
    <style>
    /* Modern background with gradient and pattern */
    .stApp {
        background: linear-gradient(135deg, #0b2447 0%, #19376d 100%);
        background-image: 
            linear-gradient(135deg, #0b2447 0%, #19376d 100%),
            repeating-linear-gradient(45deg, rgba(255,255,255,0.05) 0px, rgba(255,255,255,0.05) 2px, transparent 2px, transparent 8px);
        background-attachment: fixed;
    }
    
    /* Container styling */
    .main {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Chat container with glass effect */
    .chat-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 100px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Message box styling */
    .message-box {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        z-index: 1000;
    }
    
    /* Chat bubbles */
    .chat-bubble {
        padding: 15px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 80%;
        word-wrap: break-word;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #007AFF 0%, #1E90FF 100%);
        color: white;
        margin-left: auto;
        border-radius: 20px 20px 5px 20px;
    }
    
    .bot-bubble {
        background: rgba(255, 255, 255, 0.9);
        color: #333;
        margin-right: auto;
        border-radius: 20px 20px 20px 5px;
    }
    
    /* Header styling */
    .header {
        display: flex;
        align-items: center;
        margin-bottom: 30px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .header-icon {
        font-size: 2.5rem;
        margin-right: 15px;
        text-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .header-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: white;
        text-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        border-radius: 20px !important;
        padding: 10px 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        background: rgba(255, 255, 255, 0.9) !important;
        color: #333 !important;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 20px !important;
        padding: 10px 20px !important;
        background: linear-gradient(135deg, #007AFF 0%, #1E90FF 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }
    
    /* Form styling */
    div[data-testid="stForm"] {
        border: none;
        padding: 0;
    }
    
    /* Spinner styling */
    .stSpinner {
        text-align: center;
        color: white;
    }
    
    /* Placeholder text color */
    ::placeholder {
        color: #666 !important;
        opacity: 1 !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header">
        <div class="header-icon">🤖</div>
        <div class="header-title">Infosys AI Assistant</div>
    </div>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_llm():
    model_name = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=512,
        temperature=0.3,
        do_sample=True
    )
    
    local_llm = HuggingFacePipeline(pipeline=pipe)
    return local_llm

# Initialize components
@st.cache_resource
def initialize_components():
    client = qdrant_client.QdrantClient(url='http://localhost:6333')
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    vector_store = Qdrant(
        client=client,
        collection_name='vectorpdf02052024aaj_v4',
        embeddings=embeddings
    )
    llm = load_llm()
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    return qa

qa = initialize_components()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat container
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="chat-bubble user-bubble">
                    {msg["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-bubble bot-bubble">
                    {msg["content"]}
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Message input box
with st.container():
    st.markdown('<div class="message-box">', unsafe_allow_html=True)
    
    # Create a form for the chat input
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6,1])
        with col1:
            user_input = st.text_input(
                "Message",
                placeholder="Type your message here...",
                label_visibility="collapsed"
            )
        with col2:
            submit_button = st.form_submit_button("Send")

        if submit_button and user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Show thinking animation and generate response
            with st.spinner('Thinking...'):
                response = qa.run(user_input)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Rerun to update the chat display
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
