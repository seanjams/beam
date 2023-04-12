#!/bin/bash

# Go to beam repository
cd $HOME/Documents/code/beam

# install dependencies
pipenv install

# run gunicorn
pipenv run gunicorn -w 1 "main:app"
