import streamlit as st
import pandas as pd
import requests

def fetch_newsdata_press_releases(query, page=1):
    try:
        # NewsData.io API endpoint
        endpoint = "https://newsdata.io/api/1/news"
        params = {
            "apikey": "pub_658427ca72d97c97618f89eb495bc04ef5688",  # Replace with your actual API key
            "q": query,
            "language": "en",
            "category": "business",  # Business category
            "page": page  # Pagination for additional results
        }

        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("results", [])

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
            ]

            # Convert to DataFrame for better readability
            df = pd.DataFrame(news_data)

            # Format the publication date
            if not df.empty:
                df["Publication Date"] = pd.to_datetime(df["Publication Date"], errors="coerce")

            return df
        else:
            error_message = response.json().get("message", "Unknown error occurred.")
            return f"Failed to fetch data: {error_message} (HTTP {response.status_code})"

    except Exception as e:
        return f"An error occurred while fetching from NewsData.io: {str(e)}"

# Streamlit app
st.title("News Fetcher")

# Input field for search query
query = st.text_input("Enter a query to fetch news articles:", value="business")

if st.button("Fetch News from NewsData.io"):
    news_data = fetch_newsdata_press_releases(query)

    if isinstance(news_data, pd.DataFrame):
        st.write("### News Articles from NewsData.io")
        st.dataframe(news_data)
    else:
        st.write(news_data)
