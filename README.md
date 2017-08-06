Overview
========

This repository aims to analyze and compare the user scores of animes from two popular anime and manga databases:
- [MyAnimeList.net](https://myanimelist.net/) in United States
- [Animesachi.com](https://www.animesachi.com/) in Japan

The applied techniques include:
- Web scraping using urllib, [Beatiful Soup](https://www.crummy.com/software/BeautifulSoup/), re
- Store the collected data in [Google Cloud SQL for MySQL](https://cloud.google.com/sql/docs/mysql/)
- Utilize Pandas, Numpy, [Seaborn](https://seaborn.pydata.org/) to manipulate dataframes and visualize results

Histogram for anime **rating** and **genre**
![](/fig/Rating_Count_Plot.png)
![](/fig/Producer_Count_Plot.png)

The overall distribution of scores for all animes:
![](/fig/Two_Hist_Plot.png)
![](/fig/Two_Corr_Plot.png)

Basic comparison by rating and top 15 genres:
![](/fig/By_Rating_Comparison_Plot.png)
![](/fig/By_genre_Comparison_Plot.png)


Contact
=======

Shi Wang (<shiwang0211@gmail.com>)
