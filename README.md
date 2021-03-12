# MAthesis
This is the repository for my thesis project "Twenty years of research in Digital Humanities: a topic modeling study" within the Digital Humanities and Digital Knowledge Master Degree at the University of Bologna. Datasets are also published in Zenodo [1]

## Abstract
### Purpose
The purpose of this dissertation is to describe and explore through the lenses of scholarly publication the trends of original research works in the Digital Humanities (DH) of the last 20 years.
### Design/methodology/approach
This study is based on two datasets built by web scraping DH journals’ official web pages and API requests to popular academic databases (Crossref, Datacite). The datasets constitute a corpus of DH research and include research papers abstracts and abstract papers from DH journals and international DH conferences published between 2000 and 2020. Probabilistic topic modeling with latent Dirichlet allocation is then performed on both datasets to identify relevant research subfields. The work explores subfield trends in the defined time frame and with respect to countries derived from authors’ institutional affiliations using an interactive visualization.
### Findings
Results show that text analysis is the hallmark of DH research and has been the most popular research topic over the last two decades. Productivity of identified research subfields seems to be stable over time in the past ten years. DH research is prominently represented by North American and European institutions but it has opened to the contribution of diverse countries in the past ten years.
### Research limitations/implications
This study was limited to research articles or conference papers written in English, allowing for an overrepresentation of English speaking countries. The study also considered only original research contributions, thus excluding other common publication categories such as review, case study, conference poster, and panel discussion. Data of DH conferences held in 2001, 2005 and 2009 was not available. At the time of this study, many papers from 2020 had not been published yet. 
### Originality/value
To explore Digital Humanities research using topic modeling techniques, contributing to the international debate around the history and development of the field.

## What's inside
The directory ```articles-metadata``` contains all my metadata and the algorithms I used to gather them. ```articles-metadata/readme``` contains some notes that I wrote to keep track of my work.

In ```articles-metadata/data``` there are all (initial and final) metadata I worked with; data structured according to my schema are in ```articles-metadata/data/json_files/my_schema``` and their filename starts by "ms"; once I go on with my work, I move files in ```articles-metadata/data/unused_files``` to keep my working directory clean - there you can find Crossref and Datacite API requests, xml and bib files, empty files that I'm keeping for the record. 

In ```articles-metadata/src``` there are all the scripts I used to get, clean, add or modify the metadata of interest. In ```articles-metadata/src/journals``` there is everything needed to use Scrapy; the spiders are within ```articles-metadata/src/journals/journals/spiders```.

```Dataframe``` contains csv files with the productivity metric, which is the metric that was devised to learn the amount of a topic that a certain country has produced through time, assuming a connection between the number of affiliations of a document, the research effort and the involvement of a country. The files within contain various numbered steps of the computation.

```topic_models``` directory contains input and output data used within MITAO, a tool for mashing up automatic text analysis tools, and creating a completely customizable visual workflow (https://github.com/catarsi/mitao) [2]. The topic modeling results are divided in two folders, one for each of the datasets. 

## References
[1] Francesca Mangialardo, & Peroni Silvio. (2021). Methodology data of "Twenty years of research in Digital Humanities: a topic modeling study" (Version Version 1) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4552436
[2] Ferri, P., Heibi, I., Pareschi, L., & Peroni, S. (2020). MITAO: A User Friendly and Modular Software for Topic Modelling [JD]. PuntOorg International Journal, 5(2), 135–149. https://doi.org/10.19245/25.05.pij.5.2.3
