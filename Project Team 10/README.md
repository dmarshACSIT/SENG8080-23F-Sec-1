# Analyzing Rental Price Trends in KWC Area

## Table of Contents
- [Overview](#overview)
- [Contributors](#contributors)
- [Date](#date)
- [Abstract](#abstract)
- [Features](#features)
- [Data Sources](#data-sources)
- [Methodology](#methodology)
- [Data Collection](#data-collection)
- [Data Storage and Maintenance](#data-storage-and-maintenance)
- [Data Quality](#data-quality)
- [Data Analysis and Visualization](#data-analysis-and-visualization)
- [Extension](#extension)
- [Proposed Allocation Project Team Roles](#proposed-allocation-project-team-roles)
- [Project Timeline](#project-timeline)


## Overview

This project focuses on the analysis of rental price trends in the KWC (Kitchener, Waterloo, Cambridge) area, with a broader objective of understanding housing changes in Canada. The research utilizes various datasets from sources like the Region of Waterloo Public data and the Government of Canada's public data portal.

## Contributors

- Shivam Nyati (Data Analysis and Visualization)
- Ashwini Seelan Gnanaseelan Vimala (Data Quality and Quality)
- Gokul Mangalathu Mattathil Venugopal (Data Research and Integration)
- Joe Aju (Data Storage and Maintenance)

## Date

October 22, 2023

## Abstract

This report employs data analytic methods to investigate patterns and trends in Canadian home prices over time, focusing on the Kitchener-Waterloo area. The multidisciplinary approach considers geographic, economic, and demographic factors influencing rental pricing.

## Features

- Analysis of rental price trends
- Geographic distribution of rental rates
- Data visualization of property types

## Data Sources

- Region of Waterloo Public data
- Government of Canada's public data portal

## Methodology

The methodology involves a combination of geographic information systems (GIS), data analytics, and data visualization to gain insights into rental rates, property types, and their geographical distribution.

## Data Collection

We collected data from public sources, including [Region of Waterloo Public data](https://open.canada.ca/data/en/dataset/324befd1-893b-42e6-bece-6d30af3dd9f1) and [City of Waterloo public data](https://opendata-city-of-waterloo.opendata.arcgis.com/search?collection=Dataset). We utilized Python libraries like Requests, Beautifulsoup, Selenium, and Scrapy for data fetching and web scraping.

## Data Storage and Maintenance

The data is stored in a MongoDB database for adaptability and scalability. The schema accommodates key facts about rental properties. The NoSQL database allows for extension and sophisticated querying.

## Data Quality

We maintain data quality using Python libraries such as Pandas for cleaning, transforming, and merging data. Descriptive and inferential statistics help ensure high-quality, consistent data.

## Data Analysis and Visualization

Python libraries such as Pandas, NumPy, Matplotlib, Seaborn, GeoPandas, Folium, and Plotly are used for data analysis and visualization. We analyze spatial patterns and create visualizations to understand rental market trends.

## Extension

We plan to extend the geographical area from KWC to the Ontario province and explore new data sources. The storage needs will be determined by the frequency of data, estimated to be >50 GBs.

## Proposed Allocation Project Team Roles

1. **Data Analysis and Visualization**: Shivam Nyati
   - Responsible for data analysis using Python libraries like Pandas and NumPy.
   - In charge of creating visualizations using libraries like Matplotlib, Seaborn, and Plotly.

2. **Data Storage and Maintenance**: Joe Aju
   - Responsible for selecting an appropriate data storage solution, creating database schemas, and managing data storage and maintenance.

3. **Data Quality and Quality**: Ashwini Seelan Gnanaseelan Vimala
   - Coordinates data collection through web scraping, API integration, etc.
   - Ensures accurate and timely data collection and quality assurance.

4. **Data Research and Integration**: Gokul Mangalathu Mattathil Venugopal
   - Identifies and researches relevant data sources.
   - Integrates sourced data into datasets.

## Project Timeline

- **Oct 30**: Data collection, Loading data into DB, Visualization, Quality assurance, and database Schemas (Shivam, Ashwini)
- **Nov 5**: Drafting and Finding the data Quality and sources for data collection (Gokul, Aju)
- **Nov 11**: Presentation drafting (Aju, Gokul, Shivam)
- **Nov 11**: Quality Assurance, finding outliers/Inconsistencies (Ashwini, Shivam, Aju)
- **Nov 17**: Final Edits (All Members)
- **Nov 18**: Report submission (Ashwini)


