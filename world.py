import random

class World:
    key = {
        'S': -1,
        'B': 0,
        'G': 1,
        'W': 2,
        'F': 3,
    }
    keyReversed = {
        -1: 'S',
        0: 'B',
        1: 'G',
        2: 'W',
        3: 'F',
    }

    def __init__(self, path, player=None, bear=None, acts=(2, 3), killers=(-1, )):
        self.path = path
        self.playerLocation = player
        self.bearLocation = bear
        self.world = []

        self.playerSpawn = None
        self.bearSpawn = None

        self.score = 0
        self.previousAction = None

        self.actions = {i:set() for i in acts}
        self.killers = set(killers)

        self.load_world()
        self.load_actions()
        self.start_check()

    def load_world(self):
        with open(self.path, 'r') as file:
            lines = file.readlines()

        self.world.append([World.key['S'] for _ in range(len(lines[0].strip()) // 2 + 3)])
        self.world.append([World.key['S'] for _ in range(len(lines[0].strip()) // 2 + 3)])

        for ind, line in enumerate(lines[:-1], 1):
            self.world.insert(ind, [World.key['S']] + list(map(lambda key: World.key[key], line.split())) + [World.key['S']])

        try:
            if self.playerLocation is None:
                self.playerLocation = eval(lines[-1].split(' ')[0])
                self.playerSpawn = self.playerLocation

            if self.bearLocation is None:
                self.bearLocation = eval(lines[-1].split(' ')[1])
                self.bearSpawn = self.bearLocation
        except IndexError:
            raise ValueError(f'World file {self.path}\'s last line must contain \'(a,b) (c,d)\' specifying player '
                             f'and bear locations respectively if not provided.')

    def load_actions(self):
        for j in range(len(self.world)):
            for i in range(len(self.world[0])):
                if self.world[j][i] in self.actions.keys():
                    self.actions[self.world[j][i]].add((i, j))

    def start_check(self):
        if self.bearLocation == self.playerLocation:
            raise ValueError(f'Player spawn {self.playerSpawn} and bear spawn {self.bearSpawn} are the same.')

        if self.get_position_type() in self.actions.keys():
            self.score += 1
            self.previousAction = self.get_position_type()

        if self.playerLocation[0] in [0, len(self.world[0])] or self.playerLocation[1] in [0, len(self.world)]:
            raise ValueError(f'Player spawn {self.playerSpawn} out of playable bounds.')

    def move_bear(self):
        if abs(self.playerLocation[0] - self.bearLocation[0]) > abs(self.playerLocation[1] - self.bearLocation[1]):
            if self.playerLocation[0] > self.bearLocation[0]:
                self.bearLocation = (self.bearLocation[0] + 1, self.bearLocation[1])
            elif self.playerLocation[0] < self.bearLocation[0]:
                self.bearLocation = (self.bearLocation[0] - 1, self.bearLocation[1])
        else:
            if self.playerLocation[1] > self.bearLocation[1]:
                self.bearLocation = (self.bearLocation[0], self.bearLocation[1] + 1)
            elif self.playerLocation[1] < self.bearLocation[1]:
                self.bearLocation = (self.bearLocation[0], self.bearLocation[1] - 1)

        self.check_state()

    def move_player(self, move_dir=(0, 0)):
        if (move_dir[0] ** 2 + move_dir[1] ** 2 > 1
                or type(move_dir[0]) != int
                or type(move_dir[1]) != int
                or move_dir[0] and move_dir[1]):
            raise ValueError(f'Provided direction {move_dir} is invalid.')

        self.playerLocation = (self.playerLocation[0] + move_dir[0], self.playerLocation[1] - move_dir[1])
        self.calc_score()
        self.check_state()

    def get_position_type(self, letter=False):
        if letter:
            return World.keyReversed[self.world[self.playerLocation[1]][self.playerLocation[0]]]
        else:
            return self.world[self.playerLocation[1]][self.playerLocation[0]]

    def reset_world(self, player=None, bear=None, randomize_bear=False):
        if player is None:
            self.playerLocation = self.playerSpawn
        else:
            self.playerLocation = player

        if randomize_bear:
            spawnable = []

            for j in range(len(self.world)):
                for i in range(len(self.world[0])):
                    if (i - self.playerLocation[0]) ** 2 + (j - self.playerLocation[1]) ** 2 > 1:
                        spawnable.append((i, j))

            self.bearLocation = random.choice(spawnable)
        elif bear is None:
            self.bearLocation = self.bearSpawn
        else:
            self.bearLocation = bear

        self.score = 0
        self.previousAction = None

        self.start_check()

    def calc_score(self):
        if self.get_position_type() in self.actions.keys() and (self.get_position_type() != self.previousAction or self.previousAction is None):
            self.score += 1
            self.previousAction = self.get_position_type()

    def check_state(self):
        if self.get_position_type() in self.killers or self.playerLocation == self.bearLocation:
            self.reset_world()

    def __str__(self):
        out = f'world:\n{self.print_world(display=False)}\n'
        for key, value in self.__dict__.items():
            out += f'{key}: {value}\n' if key != 'world' else '\n'

        return out

    def print_world(self, display=True):
        if display:
            print('\n'.join([' '.join([World.keyReversed[j] for j in i]) for i in self.world]))
        else:
            return '\n'.join([' '.join([World.keyReversed[j] for j in i]) for i in self.world])
