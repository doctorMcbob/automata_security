import unittest

from automata import *
from security import *
from random import randint


class AutomataTest(unittest.TestCase):
    def test_to_binary_and_back(self):
        n = randint(0, 256)
        print("randint :", n)
        b = tobin(n, 8)
        print("to bin :", b)
        n2 = int(b, 2)
        print("back to int :", n2)
        self.assertEqual(n, n2)

    def test_reduce_and_undo(self):
        print("Generating Grid...")
        grid = fresh_start()
        print("Done.")
        
        print("Reducing to int...")
        n = reduce_to_int(grid)
        print("Done")
        
        print("Converting back into grid...")
        grid2 = undo_reduce(n)
        print("Done")
        
        self.assertEqual(grid, grid2)


class SecurityTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(SecurityTest, self).__init__(*args, **kwargs)
        self.log = []
        def dummy_send(*args): self.log.append(args)
        self.handler = SecurityHandler(dummy_send)

    def test0_new_users(self):
        print("Testing new user")
        self.handler.new_user("Jason")
        print("added Jason")
        assert "Jason" in self.handler.USER_KEYS
        key = self.handler.USER_KEYS["Jason"]
        self.handler.new_user("Jason")
        key2 = self.handler.USER_KEYS['Jason']
        assert key == key2

    def test1_start_connection(self):
        print("Testing start connection")
        print("Starting Jason")
        self.handler.start_connection("Jason")
        print("Starting Sally")
        self.handler.start_connection("Sally")
        print("Starting Bobby")
        self.handler.start_connection("Bobby")
        for name in ["Jason", "Sally", "Bobby"]:
            self.assertTrue( name in self.handler.USER_KEYS )
            self.assertTrue( name in self.handler.CONNECTIONS )

    def test2_resolve(self):
        print("Testing resolve connection")
        print("Starting Jason")
        self.handler.start_connection("Jason")
        print("Starting Sally")
        self.handler.start_connection("Sally")
        print("Starting Bobby")
        self.handler.start_connection("Bobby")
        
        for user, data in self.log:
            if data == self.handler.USER_KEYS[user]:
                continue
            print("Testing user: ", user)
            rule = self.handler.USER_KEYS[user]
            rule2 = rule + 1
            grid = undo_reduce(data)
            grid2 = grid.copy()

            print("trying with wrong data")
            self.assertFalse(self.handler.resolve_connection(user, data))
            print("Done")

            print("running rule...")
            for _ in range(self.handler.steps):
                grid = apply_rule(rule, grid)
            response = reduce_to_int(grid)

            print("running wrong rule...")
            for _ in range(self.handler.steps):
                grid2 = apply_rule(rule2, grid2)
            response2 = reduce_to_int(grid2)

            print("Trying following wrong rule")
            self.assertFalse(self.handler.resolve_connection(user, response2))
            print("Done")
            print("Trying following right rule")
            self.assertTrue(self.handler.resolve_connection(user, response))
            print("Done")

            print("running rule...")
            for _ in range(self.handler.steps):
                grid = apply_rule(rule, grid)
            response = reduce_to_int(grid)

            print("Trying following right rule, second time")
            self.assertTrue(self.handler.resolve_connection(user, response))
            print("Done")
if __name__ == """__main__""":
    unittest.main()
