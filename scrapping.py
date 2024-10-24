import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from PyPDF2 import PdfReader
import PyPDF2
import re
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to fetch and parse the webpage
def scrape_website(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    return soup

# Function to extract paragraphs from the parsed HTML
def extract_paragraphs(soup):
    paragraphs = soup.find_all("p")
    return [p.get_text() for p in paragraphs]

# Function to write paragraphs to a PDF file
def write_to_pdf(paragraphs_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for paragraphs in paragraphs_list:
        for paragraph in paragraphs:
            pdf.cell(200, 10, txt=paragraph.encode('latin-1', 'replace').decode('latin-1'), ln=True)
    filename = "merged_DATA30042024.pdf"
    pdf.output(filename)
    return filename

# Main function
def main():
    urls = [
        "https://www.infosys.com/",
        "https://www.infosys.com/about.html",
        "https://www.infosys.com/about/history.html",
        "https://www.infosys.com/about/subsidiaries.html",
        "https://www.infosys.com/about/management-profiles.html",
        "https://www.infosys.com/about/alliances.html",
        "https://www.infosys.com/about/awards.html",
        "https://www.infosys.com/about/overview.html",
        "https://www.infosys.com/newsroom/press-releases/2024/top-3-it-services-brand-globally2024.html",
        "https://www.infosys.com/newsroom/features/2023/recognized-global-top-employer.html",
        "https://www.infosys.com/industries.html ",
        "https://www.infosys.com/services.html" ,
        "https://www.infosys.com/products-and-platforms.html",
        "https://www.infosys.com/about/springboard.html",
        "https://www.infosys.com/newsroom/journalist-resources/contact.html",
        "https://www.infosys.org/infosys-foundation/initiatives.html",
        "https://www.infosys.com/leadership-institute.html",
        "https://www.infosys.com/services/generative-ai/overview.html"
    ]
    paragraphs_list = []
    for url in urls:
        soup = scrape_website(url)
        paragraphs = extract_paragraphs(soup)
        paragraphs_list.append(paragraphs)
    
    pdf_filename = write_to_pdf(paragraphs_list)
    print("Scraping Completed and the data has been merged into a single PDF file:", pdf_filename)
    
    print("Removing unwanted words")
    
    remove_unwanted_words(pdf_filename)
    
# Function to remove unwanted data
def remove_unwanted_data(text):
    # Define patterns for unwanted data (e.g., navigation text, headers, footers)
    unwanted_patterns = [
        r"View",
        r"Explore",
        r"View all",
        r"read more",
        r"Go to website",
        r"Case Study",
        r"Case studies",
        r"Digital Core Capabilities",
        r"Digital Operating Model",
        r"Empowering Talent Transformations",
        r"Tales of Transformation",
        r"Industries", 
        r"Services",
        r"Platforms",
        r"Infosys Knowledge Institute",
        r"About Us",
        r"Champions Evolve",
        r"Build vital capabilities to deliver digital outcomes",
        r"Learn more",
        r"Company",
        r"Subsidiaries",
        r"SubsidiariesProgram",
        r"Industries",
        r"The page you requested cannot be found",
        r"Experience",
        r"Insight",
        r"Innovate",
        r"Accelerate",
        r"Assure",
        r"Infosys Knowledge Institute",
        r"About Us",
        r"Press Release",
        r"WHITE PAPER",
        r"Read more",
        r"Programs",
        r"Support",
        r"Being Resilient. That's Live Enterprise",
        r"Recognized As 2024",
        r"Connect with us",
        r"Copyright © 2024 Infosys Limited",
        r"Article",
        r"Platform",
        r"Press release"
    
    ]
    # Remove unwanted patterns
    for pattern in unwanted_patterns:
        text = re.sub(pattern, "", text)
    return text

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to remove unwanted words from PDF
def remove_unwanted_words(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    text_without_unwanted = remove_unwanted_data(text)
    with open("text_without_unwanted.txt", "w") as file:
        file.write(text_without_unwanted)
    print("Unwanted words removed and saved in text_without_unwanted.txt")

def text_to_pdf(text_file, pdf_file):
    # Open the text file and read its contents
    with open(text_file, 'r') as file:
        text = file.read()

    # Create a canvas to draw on
    c = canvas.Canvas(pdf_file, pagesize=letter)

    # Set the font and size
    c.setFont("Helvetica", 12)

    # Set the margin
    margin = 50
    y = 750

    # Write the text to the PDF
    for line in text.split('\n'):
        c.drawString(margin, y, line)
        y -= 15  # Adjust the vertical position for the next line

        # Check if we need to start a new page
        if y < margin:
            c.showPage()  # Start a new page
            y = 750  # Reset the vertical position

    # Save the PDF
    c.save()

# Rest of the code remains the same

if __name__ == "__main__":
    main()
    text_to_pdf("text_without_unwanted.txt", "formatted30042024.pdf")
    print("PDF file completed")