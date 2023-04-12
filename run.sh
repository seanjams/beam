#!/bin/bash

# Go to beam repository
cd $HOME/Documents/code/beam

# install dependencies
pipenv install

# run gunicorn
RUN_SCHEDULER=true pipenv run gunicorn -w 1 "app:app"
