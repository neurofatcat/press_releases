import streamlit as st
import pandas as pd
import requests

def fetch_newsdata_press_releases(query, page=1):
    try:
        # NewsData.io API endpoint
        endpoint = "https://newsdata.io/api/1/news"
        params = {
            "apikey": "pub_65842e7b50e277f4bae2b2350f8f2bd25924b",  # User-provided API key
            "q": query.strip(),  # Ensure no leading/trailing spaces
            "language": "en",  # Language parameter
            "category": "business",  # Business category
            "page": page  # Pagination for additional results
        }

        # Make the API request
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
            ][:10]  # Limit to 10 articles

            # Convert to DataFrame for better readability
            df = pd.DataFrame(news_data)

            # Format the publication date
            if not df.empty:
                df["Publication Date"] = pd.to_datetime(df["Publication Date"], errors="coerce")

            return df
        elif response.status_code == 422:
            return "The request was unprocessable. Ensure the query and parameters are valid."
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
    if not query.strip():
        st.write("Please enter a valid query.")
    else:
        news_data = fetch_newsdata_press_releases(query)

        if isinstance(news_data, pd.DataFrame):
            st.write("### News Articles from NewsData.io")
            st.dataframe(news_data)
        else:
            st.write(news_data)
