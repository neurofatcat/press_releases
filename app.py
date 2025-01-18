import streamlit as st
import pandas as pd
from newsdataapi import NewsDataApiClient

def fetch_newsdata_press_releases(query):
    try:
        # Initialize the NewsData API client
        api = NewsDataApiClient(apikey="pub_65842e7b50e277f4bae2b2350f8f2bd25924b")

        # Fetch news articles
        response = api.news_api(q=query.strip(), language="en")

        if response["status"] == "success":
            articles = response.get("results", [])

            if not articles:
                return "No news articles found for the given query."

            # Parse news articles into a structured format and limit to 10 articles
            news_data = [
                {
                    "Title": article.get("title"),
                    "Publisher": article.get("source_id"),
                    "Link": article.get("link"),
                    "Publication Date": article.get("pubDate")
                }
                for article in articles
            ][:10]  # Limit to 10 articles

            # Convert to DataFrame for better readability
            df = pd.DataFrame(news_data)

            # Format the publication date
            if not df.empty:
                df["Publication Date"] = pd.to_datetime(df["Publication Date"], errors="coerce")

            return df
        else:
            return f"Failed to fetch data: {response.get('message', 'Unknown error occurred.')}"

    except Exception as e:
        return f"An error occurred while fetching from NewsData.io: {str(e)}"

# Streamlit app
st.title("News Fetcher")

# Input field for search query
query = st.text_input("Enter a query to fetch news articles:", value="pizza")

if st.button("Fetch News from NewsData.io"):
    if not query.strip():
        st.write("Please enter a valid query.")
    else:
        news_data = fetch_newsdata_press_releases(query)

        if isinstance(news_data, pd.DataFrame):
            st.write("### News Articles from NewsData.io")
            st.dataframe(news_data)
        else:
            st.write(news_data)
