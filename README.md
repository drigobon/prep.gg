# prep.gg

Built initially as project for LiquidHacks. You can check out the final product [here](http://www.prep.gg).

## Intro

There is a lot of publicly available data on League of Legends (LoL) pro teams. However, it is scattered across multiple websites, the information is not presented in a format easily digestible by teams.

We present [prep.gg](http://www.prep.gg), a one-stop analytics site for gathering relevant scouting information on LoL pro teams in the four major regions.

## How To Run

Navigate to `./scout-gg-server`. Make sure you pip install everything in `requirements.txt`. Then, run on command line:

```
python3 application.py
```

This hits the development S3 bucket we have, which has public access, so you can run a version of `prep.gg` locally with all the data displaying. We will not be updating the data on the development server as of November 6th, 2020.

## Features in development

Below are features we're currently working on adding.
-add a functionality for filtering by patch, split, and date, so that teams can construct manual time windows to scout 
-incorporate players’ soloQ data from [u.gg](https://u.gg) and [op.gg](https://op.gg)
-calculate world-wide and regional averages for different stats, so we can objectively evaluate teams and players with respect to their regional and global competitive scenes.
