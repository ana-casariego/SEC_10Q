# SEC_10Q
Web scraper package in Python that scrapes company 10-Q files from the SEC EDGAR website and uses sentiment analysis and NLP to show whether tone can predict short-term movements in share prices.

## Getting Started

### Prerequisites
- ChromeDriver

To downlad ChromeDriver for your version of Chrome, visit <https://chromedriver.chromium.org/downloads>.

### Key files and folders

```
└── nlp_analysis/ 
└── web_scraper/
    └── edgar_10q/        # Web scraper package
        └── __init__.py
        └── cleaner.py
        └── download.py
        └── setup.py
└── README.md
```

## To do 

This project is currently in progress. 

- [ ] `edgar_10q` web scraper package 
  - [x] Add download.py module to download raw 10-q files from SEC EDGAR website
  - [ ] Add cleaner.py module to perform text cleaning
  - [ ] Add sent_extract.py module to create dataframe that counts number of negative, positive, uncertain etc. words for file as 
  - [ ] Add ref.py module to scrape reference data (stock prices and Loughran-McDonald Sentiment Words) 
- [ ] NLP Analysis
  - [ ] Utilize Loughrain McDonald sentiment word list - specifically built for textual analysis related to finance - for textual analysis. 
  - [ ] Finbert NLP Analysis 

## Acknowledgments
- [SEC Edgar](https://www.sec.gov/edgar/searchedgar/companysearch.html) - 10Q html data 


