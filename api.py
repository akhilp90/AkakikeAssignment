from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import get_news_links, get_article_content, analyze_sentiment, summarize, extract_topics, translate, generate_audio

app = FastAPI()

class CompanyRequest(BaseModel):
    company: str

@app.post("/analyze")
async def analyze_news(request: CompanyRequest):
    try:
        articles = []
        links = get_news_links(request.company)
        
        if not links:
            raise HTTPException(status_code=404, detail="No articles found")
        
        for link in links[:10]:  # Process max 10 articles
            article = get_article_content(link)
            if article["content"]:
                articles.append({
                    "title": article["title"],
                    "summary": summarize(article["content"]),
                    "sentiment": analyze_sentiment(article["content"]),
                    "topics": extract_topics(article["content"])
                })
        
        # Comparative Analysis
        sentiment_counts = {
            "Positive": sum(1 for a in articles if a["sentiment"] == "Positive"),
            "Negative": sum(1 for a in articles if a["sentiment"] == "Negative"),
            "Neutral": sum(1 for a in articles if a["sentiment"] == "Neutral")
        }
        
        # Generate Hindi Summary
        hindi_text = translate(f"{request.company} के बारे में {len(articles)} समाचार लेखों में से {sentiment_counts['Positive']} सकारात्मक, {sentiment_counts['Negative']} नकारात्मक और {sentiment_counts['Neutral']} तटस्थ पाए गए।")
        audio_path = generate_audio(hindi_text)
        
        return {
            "company": request.company,
            "articles": articles,
            "sentiment_distribution": sentiment_counts,
            "audio_path": audio_path
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))