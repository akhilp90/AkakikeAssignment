import requests
from bs4 import BeautifulSoup
from transformers import pipeline, MarianMTModel, MarianTokenizer
from keybert import KeyBERT
from TTS.api import TTS

# News Extraction
def get_news_links(company: str) -> list:
    """Scrape news articles from Reuters"""
    url = f"https://www.reuters.com/site-search/?query={company}"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("div", class_="search-results__item__2oqiX")[:10]
        return [a.find("a")["href"] for a in articles if a.find("a")]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def get_article_content(url: str) -> dict:
    """Extract article content"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1").text if soup.find("h1") else "No Title"
        content = " ".join([p.text for p in soup.find_all("p")])
        return {"title": title, "content": content}
    except:
        return {"title": "Error", "content": ""}

# Sentiment & Summarization
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def analyze_sentiment(text: str) -> str:
    result = sentiment_analyzer(text[:512])[0]
    return result["label"].capitalize()

def summarize(text: str) -> str:
    return summarizer(text, max_length=130, min_length=30)[0]["summary_text"]

# Topic Extraction
kw_model = KeyBERT()
def extract_topics(text: str) -> list:
    return [kw[0] for kw in kw_model.extract_keywords(text)]

# Translation & TTS
translator = pipeline("translation_en_to_hi", model="Helsinki-NLP/opus-mt-en-hi")
tts = TTS(model_name="tts_models/hi/fastpitch/hifitts", progress_bar=False, gpu=False)

def translate(text: str) -> str:
    return translator(text[:500], max_length=400)[0]["translation_text"]

def generate_audio(text: str) -> str:
    tts.tts_to_file(text=text, file_path="hindi_summary.wav")
    return "hindi_summary.wav"