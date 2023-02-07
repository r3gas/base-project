# My Selenium/Python Repo

* This repo serves as a portfolio for all Python and/or Selenium projects I work on

## Setup
* This repo uses Pipenv which should come with any current version of Python 3.X
* Pycharm is the default IDE used in creating this project
* If you care to pull this repo you will want to clone it, then run ```pipenv install```
  * This will allow you to pickup all the necessary modules

## Other things to know
* Selenium is configured to run against chrome
* * If you have never installed chromedriver
  * ```brew install --cask chromedriver```
* If you have previously installed chromedriver run 
  * ```brew reinstall --cask chromedriver```
* To allow chromdriver to run (iOS specific)
  * ```xattr -d com.apple.quarantine /usr/local/bin/chromedriver```