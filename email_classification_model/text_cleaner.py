import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Get the list of stopwords
stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Check if the text is a string and not empty
    if not isinstance(text, str) or not text.strip():
        return ""

    try:
        # Remove HTML tags if text resembles HTML content
        if "<" in text and ">" in text:
            soup = BeautifulSoup(text, "html.parser")
            text = soup.get_text()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email signatures (simple heuristic: lines starting with "--")
        text = re.sub(r'--\s*\n.*', '', text, flags=re.DOTALL)
        
        # Remove non-letters
        text = re.sub("[^a-zA-Z\s]", " ", text)
        
        # Convert to lower case and split into words
        words = word_tokenize(text.lower())
        
        # Remove stopwords
        words = [word for word in words if word not in stop_words]
        
        # Remove single letters and non-word letter combinations
        words = [word for word in words if len(word) > 1]
        
        return " ".join(words)
    except Exception as e:
        logging.error(f"Error cleaning email text: {e}")
        return ""
