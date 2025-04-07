import streamlit as st
import requests

st.set_page_config(page_title="News Analyzer", layout="wide")

# UI Components
st.title("📰 News Summarization & Sentiment Analysis")
company = st.text_input("Enter a company name (e.g., Tesla, Microsoft):")

if st.button("Analyze News"):
    if company.strip():
        with st.spinner("Analyzing news articles..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze",
                    json={"company": company}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display Results
                    st.subheader(f"Analysis Report for {data['company']}")
                    
                    # Articles Display
                    for idx, article in enumerate(data["articles"], 1):
                        with st.expander(f"Article {idx}: {article['title']}"):
                            st.write(f"**Summary:** {article['summary']}")
                            st.write(f"**Sentiment:** {article['sentiment']}")
                            st.write(f"**Topics:** {', '.join(article['topics'])}")
                    
                    # Sentiment Chart
                    st.subheader("Sentiment Distribution")
                    st.bar_chart(data["sentiment_distribution"])
                    
                    # Audio Player
                    st.subheader("Hindi Summary Audio")
                    st.audio(data["audio_path"])
                    
                else:
                    st.error(f"Error: {response.json()['detail']}")
            
            except Exception as e:
                st.error(f"Connection error: {str(e)}")
    else:
        st.warning("Please enter a company name")