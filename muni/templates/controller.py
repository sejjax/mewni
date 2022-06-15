class Controller:
    @command
    def start(self):
        name: str = ask('Send me your name')
        age: int = ask('Good. Now me need your age')

    @command
    def help(self):
        pass

    @startup
    def on_startup(self):
        pass