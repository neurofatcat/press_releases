import streamlit as st
import yfinance as yf
import pandas as pd

def fetch_yfinance_press_releases(ticker):
    try:
        # Use yfinance to fetch the company object
        company = yf.Ticker(ticker)

        # Fetch news data from yfinance
        news_items = company.news

        if news_items:
            # Parse press releases into a structured format and limit to 10 articles
            press_releases = [
                {
                    "Title": item.get("title"),
                    "Publisher": item.get("publisher"),
                    "Link": item.get("link"),
                    "Publication Date": item.get("providerPublishTime")
                }
                for item in news_items if "press release" in item.get("title", "").lower()
            ][:10]  # Limit to 10 articles

            # Convert to DataFrame for better readability
            df = pd.DataFrame(press_releases)

            # Format the publication date
            if not df.empty:
                df["Publication Date"] = pd.to_datetime(df["Publication Date"], unit="s")

            return df
        else:
            return "No press releases found for this ticker."

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit app
st.title("Press Release Fetcher")

# Input field for ticker symbol
ticker = st.text_input("Enter the ticker symbol of the company:", value="AAPL")

if st.button("Fetch Press Releases"):
    press_releases = fetch_yfinance_press_releases(ticker)

    if isinstance(press_releases, pd.DataFrame):
        st.write("### Press Releases")
        st.dataframe(press_releases)
    else:
        st.write(press_releases)
