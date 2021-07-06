from stuff.player import Player

class Guild():
    def __init__(self, s_id):
        self.server_id = s_id
        self.profanity_setting = False
        self.blacklisted_words = [] 
        self.users = {}
        self.lotteries = {}
        self.active_games = {}
        self.awards = {"Gold": ["🏅", 50]}

    def get_playerobj(self, usr_id) -> Player:
        return self.users.get(usr_id)
    
    def get_lotteries(self, message_id):
        return self.lotteries.get(message_id)
    
    def set_psetting(self, booli):
        self.profanity_setting = booli

    def blacklist_word(self, word):
        added = False
        if word not in self.blacklisted_words:
            self.blacklisted_words.append(word) 
            added = True 
        return added
    
    def add_user(self, usr_id:str):
        added = False
        if self.users.get(usr_id) == None:
            self.users[usr_id] = Player(usr_id)
            added = True
        return added
    
    def add_lottery(self, mssg_id, time_end)->tuple:
        self.lotteries[mssg_id] = ([], time_end)

    def add_award(self, name, visual, price):
        if not self.awards.get(name):
            self.awards[name] = [visual, int(price)]
    
    def get_awards(self):
        return self.awards

class World():
    def __init__(self):
        self.guilds = {}
        self.active_lotteries = {}
    
    def add_guild(self, server_id):
        guild = Guild(server_id)
        self.guilds[server_id] = guild
    
    def get_guild(self, server_id) -> Guild:
        return self.guilds[server_id]

    def add_lottery(self, mssg_id:str,time_end,mssg_obj)->tuple:
        print(time_end)
        self.active_lotteries[mssg_id] = [[], time_end,mssg_obj]
    
    def get_lotteries(self) ->dict:
        return self.active_lotteries

    