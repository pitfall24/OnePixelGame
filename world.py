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

    def __init__(self, path, player=None, bear=None):
        self.path = path
        self.playerLocation = player
        self.bearLocation = bear
        self.world = []

        self.load_world()

    def load_world(self):
        with open(self.path, 'r') as file:
            lines = file.readlines()

        self.world.append([World.key['S'] for _ in range(7)])
        self.world.append([World.key['S'] for _ in range(7)])

        for ind, line in enumerate(lines[:-1], 1):
            self.world.insert(ind, [World.key['S']] + list(map(lambda key: World.key[key], line.split())) + [World.key['S']])

        try:
            if self.playerLocation is None:
                self.playerLocation = eval(lines[-1].split(' ')[0])

            if self.bearLocation is None:
                self.bearLocation = eval(lines[-1].split(' ')[1])
        except IndexError:
            raise ValueError(f'World file {self.path}\'s last line must contain \'(a,b) (c,d)\' specifying player '
                             f'and bear locations respectively if not provided.')

    def move_bear(self):
        if abs(self.playerLocation[0] - self.bearLocation[0]) > abs(self.playerLocation[1] - self.bearLocation[1]):
            if self.playerLocation[0] > self.bearLocation[0]:
                self.bearLocation = (self.bearLocation[0] + 1, self.bearLocation[1])
            else:
                self.bearLocation = (self.bearLocation[0] - 1, self.bearLocation[1])
        else:
            if self.playerLocation[1] > self.bearLocation[1]:
                self.bearLocation = (self.bearLocation[0], self.bearLocation[1] + 1)
            else:
                self.bearLocation = (self.bearLocation[0], self.bearLocation[1] - 1)

    def move_player(self, move_dir=(0, 0)):
        if (move_dir[0] ** 2 + move_dir[1] ** 2 > 1
                or type(move_dir[0]) != int
                or type(move_dir[1]) != int
                or move_dir[0] and move_dir[1]):
            raise ValueError(f'Provided direction {move_dir} is invalid.')

        self.playerLocation = (self.playerLocation[0] + move_dir[0], self.playerLocation[1] + move_dir[1])

    def __str__(self):
        out = f'world:\n{self.print_world(display=False)}\n'
        for key, value in self.__dict__.items():
            out += f'{key}: {value}\n' if key != 'world' else '\n'

        return out

    def get_position_type(self):
        return World.keyReversed[self.world[self.playerLocation[1]][self.playerLocation[0]]]

    def print_world(self, display=True):
        if display:
            print('\n'.join([' '.join([World.keyReversed[j] for j in i]) for i in self.world]))
        else:
            return '\n'.join([' '.join([World.keyReversed[j] for j in i]) for i in self.world])
