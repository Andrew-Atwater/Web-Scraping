# Web-Scraping
A web scraper exercise using Selenium with Chromedriver, scraping the Google Scholar page for keyword 'machine learning' and storing desired data in a Pandas dataframe.

In this task, you will scrape the Google Scholar pages for articles related to machine learning
published since year 2023:
https://scholar.google.com/scholar?as_ylo=2023&q=machine+learning&hl=en&as_sdt=0,20
The above link will take you to the first page of the Google Scholar search results using the
keyword “machine learning” and specifying the years of publication to be 2023 or later. However,
there are more than one page of search results.
Your task is to scrape all pages of the above search results, and collect the following information
about each article: title, publication information (including authors, publication venue, year, and
publisher), and the number of times the article has been cited by other articles. You should
construct a Pandas’ dataframe to hold the above information for each article. Your dataframe
should look like: (see homework)

Process the above dataframe to transform the publication_info column into four
separate columns: authors, year, venue, and publisher. Also, rename the column
cited_by as citation_count, and remove “Cited by” from the citation_count
column. In addition, create a new column named avg_citations_per_year, which
maintains the average number of citations each article received per year. To estimate an
article’s average number of citations per year, we will divide the article’s total citation count
by 3, 2, or 1, if the article was published in 2023, 2024, or 2025, respectively.
Your dataframe should eventually look like: (see homework)

Use the cleaned dataset to do the following:
(b) Find the titles, authors, and years of all articles published in 2024 or later with a total citation
count exceeding 100. You may include your answer in your write-up or a separate text file.
(c) Create a scatterplot of the total citation count versus the average citations per year for the
articles in the dataset. You must include your scatterplot in your write-up.
(d) Create a histogram to visualize the distribution of the average citations per year for the articles
in the dataset. You must include your histogram in your write-up.
(e) What is the number of articles published in each year since 2023? Include your answer in your
write-up. Create a bar plot to visualize the number of articles published in each year since
2023, and include the bar plot in your write-up.
(f) What is the mean citation count of the articles for each publication year? Include your answer
in your write-up. Create a bar plot to visualize the mean citation count of the articles for each publication year, and include the bar plot in your write-up.