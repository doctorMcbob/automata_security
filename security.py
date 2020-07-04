from random import randint
import automata as atoma

class SecurityHandler(object):
    def __init__(self, send_function, steps=50):
        # "user name" : key (integer)
        self.USER_KEYS = {}

        # "user name" : (sent integer, expected response)
        self.CONNECTIONS = {}
        self.send = send_function

        self.steps = steps

    def new_key(self): return randint(0, 2**256)

    def new_user(self, user):
        if user not in self.USER_KEYS:
            key = self.new_key()
            self.USER_KEYS[user] = key
            self.send(user, key)

    def start_connection(self, user):
        if user not in self.USER_KEYS:
            self.new_user(user)
            

        grid = atoma.fresh_start()
        n = atoma.reduce_to_int(grid)
        self.send(user,  n)
        for _ in range(self.steps):
            grid = atoma.apply_rule(self.USER_KEYS[user], grid)
        n2 = atoma.reduce_to_int(grid)
        self.CONNECTIONS[user] = (n, n2)

    def resolve_connection(self, user, response):
        if (user not in self.USER_KEYS or
            user not in self.CONNECTIONS):
            return False

        if response == self.CONNECTIONS[user][1]:
            self.CONNECTIONS.pop(user)
            grid = atoma.undo_reduce(response)
            for _ in range(self.steps):
                grid = atoma.apply_rule(self.USER_KEYS[user], grid)
            new = atoma.reduce_to_int(grid)
            self.CONNECTIONS[user] = (response, new)
            return True
        
        return False

