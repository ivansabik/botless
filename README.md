# botless
Serverless bot framework for automating tasks from external applications (like GMail, Slack, Toggl, Github, etc). Basically it provides developers with tools to build their own bots using predefined actions and automate the scheduling and running part using the AWS serverless stack. Inspired by the following projects:

- [Zapier](https://zapier.com/)
- [Huginn](https://github.com/huginn/huginn)
- [IFTTT](https://ifttt.com)

A key difference is that for now botless is intended to provide a framework and tools used to developers or people who know how to code in Python.

## App Integrations
- Amazon S3
- GitHub
- GMail
- Google Spreadsheets
- Slack
- Toogle

## Bots
Bots are workflows that can be run on a schedule or based on a trigger (webhook). Bots are composed of different actions that can take in variable arguments or parameters.

Examples:
 - Get number of hours registered in Toggl and alert to a slack channel the users that have less than a certain amount of hours
 - Get detailed reports from Toggl and put in a Google Spreadsheet
 - Get information from GitHub (Pull Requests in a list of repositories, Issue Comments in a list of repositories, Commits in a list of repositories) and put as CSV in an S3 bucket

## Installation in AWS
 1. Install virtualenv, create new virtualenv and activate it
 2. Install AWS cli and make sure its configured properly (try `aws sts get-caller-identity`), you'll need permissions to create lambdas among other stuff
 3. Install deployment requirements `pip install -r requirements/deploy.txt`
 4. Set your configuration values like api keys, account IDs, etc. in a file named `zappa_settings.json`
 5. Deploy with `zappa deploy mybots`


## Installation for local development
1. Install virtualenv, create new virtualenv and activate it
2. Install deployment requirements `pip install -r requirements/dev.txt`
3. Set your configuration values like api keys, account IDs, etc. in a file named `.env`
