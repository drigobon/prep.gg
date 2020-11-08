# prep.gg

Built initially as project for LiquidHacks. You can check out the final product [here](www.prep.gg).

## Intro

There is a lot of publicly available data on League of Legends (LoL) pro teams. However, it is scattered across multiple websites, the information is not presented in a format easily digestible by teams.

We present [prep.gg](www.prep.gg), a one-stop analytics site for gathering relevant scouting information on LoL pro teams in the four major regions.

## How To Run

Navigate to `./scout-gg-server`. Make sure you pip install everything in `requirements.txt`. Then, run on command line:

```
python3 application.py
```

This hits the development S3 bucket we have, which has public access, so you can run a version of `prep.gg` locally with all the data displaying. We will not be updating the data on the development server as of November 6th, 2020.

## How we built it

Our vision for prep.gg required a robust and fault-tolerant data pipeline with low latency for better user experience. We decided to on the following system design:

The data is collected hourly, with an AWS Cloudwatch trigger starting a cron job on Amazon ECS that uses BeautifulSoup to scrape from data vendors of interest (currently [lol.gamepedia](https://lol.gamepedia.com/League_of_Legends_Esports_Wiki) and [gol.gg](https://gol.gg/esports/home/)) and stores data as json files in an S3 bucket. 

The prep.gg webserver, which is built with Flask, asks the S3 bucket for the most recent data and passes it to frontend Jinja templates for client-side Javascript rendering. This design minimizes server-side latency, and ensures that even if the data pipeline fails, prep.gg still grabs the most recent data it has access to.  

We heavily utilized AWS for this project. Apart from Amazon ECS, AWS Cloudwatch, and AWS S3, we also host our webserver on AWS Beanstalk. This facilitates secure interactions between system components through AWS IAM roles.

The frontend is built from an open-sourced dashboard bootstrap template, and graphs are rendered with the charts.js library.



## Challenges we ran into

Setting up proper IAM roles and permissions for different AWS components to interact was fun.  Also, getting the relevant data from websites in a fault-tolerant manner proved difficult, especially in the cases where the data provided by vendors were corrupted. 





## Accomplishments that we're proud of & what we learned

We created a web page that is user-friendly, functional, and broadly applicable. We’re also proud of having developed better technical and collaborative skills.

Most importantly, we’re grateful to be a part of the first LiquidHacks as a potential avenue to contribute to the esports analytics industry - a cause we are deeply passionate about.

Andy is proud to have completed a full-stack product people can (hopefully) use, and Daniel is proud to have contributed significantly to the project in his first hackathon.


## What's next for prep.gg

Our ultimate goal is for [prep.gg](www.prep.gg) to be used by people in the industry. In that vein, we’d like to make a few changes before the upcoming spring split. First, we want to add a functionality for filtering by patch, split, and date, so that teams can construct manual time windows to scout. In addition, we’re looking to incorporate players’ soloQ data from [u.gg](https://u.gg) and [op.gg](https://op.gg). Lastly, we would like to calculate world-wide and regional averages for different stats, so we can objectively evaluate teams and players with respect to their regional and global competitive scenes.
