# STEB - Simple Telegram Exchange Bot
STEB - is a telegram exchange bot for currency exchange by provided URL-API. Created as test task.

## Test task
This test task was not new and unique (so be cautionary with those, who gives you this), and I have indeed found existing solutions. [For example](https://github.com/iii-xvi/tt-001).
I quote this task as it was presented to me, so it will be possible to find this repository in Google:
> Implement a small exchange rate telegram bot which does the following: Uses exchange rate data from this web service: exchangeratesapi.io or similar. Returns the latest exchange rates in a listview. USD should be used as base currency and converts currency from the list.
> 
> Requirements.
> Add the following commands: /list or /lst - returns list of all available rates from: api.exchangeratesapi.io/latest?base=USD. Item of the listview should have 2 rows: the currency name in the first row and the latest exchange rate (with two decimal precision) in the second row: Ex.
> 
> DKK: 6.74
> HUF: 299.56
> Once the currency data is loaded from the service, save it in a local database too. Also, save the timestamp of the last request somewhere. Next time user requests anything the app you should check whether 10 minutes elapsed since the last request:
> 
> If yes, you should load new data from web service.
> If no, you should load previously saved data from the local database.
> /exchange $10 to CAD or /exchange 10 USD to CAD - converts to the second currency with two decimal precision and return. Ex.:
> 
> $15.55
> /history USD/CAD for 7 days - return an image graph chart which shows the exchange rate graph/chart of the selected currency for the last 7 days. Here it is not necessary to save anything in the local database, you should request every time the currency data for the last 7 days. Example request for getting currency history in a given period between USD and CAD: api.exchangeratesapi.io/history?start_at=2019-11-27&end_at=2019-12-03&base=USD&symbols=CAD
> 
> Results must be given as sources and short instruction how to run it.

This bot succeeds in all of the requirements, except checking 10 minutes interval and loading local data. *If you know how to do it relatively simple in Python, please contact me; my undying gratitude will result in starring and forking your repositories as long as I'm using GitHub.*

## How to start your own instance
1. Clone this repository and **keep it private**.
2. Find `@BotFather` contact in Telegram. Start and use `/newbot` command. Register new bot and save token (**KEEP IT SECRET**).
3. Get back to GitHub and save your token in code, 11th line. *Alternatively, there are ways to load your token into file. Discussed below.*
4. Create a [Heroku](https://dashboard.heroku.com/) account.
5. Create a new App with unique name. On `Settings` page in `Buildpack` choose Python.
6. On `Deploy` page link your Heroku account to Github account, choose your STEB repository and deploy it.
7. On `Resources` page activate worker.
8. Test your bot. It should work now.
9. If required, change `API/URL` and modify code accordingly.

### Loading token into file
You either can set up an .env at Heroku ([check manual](https://devcenter.heroku.com/articles/config-vars)) or load it locally, through a `JSON-mapping`, for example. Latter will require installing of [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and, **of course** addition of according `.gitignore` line. You will stage your bot directly from your local repository, so you won't need a GitHub linking to Heroku anymore.

## How to use
**Commands:**
- /start: tells about all existent commands;
- /lst: you type command -> bot tells you to type three-letter currency code -> you type it (e.g.: USD) -> bot shows result as a text;
- /exchange: you type command -> bot tells you to type three-letter currency code (twice) and provide amount, **using comas and spaces** -> you type it (e.g.: PLN, HUF, 150) -> bot shows result as a float;
- /history: you type command -> bot tells you to type three-letter currency code (twice), **using comas and spaces** -> you type it (e.g.: GBP, USD) -> bot shows result as a chart.

## Known issues
1. Bot will not instantly start working after deployment on Heroku, Matplotlib requires some build time. 
2. Sometimes there are more than two decimals points in the answer. Python is prone to it, but if it bothers you too much, modify the code.
3. History chart may become crowded (showing more than one currencies relation) if `plt.clf()`-line will not work for some reason.