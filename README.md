# Infosys AI Chatbot

An intelligent chatbot powered by LLM (Large Language Model) technology that provides information about Infosys. The chatbot uses advanced vector storage and natural language processing to deliver accurate and contextual responses.

## Features

- 🎯 Modern, responsive chat interface
- 💡 Intelligent responses using LLM technology
- 🔍 Vector-based semantic search using Qdrant
- 🔄 Real-time text processing
- 💾 PDF document integration
- 🎨 Glass-morphism UI design

## Technologies Used

- **Frontend**: Streamlit
- **Vector Store**: Qdrant
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **LLM**: FLAN-T5
- **Data Processing**: PyPDF2, LangChain

## Prerequisites

- Python 3.8+
- Docker (for Qdrant)
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Supriya2903/AI_Chatbot_LLM.git
cd AI_Chatbot_LLM
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Start Qdrant server using Docker:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

## Usage

1. Process and index the PDF document:
```bash
python integration.py
```

2. Start the chatbot interface:
```bash
streamlit run streamlitUI.py
```

3. Access the chatbot in your browser at `http://localhost:8501`

## Project Structure

- `streamlitUI.py`: Main chatbot interface with Streamlit
- `integration.py`: PDF processing and vector store integration
- `interactive.py`: Interactive components and utilities
- `scrapping.py`: Data scraping utilities
- `formatted30042024.pdf`: Source data file

## Features in Detail

### Vector Search
The chatbot uses Qdrant vector database to store and search through document embeddings, enabling semantic search capabilities that understand the context of user queries.

### Modern UI
- Glass-morphism design
- Responsive chat bubbles
- Real-time message updates
- Professional color scheme
- Smooth animations

### Document Processing
- Automatic PDF text extraction
- Text chunking for optimal processing
- Vector embeddings generation
- Efficient storage and retrieval

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
