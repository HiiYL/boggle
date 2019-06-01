## Boggle Word Game   [![Build Status](https://travis-ci.org/HiiYL/boggle.svg?branch=master)](https://travis-ci.org/HiiYL/boggle)

A simple Django implementation of the boggle word game.

## SETUP

1. Install requirements using `pip install -r requirements.txt`
2. Run webserver using `python manage.py  runserver`
3. Play the game using a HTTP client, e.g Postman. See [Problem.md](https://github.com/HiiYL/boggle/blob/master/PROBLEM.md) for API Details.

## Running the Tests

#### Django Tests
```
python manage.py test
```

#### Rspec tests
1. Install ruby
2. Install gems:

```
bundle install
```

3. Run test:

```
rspec
```
