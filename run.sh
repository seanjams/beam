#!/bin/bash

# Go to beam repository
cd $HOME/Documents/code/beam

# activate virtualenv
pipenv shell

# start gunicorn
gunicorn -w 1 "main:app"
