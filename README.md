## Boggle Word Game

A simple Django implementation of the boggle word game.

## SETUP

1. Install requirements using `pip install -r requirements.txt`
2. Run webserver using `python manage.py  runserver`
3. Play the game using a HTTP client, e.g Postman. See [Problem.md](https://github.com/HiiYL/boggle/blob/master/PROBLEM.md) for API Details.

## Running the Tests

1. Run Step 1 and Step 2 above.
2. Install ruby
3. Install gems:

```
bundle install
```

4. Run test:
Rspec tests:
```
1. ensure server is up and running
2. rspec
```
Django tests:
```
python manage.py test
```

