# Meme Analysis

Analysing the trend of a particular meme template over time, using Reddit as the source.

## Features

- Track the popularity and usage trend of specific meme templates.
- Uses Reddit as the primary data source.

## What this project does
 - Web Scraping (Reddit) 
 - Text analysis
 - Time Series
 - Social Network analysis

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kavinraj-95/meme-analysis.git
   cd meme-analysis
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Steps to Run

1. **Configure Reddit API Credentials:**
   - Make sure you have a Reddit account and create an application to get your `client_id`, `client_secret`, and `user_agent`.
   - Add these credentials to a `.env` file or directly into the configuration section of your code.

2. **Run the analysis script:**
   ```bash
   python src/main.py
   ```

3. **View Results:**
   - Output results will be available in the result/ directory.

## Contributing

Feel free to open issues or submit pull requests for new features and bug fixes!

## License

This project currently does not have a license. Please open an issue if you wish to discuss licensing.
