# Muni is the python telegram bot framework 

## How you can start?
Just run `pip3 install muni` to install package.

Run `ni init superbot` to initialize new bot.

## Tasks
- [ ] Implement method `ask()` which send to user request with question and return value which send user back
- [ ] Implement method `select(message: str, enum: Enum)` which send a message with selection and return option of enum and map selected option to value
- [ ] Implement `LocalStorage()` with the same syntax `name, email, age = LocalStore()` which create storage for each user. For implementation need to use python AST.
- [ ] Make architecture for this project
- [ ] Refactor all project
- [ ] Make documentation better
- [ ] Make errors better
- [ ] Make using Config class from project for type auto complete
- [ ] Add code formatter - black
- [ ] Set name to "bot" folder the same as project
- [ ] Make plugin system
- [ ] Add Template renderer
- [ ] Add @startup, @stop decorators
- [ ] Add @on_message decorator
- [ ] Add the ability to work with inline query
- [ ] Add checking for existence value in .env file. If value is not defined then raise error
- [ ] Colorize output
- [ ] Make beautiful serve message
- [ ] Add the ability to adding other threads to app
- [ ] Add @middleware decorator
- [ ] Add @filter decorator
- [ ] Add questions to init project command
- [ ] Add auto db injection to peewee models
- [ ] Change every event syntax
- [ ] Implement overwrite default /help command text and reaction for it
- [ ] Add logging with structuring for years, month and days
- [ ] Buy website for muni project
- [ ] Make additional cli commands:
  - [ ] generate - generate something project items
  - [ ] start - start server
  - [ ] dev - start server with auto reloading
  - [ ] build - compile all project to one .pyc file
  - [ ] deploy - deploy bot to muni server
  - [ ] auth - authorize for muni server for deploy
- [ ] Implement plugins:
  - [ ] Role plugin
  - [ ] Admin plugin
  - [ ] Analytic plugin
  - [ ] Payment plugin
- [ ] Add notification about startup and stopping for bot admins
- [ ] Detach Muni from specific service (Telegram) and make it universe:
  - [ ] Telegram
  - [ ] WhatsApp
  - [ ] Discord
  - [ ] Github
  - [ ] Twitter and others social networks
- [ ] Draw logotype for Muni project
- [ ] Add choosing between requirements.txt and pyproject.toml files (poetry and pip options) 