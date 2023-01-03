import pygame as pg
from world import World
from color import colors

world = World('./test_level.txt')

pg.init()
pg.display.set_caption(world.path)
clock = pg.time.Clock()

FRAMERATE = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 896, 1152

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

bearCounter = 0
playerCounter = 0
frameCounter = 0

bearCooldown = FRAMERATE
playerCooldown = FRAMERATE / 10

switch = (-1000000, -1000000)

running = True
while running:
    '''
    if frameCounter % 10 == 0:
        print(f'Player location: {world.playerLocation}')
        print(f'Bear location: {world.bearLocation}')
        print(world.score)
    '''

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                running = False
            elif event.key == pg.K_LEFT and playerCounter == 0:
                world.move_player((-1, 0))
            elif event.key == pg.K_RIGHT and playerCounter == 0:
                world.move_player((1, 0))
            elif event.key == pg.K_UP and playerCounter == 0:
                world.move_player((0, 1))
            elif event.key == pg.K_DOWN and playerCounter == 0:
                world.move_player((0, -1))

            if event.key == pg.K_i:
                world.score += 1
            elif event.key == pg.K_o:
                world.score += 10
            elif event.key == pg.K_p:
                world.score *= 2

            if event.key == pg.K_c:
                temp = world.bearLocation
                world.bearLocation = switch
                switch = temp

            if playerCounter == 0:
                playerCounter = playerCooldown

    playerCounter -= 1 if playerCounter > 0 else 0

    if bearCounter > bearCooldown:
        world.move_bear()
        bearCounter = 0
    bearCounter += 1

    screen.fill(colors['Black'])

    for j in range(len(world.world)):
        for i in range(len(world.world[0])):
            pg.draw.rect(screen, colors[world.keyReversed[world.world[j][i]]], pg.Rect(i * 128, j * 128, 128, 128))

    score_display = [int(i) for i in bin(world.score)[2:]]
    for i in range(len(score_display)):
        if score_display[i]:
            pg.draw.rect(screen, colors['White'], pg.Rect(SCREEN_WIDTH - 64 * (len(score_display) - i + 1) + 32, 1056, 64, 64))

    pg.draw.rect(screen, colors['White'], pg.Rect(SCREEN_WIDTH - 64 * (len(score_display) + 1) + 22, 1046, 64 * len(score_display) + 20, 84), 10)
    pg.draw.rect(screen, colors['Player'], pg.Rect(world.playerLocation[0] * 128 + 32, world.playerLocation[1] * 128 + 32, 64, 64))
    pg.draw.rect(screen, colors['Bear'], pg.Rect(world.bearLocation[0] * 128 + 32, world.bearLocation[1] * 128 + 32, 64, 64))

    pg.display.flip()
    frameCounter += 1
    clock.tick(FRAMERATE)

pg.quit()
