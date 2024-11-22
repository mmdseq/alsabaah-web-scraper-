# AlsabahmongoSpider

## Description
The AlsabahmongoSpider is a web scraper built using the Python Scrapy library. It crawls the Alsabaah.iq website, a popular Iraqi news website, and extracts news articles' data. The data is then stored in a MongoDB database.

### Features

- Crawl all posts of the website.
- Crawl any number of pages you want.
- Crawl new posts of website immediately and realtime.
- Crawl (title,img_url,publish_date,link,description,text_without_line_breaks,text_with_line_breaks,tag) from each post.


## Usage

#### Prerequisites

Before using this scraper, ensure you have the following installed:

- Python 3
- Scrapy
- pymongo


    
### Generic data

```yml
---
title: Alsabah web crawler document
author: Mohamad Nadimi
rights:  copyrights 2023
language: en-US
tags: [document, alsabah, crawler, scrapy, mongoDB]
```


#### How to use

    Clone the repository using git clone https://github.com/your_username/AlsabahmongoSpider.git.
    Navigate to the project directory using cd AlsabahmongoSpider.
    Run the scraper using scrapy crawl alsabahmongo.
    Wait for the scraper to finish scraping data from the website.
    Check the database to verify that the data has been stored correctly.

#### Configuration

##### __init__(self, *args, **kwargs):
This method is called when an object of the AlsabahmongoSpider class is created. In this method, the class sets up a connection to MongoDB and initializes several class-level variables including mongo_uri, mongo_db, and collection_name. Additionally, it creates an index on the MongoDB collection to ensure that each document has a unique link. Finally, the method sets the default number of pages to crawl to 4.

   
##### closed(self, reason):
This method is called when the spider is closed. In this method, the class disconnects from MongoDB.

##### parse(self, response):
This method is called when the spider crawls a page. In this method, the spider extracts the links to individual news articles and follows them by calling the parse_link method. Additionally, the spider looks for a link to the next page and follows it if it exists and the current page number is less than the maximum number of pages to crawl.

##### parse_link(self, response):
This method is called when the spider crawls an individual news article. In this method, the spider extracts information about the article including the title, image URL, publish date, tag, and text. The spider then stores this information in a dictionary and tries to insert or update a MongoDB document with the information. Finally, the spider yields the dictionary to be stored in the MongoDB collection.


Overall, the AlsabahmongoSpider class defines a spider that crawls the Alsabaah news website, extracts information about individual news articles, and stores the information in a MongoDB collection. The spider is designed to crawl multiple pages of the website and to ensure that each article is only stored once in the collection.


#### You can run Scrapy spider continuously on a server


1. First you need a server or virtual machine, preferred operating system (e.g. Ubuntu Server 20.04 LTS).
2. Once the virtual machine is created, install Python, Scrapy, and any other dependencies your spider requires.
3. Create a Python script that runs your Scrapy spider.
4. Use the nohup command to run the Python script in the background and redirect the output to a file. Here's an example:
    
nohup python /path/to/your/spider.py > spider.log &

This will run your Scrapy spider in the background and save the output to a file called spider.log.

1. You can then close the terminal or disconnect from the virtual machine without stopping the Scrapy spider.
2. To check the status of the spider, you can use the ps command to list all running processes and search for the process ID (PID) of your spider:

ps -ef | grep spider.py

This will show you the PID of your spider process.

1. To stop the spider, you can use the kill command to send a signal to the spider process. Here's an example:

kill -9 PID

    
Replace PID with the process ID of your spider

That's it! Your Scrapy spider will now run continuously on your VMware virtual machine. Make sure to handle any errors or exceptions that may occur during the spider's continuous execution.

#### Conclusion

The AlsabahmongoSpider is a powerful web scraper that can extract valuable data from the Alsabaah.iq website and store it in a MongoDB database. With its flexible configuration options and powerful Scrapy framework, it can be adapted to meet a wide range of scraping needs.