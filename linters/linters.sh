#!/bin/bash

pip install --upgrade pip
pip install -r requirements.txt

ruff check ..
safety check -r ../requirements.txt