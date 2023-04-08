# Euro Counter

## What is it?
The aim of this project is to collect viewing numbers of YouTube videos
of the Eurovision Song Contest to determine if views correlate to the final
position of each country in the contest.
These view numbers are displayed in a graph in such a way so that the viewer can
easily determine which country's song is most viewed compared to the others.
The Eurovision videos that are used for this collection are only the live performances
of each country in the semi-final qualifying event. We presume that the view
numbers for those videos are more reliable than if we were to collect data from the music videos.
Sometimes this rule is broken, for example with the big-5 countries, but users should
be aware that data for those videos is likely not as accurate.

## Project Structure

This project is split into 2 parts. The first part is a relatively self-contained
pure Python project called "eurovision_youtube_counter". This part retrieves the data
for each video and stores it in the database.

The second part is called "euro_counter" and is the Django app that is 
responsible for the website that displays the YouTube data in the database.

## Deployment
To run this project you are going to need a secret key for Django. That should
be located in the 'eurovision_data/eurovision_data/secrets/secret_key.txt'.
This (and any other secrets) is not in this git repo so you can just generate your own.

To run the data collection part you need configuration details that are usually
stored in 'eurovision_data/eurovision_data/config/cron.ini'. This is not in this
git repo but you can find it on the production environment. If you don't have access
to that then you need to generate your own YouTube API key.

You needto run the Django project with the environment variable 'ENVIRONMENT'.
It's value should be 'DEVELOPMENT' or 'PRODUCTION' depending on which you want to run.

Everything else should be in the requirements.txt file.

## Miscellaneous
Trello board: https://trello.com/b/vGKvoaH1/euro-counter