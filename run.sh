#!/bin/bash

gunicorn -w 1 "main:main()"
