## AI-Spring-2021
AI Project Course - Vanderbilt Spring 2021
Group 6 Part 1 Deliverable

## Table of Contents
* [Setup](#setup)
* [Genral Info](#general-info)
* [Navigation](#navigation)

## Setup
Use a Python 3.7 interpreter (or above).
Download the following packages into your project:
- pandas
- xlrd v 1.2.0
- depq

## General Info
This project is a modeling of a world that contains countries with different resources. Countries are able to transfer and transform these resources, and have a certain quality at a given state. A scheduler creates an output of different paths countries can take to do this, and the most beneficial one for the world is ideally chosen.

## Navigation
- country.py: generates a country and its attributes
- main.py: generates a world and its attributes; reading to/from the data files
- world.py: the backbone of our project; contains transform and transfer functions; contains expected utility functions
- scheduler.py: contains the main scheduler function along with its necessary helper functions
- statequality.py: calculation of a country's given state
