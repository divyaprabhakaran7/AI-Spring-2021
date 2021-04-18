## AI-Spring-2021
AI Project Course - Vanderbilt Spring 2021
Group 6 Part 2 Deliverable

## Table of Contents
* [Setup](#setup)
* [Genral Info](#general-info)
* [Navigation](#navigation)
* [How To Run](#how-to-run)

## Setup
Use a Python 3.7 interpreter (or above).
Download the following packages into your project:
- pandas v 1.1.3
- xlrd v 1.2.0
- depq
- XlsxWriter

## General Info
This project is a modeling of a world that contains countries with different resources. Countries are able to transfer and transform these resources, and have a certain quality at a given state. A scheduler creates an output of different paths countries can take to do this, and the most beneficial one for the world is ideally chosen.

We have put in 5 test case files as well as their output files in /data. If you would like to create your own test cases (initial states), feel free to add them to the data file and update the method test_cases() in main.py to account for them.

## Navigation
- country.py: generates a country and its attributes
- main.py: generates a world and its attributes; reading to/from the data files
- world.py: the backbone of our project; contains transform and transfer functions; contains expected utility functions
- scheduler.py: contains the main scheduler function along with its necessary helper functions
- statequality.py: calculation of a country's given state

## How To Run
1. Navigate to the project folder in Terminal
2. Activate a virtual environment with the appropriate packages installed (see Setup). Example using conda: 
```
conda activate virtual_env_name
```
3. Run main.py. Example (depending on the version of python installed): 
```
python main.py
```
OR
```
python3 main.py 
```
