# MAthesis
This is the repository for my thesis project. I'm gathering research articles metadata from the most relevant digital humanities journals. Contact me at mangiafrangette@gmail.com to know more :)

## What's inside
The directory ```articles-metadata``` contains all my metadata and the algorithms I used to gather them. 
To keep track of my work I created some readme files in ```articles-metadata/readme```.
In ```articles-metadata/data``` there are all (initial and final) metadata I worked with; data structured according to my schema are in ```articles-metadata/data/json_files/my_schema``` and their filename starts by "ms"; once I go on with my work, I move files in ```articles-metadata/data/unused_files``` to keep my working directory clean - there you can find Crossref and Datacite API requests, xml and bib files, empty files that I'm keeping for the record. 
In ```articles-metadata/src``` there are all the scripts I used to get, clean, add or modify the metadata of interest. In ```articles-metadata/src/journals``` there is everything needed to use Scrapy; the spiders are within ```articles-metadata/src/journals/journals/spiders```.

