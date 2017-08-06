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

Figure 1 | Figure 2
:-------------------------:|:-------------------------:
<img src="/fig/Rating_Count_Plot.png" width="500">  |  <img src="/fig/Producer_Count_Plot.png" width="500">

The overall distribution of scores for all animes:

Figure 3 | Figure 4
:-------------------------:|:-------------------------:
<img src="/fig/Two_Hist_Plot.png" width="500"> | <img src="/fig/Two_Corr_Plot.png" width="500">

Basic comparison by rating and top 15 genres:

Figure 5 | Figure 6
:-------------------------:|:-------------------------:

<img src="/fig/By_rating_Comparison_Plot.png" width="500"> | <img src="/fig/By_genre_Comparison_Plot.png" width="500">


Contact
=======

Shi Wang (<shiwang0211@gmail.com>)
