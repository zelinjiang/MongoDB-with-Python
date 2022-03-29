# MongoDB-with-Python

Hey there, welcome!         

This is a series that integrates your knowledge in Web-scraping, RegEx, API and MongoDB (comnnect MongoDB, create databases, create collections, query and update MongoDB, and set Index to speed up your query with Python).         

It consists of 4 files:       
- 0 - samples_pokemon.zip
- 1 - Connecting MongoDB Server and Do Simple Queries.py
- 2 - Comprehensive Project - Scrape(BeautifulSoup), Store, and Query the Yelp Top 40 Donut Shops in San Francisco.py
- 3 - Comprehensive Project 2 - Scrape(Selenium) and Store the Top 100 San Francisco Companies on Zippia.py

The first file is a sample database 'Pokemon', which consists of some charasters of Pokemon that I don't know any of them.             

The second file is a Python code that shows how to connect you local MongoDB server, and make queries.          

The third and fourth file are two comprehensive End-to-End projects that integrate your knowledge in Web-scraping, RegEx, API and MongoDB (includes Indexing).       

They start from scraping the data from webpages and store the information into the database-collection created. Then the program will scrape (or use API to get) some more information and update them into the database. Lastly we will also set an Index on one field to increase the query speed.                   

If you already know well about Web-scraping then they should be understandable, but if you are not, I highly recommend you go through my previous repo 'Web-scraping with BeautifulSoup and Selenium', after you finished the 6 exercises there, you will be very fluent in web-scraping.               


## Coding Questions:
### 1 - Connecting MongoDB Server and Do Simple Queries
Use the 'Pokemon' sample database and: 
- (1) Write a query and return the Pokemons that have candycount equal to the sum of month and date of your birthday
- (2) Write a query and return the Pokemon that with 'num' equal to the month or date of your birthday

### 2 - Comprehensive Project - Scrape(BeautifulSoup), Store, and Query the Yelp Top 40 Donut Shops in San Francisco
- (1) Yelp uses GET requests for its search. Using Python write a program that searches on yelp.com for the top-40 “Donut Shop” in the San Francisco area. Save each search result page to disk. Remember to pause after loading each page
- (2) write new code that opens the search result pages saved in (1) and parses out all shop information (search rank, name, linked URL [this store’s Yelp URL], star rating, number of reviews, store tags, “$” signs, delivery / dine-in tags, and whether you can order through Yelp). Please be sure to skip all “Sponsored Results”.
- (3) Adjust your code in (2) to create a MongoDB collection called “sf_donut_shops” that stores all the extracted shop information, one document for each shop.
- (4) Write a _new_ piece of code that reads all URLs stored in “sf_donut_shops” collection and download each shop page. Store the pages to disk.
- (5) Write new code that reads the 40 shop pages saved in (4) and parses each shop’s address, phone number, and website.
- (6) Sign up for a free account with https://positionstack.com/ Adjust your code in (5) to query each shop address’ geolocation (long, lat) through the API. Update each shop document on the MongoDB collection “sf_donut_shops” to contain the shop’s address, phone number, website, and geolocation. Lastly, place an index on the shop’s search rank.            

### 3 - Comprehensive Project 2 - Scrape(Selenium) and Store the Top 100 San Francisco Companies on Zippia
- (1) Go to the 20 Best Company in San Francisco page using Selenium: https://www.zippia.com/company/best-companies-in-san-francisco-ca/
- (2) Click the 'Show More' Button for 4 times to load the top 100 companies
- (3) Connect to MongoDB and create DataBase for Top100 companies; Create a new database and a new collection in the database to store the information of Top 100 companies. 
- (4) Get the Ranking, Name, Zippia link, Zippia Score, and Description of each company, store these information into the collection. 
- (5) Use the Zippia link of each company in (4), go to the main page of each company, use Selenium driver to click each tab and get these information: 
  - Company's Industry
  - Revenue
  - Headquarter
  - Employee Number 
  - Official Website
  - Founded Year
  - Organization Type
  - Link of Job Section
  - Average Salary
  - 10%-90% Salary Interval 
  - Salary Ranking by Position
- (6) Update new information got in (5) into the collection.           
