import qdrant_client
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.qdrant import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Path to the PDF file
pdf_path = "formatted30042024.pdf"

# Read PDF and extract text
def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            pdf_text += page.extract_text()
    return pdf_text

# Extract text from PDF
print("Extracting text from PDF...")
raw_text = extract_text_from_pdf(pdf_path)

# Split text into chunks
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
docs = text_splitter.split_text(raw_text)
print(f"Created {len(docs)} text chunks")

# Initialize Qdrant client
client = qdrant_client.QdrantClient(
    "http://localhost:6333",
)

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)

# Get embedding dimension from the model
sample_embedding = embeddings.embed_query("Sample text")
embedding_dimension = len(sample_embedding)

# Define vectors configuration compatible with Qdrant
vectors_config = VectorParams(size=embedding_dimension, distance=Distance.COSINE)

# Create a new collection with a unique name
collection_name = "infosys_knowledge_v1"

try:
    # Try to create the collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=vectors_config,
    )
    print(f"Created new collection: {collection_name}")
except Exception as e:
    print(f"Note: {str(e)}")
    pass

# Initialize vector store
print("Initializing vector store...")
vectorstore = Qdrant(
    client=client,
    collection_name=collection_name,
    embeddings=embeddings
)

# Add texts to vector
print("Adding texts to vector store...")
vectorstore.add_texts(docs)
print("Successfully added texts to vector store!")
