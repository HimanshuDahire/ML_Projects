# News Sentiment Analysis

A Streamlit web application that scrapes news articles based on user queries and performs sentiment analysis using natural language processing techniques.

## Features

- **Real-time News Scraping**: Fetch recent news articles on any topic using Google News search
- **Sentiment Analysis**: Determine if news coverage is positive, negative, or neutral
- **Interactive Visualizations**:
  - Sentiment distribution pie charts
  - Word clouds for unigrams (single words)
  - Word clouds for bigrams (word pairs)
- **Customizable**: Choose the number of articles to analyze

## Technologies Used

- **Python 3.13.3
- **Streamlit**: For the web application interface
- **Selenium**: For automated web browsing and scraping
- **BeautifulSoup4**: For HTML parsing
- **NLTK**: For natural language processing and sentiment analysis
- **Matplotlib**: For data visualization
- **WordCloud**: For generating word clouds

## Installation

```bash
# Clone the repository
git clone https://github.com/username/news-sentiment-analysis.git
cd news-sentiment-analysis

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Download NLTK resources
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# Install Chrome WebDriver for your Chrome version
# Download from: https://sites.google.com/chromium.org/driver/
```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Enter a news topic in the text field (e.g., "Grok AI")

4. Specify the number of news articles to fetch

5. Click "Fetch and Analyze news articles 📰" to start the process

6. View the results including sentiment analysis and word clouds

## How It Works

1. **Data Collection**: The application uses Selenium to search Google News for the requested topic, collects article URLs, and scrapes the content using BeautifulSoup.

2. **Text Preprocessing**: Raw text is tokenized, stopwords are removed, and tokens are lemmatized to prepare for analysis.

3. **Sentiment Analysis**: NLTK's SentimentIntensityAnalyzer is used to classify each article as positive, negative, or neutral.

4. **Visualization**: Results are presented as interactive charts and word clouds.

## Example Results

For a search on "Grok AI":
- Sentiment distribution might show 45% positive, 30% negative, and 25% neutral coverage
- Word clouds highlight the most frequent words and word combinations in the news articles

## Requirements

See the `requirements.txt` file for a complete list of dependencies.

## Future Improvements

- Add source credibility analysis
- Implement topic modeling to identify key themes
- Create time-series analysis for tracking sentiment changes over time
- Add export functionality for reports
- Include advanced filtering options

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NLTK team for their comprehensive natural language processing tools
- Streamlit for making web app development with Python straightforward
