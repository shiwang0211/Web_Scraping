Overview
========

This repository aims to analyze and compare the user scores of animes from two popular anime and manga databases:
- [MyAnimeList.net](https://myanimelist.net/) in United States
- [Animesachi.com](https://www.animesachi.com/) in Japan

The applied techniques include:
- Web scraping using urllib, [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/), re
- Store the collected data in [Google Cloud SQL for MySQL](https://cloud.google.com/sql/docs/mysql/)
- Utilize Pandas, Numpy, [Seaborn](https://seaborn.pydata.org/) to manipulate dataframes and visualize results

Sample codes to extract information from html
------
```python
 Name_US = bsObj.findAll("span", {"itemprop":"name"})[0].get_text()
 Score_US = float(bsObj.findAll("div", {"class":"fl-l score"})[0].get_text())
 Rating_US = bsObj.find(text= 'Rating:').parent.parent.get_text()[11:-3]
 Producer_US = bsObj.find(text= 'Studios:').parent.parent.get_text()[10:-1]
 sql = "insert into anime (id, name, us_score, us_rating, us_producer) values (%s,%s,%s,%s,%s)"
 c.execute(sql,(index,Name_US, Score_US, Rating_US, Producer_US))
 ```
 
Histogram for anime **rating** and **genre**
------

Rating | Producer
:-------------------------:|:-------------------------:
<img src="/fig/Rating_Count_Plot.png" width="500">  |  <img src="/fig/Producer_25_Count_Plot.png" width="500">

The overall distribution of scores for all animes
------

Distribution of Rating (1) | Distribution of Rating (2)
:-------------------------:|:-------------------------:
<img src="/fig/Two_His_Plot.png" width="500"> | <img src="/fig/Two_Corr_Plot.png" width="500">

Basic comparison by rating and top 15 genres
------

Group by Rating | Group by Genre
:-------------------------:|:-------------------------:
<img src="/fig/By_rating_Comparison_Plot.png" width="500"> | <img src="/fig/By_genre_Comparison_Plot.png" width="500">

Sample records
------
<img src="/fig/database.png" width="500">


Contact
=======

Shi Wang (<shiwang0211@gmail.com>)
