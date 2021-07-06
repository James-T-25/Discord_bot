class Player:
    def __init__(self, user_id):
        self.u_id = user_id
        self.server_merit = 0
        self.awards = {}
    
    def add_merit(self, pts: int):
        self.server_merit += pts
    
    def get_server_merit(self) -> int:
        return self.server_merit
    
    def add_award(self, name, visual):
        award = self.awards.get(name)
        if award:
            award[1] += 1
        else:
            self.awards[name] = [visual, 1]
    
    def get_awards(self):
        return self.awards
    
