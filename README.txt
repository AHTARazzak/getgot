ALI RAZZAK SCRIPT MADE Theoretical Chemistry PhD at UNIVERSITY OF BASEL
For "mercarifun.tar" to be run in Python3

NEEDS SCRAPY

This script scrapes all the images within listings for a specific search term in meracari website, organises into a set of directories for the search term and also compiles a spreadsheet listing details about the listings (price, listing, sold or not)

To change the search term go to line 13 change "Rick Owens" to any other brand, retain the quotation marks.

to use go to directory mercarifun/mercarifun/spiders after unzipping .tar

to use in command line type:
scrapy crawl meriscrape <PUT NAME OF DATASHEET>.<FILEFORMAT>:<FILE FORMAT>
for example:
scrapy crawl meriscrape whatever.csv:csv

1) Make directory for keyword
2) Makes a directory within that directory for each listing
3) downloads all images for each listing and places in directory
4) Creates data base for each listing containng, brand, item code, listing url, price (yen), size, type (pant, shirt etc), and status (sold or not)

For "aucfanscrape.tar" to be run in Python3

This script scrapes all the images within listings for a specific search term in meracari website, organises into a s
et of directories for the search term and also compiles a spreadsheet listing details about the listings (price, listing, sold or not)

To change the search term go to line 13 change "Rick Owens" to any other brand, retain the quotation marks.

to use go to directory mercarifun/mercarifun/spiders after unzipping .tar

to use in command line type:
scrapy crawl okay <PUT NAME OF DATASHEET>.<FILEFORMAT>:<FILE FORMAT>
for example:
scrapy crawl okay whatever.csv:csv

1) Make directory for keyword
2) Makes a directory within that directory for each listing
3) downloads all images for each listing and places in directory
4) Creates data base for each listing containng, brand, item code, listing url, price (yen), size, type (pant, shirt etc)

