# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')

from wordcloud import WordCloud
from collections import Counter

import matplotlib.pyplot as plt

import streamlit as st
# Options to avoid browser detection
options = Options()
options.add_argument("start-maximized")
# options.add_argument("--headless")  # Run Chrome in headless mode for efficiency
options.add_argument("--disable-gpu")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Function to scrape the news content
def scrape_news_content(url: str):
    # Set headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Make the request
    response = requests.get(url, headers=headers)
    time.sleep(2) # wait for some time to load the page

    content = None
    if response.status_code == 200: # check for successful response

        # Parse the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <p> elements
        news_contents = soup.find_all("p")

        content = "\n".join([i.text for i in news_contents])

    return content

# Function to get news contents
def get_news_contents(topic: str,
                    num_news_articles:int = 20):

    progress_bar = st.progress(0)
    # Creating Web driver instance for chrome
    driver = webdriver.Chrome(options=options)

    # fetching google webpage
    driver.get("https://www.google.com/")

    # Searching for the news 
    text_box = driver.find_element(by = "name", value="q")
    text_box.send_keys(topic + " news in english")
    text_box.submit()

    time.sleep(2)

    # Going to the news tab
    news_tab = driver.find_element(by = "link text", value="News")
    news_tab.click()

    news_articles = []
    
    while True:
        
        break_while = False

        for i in driver.find_elements(by="class name", value="WlydOe"):
            url = i.get_attribute("href")
            
            content = scrape_news_content(url)

            # Check the number of news articles
            if len(news_articles) == num_news_articles:
                break_while = True
                break
            else:
                # check if content is empty or not
                if  content is None or len(content) < 200:
                    continue
                else:
                    news_articles.append(content)
                    
                    progress = min(len(news_articles) / num_news_articles, 1.0)
                    progress_bar.progress(progress)
        
        # if enough news articles break the while loop
        if break_while:
            break

        # Going to next page
        next_page = driver.find_element(by = "link text", value = "Next")
        next_page.click()

    progress_bar.progress(1.0)
    driver.quit()
    return news_articles

# Function to preprocess the text
def text_preprocessing(text: str):
    """"
    text: list
        String of text to be tokenized
    """

    stop_words = set(stopwords.words('english'))

    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stopwords
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    # Join the tokens to form a string
    processed_text = " ".join(lemmatized_tokens)

    return processed_text

# Function to get the sentiment of the text
def get_sentiment(text: str):
    """
    text: str
        String of text to be analyzed
    """

    sia = SentimentIntensityAnalyzer()
    
    # pre-processing the text
    processed_text = text_preprocessing(text)
    
    sentiment = sia.polarity_scores(processed_text)

    # Classify the sentiment
    result = "Positive" if sentiment['compound'] > 0.05 else "Negative" if sentiment['compound'] < -0.05 else "Neutral"
    
    return result

# Function to plot the sentiment analysis
def plot_sentiment_analysis(news_articles, news_title: str):    
    result = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for article in news_articles:
        sentiment = get_sentiment(article)

        result[sentiment] += 1

    fig, ax = plt.subplots(figsize=(8, 6))
            
    # Color palette
    colors = ['#2ecc71', '#e74c3c', '#3498db']  # Green for Positive, Red for Negative, Blue for Neutral
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        result.values(), 
        labels=result.keys(), 
        autopct='%1.1f%%',
        colors=colors,
        # Explode slightly to make chart more readable
        explode=[0.1 if value > 0 else 0 for value in result.values()]
    )

    # Enhance text properties
    plt.setp(autotexts, size=9, weight="bold")
    plt.setp(texts, size=10)
    
    # Set title
    plt.title(f"Sentiment Analysis of {news_title}", fontsize=12, fontweight='bold')
    
    # Add legend with absolute numbers
    legend_labels = [f"{key}: {value}" for key, value in result.items()]
    plt.legend(wedges, legend_labels, title="Sentiment Counts", loc="upper right")
    
    # Adjust layout to prevent cutting off legend
    plt.tight_layout()

    # Display in Streamlit
    st.pyplot(fig)
    
# Function to plot the unigram word cloud
def plot_unigram_worldCloud(tokens):
    # Create unigram word cloud

    # Create a dictionary of words and their frequency
    word_freq = Counter(tokens.split())

    # Create a word cloud
    wordcloud = WordCloud(width=800, height=400, 
                          background_color='white', 
                          max_words=50, 
                          colormap='viridis').generate_from_frequencies(word_freq)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
        
    # Plot the WordCloud
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Unigram Word Cloud of News Content')
    
    # Ensure tight layout
    plt.tight_layout(pad=0)
    
    # Display in Streamlit
    st.pyplot(fig)

# Function to plot the bigram word cloud
def plot_bigram_wordCloud(tokens):
    from nltk import bigrams

    # Create a list of bigrams
    bi_grams = list(bigrams(tokens.split()))

    # Create a dictionary of bigrams and their frequency
    bi_gram_freq = {" ".join(bigram): freq for bigram, freq in Counter(bi_grams).items()}

    wordcloud = WordCloud(width=800, height=400, 
                            background_color='white', 
                            max_words=50, 
                            colormap='viridis').generate_from_frequencies(bi_gram_freq)
        
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
        
    # Plot the WordCloud
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Bigram Word Cloud of News Content')
    
    # Ensure tight layout
    plt.tight_layout(pad=0)

    # Display in Streamlit
    st.pyplot(fig)

# Main function
def main():
    st.title("News Sentiment Analysis")

    # Get the topic from the user
    topic = st.text_input("Enter the news topic for analysis", "Grok AI")
    num_articles = int(st.text_input("Enter the number of news articles to be fetched", 20))


    if st.button("Fetch and Analyze news articles 📰") and topic:
        with st.spinner("Fetching News Articles...", show_time = True):

            # Get news articles
            news_articles = get_news_contents(topic,num_articles)
            st.success(f"Done! (Fetched {len(news_articles)} articles)")

            st.header("Sentiment of Articles", divider=True)
            # Plot the sentiment analysis
            plot_sentiment_analysis(news_articles, topic)

            # What is the combined sentiment of all the news articles?
            all_articles = " ".join(news_articles)

            result = get_sentiment(all_articles)

            if result == "Positive":
                st.write("Overall sentiment is 😄", result)
            elif result == "Negative":
                st.write("Overall sentiment is 😞", result)
            else:
                st.write("Overall sentiment is 🤔", result)


            all_articles = "\n".join(news_articles)

            # PLotting the unigram and bigram word cloud
            processed_text = text_preprocessing(all_articles)

            st.header("Word Cloud Analysis", divider=True)

            plot_unigram_worldCloud(processed_text)
            plot_bigram_wordCloud(processed_text)

if __name__ == "__main__":
    main()  # Run the main function
