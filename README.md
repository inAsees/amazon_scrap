# Project Info: 
# This program is used to scrap the required data from ww.amazon.com and all the scraped data is stored as JSON file in the users local system .


# Python version : 3.10
# Requirenments
* ## Lib used:
  * ### Requests
  * ### BeautifulSoup
* ## Input file:
   * ### File Path: Automatically received(user dont need to give provide file path) from main.py file as the file is stored in the current working directory which is amazon_scrap . 
   * ### Headers: Google chrome headers are extracted, using curl and are passed as a argument from main.py .
# How to run :
* ## Get into the current working directory (amazon_scrap).
* ## Run the main.py file.

# Note: All those records whose values are not mentioned on website are returned as None/NULL.