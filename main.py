import pygame as pg
from world import World
from color import colors

world = World('./test_level.txt')

pg.init()
pg.display.set_caption(world.path)
clock = pg.time.Clock()

FRAMERATE = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

bearCounter = 0
playerCounter = 0

bearCooldown = FRAMERATE * 2
playerCooldown = FRAMERATE / 2

running = True
while running:
    print(f'Player location: {world.playerLocation}')
    #print(f'Bear location: {world.bearLocation}')

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            #print(f'KEYDOWN event: {event.key}')

            if event.key == pg.K_LEFT and playerCounter == 0:
                world.move_player((-1, 0))
            elif event.key == pg.K_RIGHT and playerCounter == 0:
                world.move_player((1, 0))
            elif event.key == pg.K_UP and playerCounter == 0:
                world.move_player((0, 1))
            elif event.key == pg.K_DOWN and playerCounter == 0:
                world.move_player((0, -1))

            playerCounter = playerCooldown

    playerCounter -= 1 if playerCounter > 0 else 0

    if bearCounter > bearCooldown:
        world.move_bear()
        bearCounter = 0
    bearCounter += 1

    pg.draw.rect(screen, colors[world.get_position_type()], pg.Rect(SCREEN_WIDTH / 2 - 16, SCREEN_HEIGHT / 2 - 16, 32, 32))

    pg.display.flip()
    clock.tick(FRAMERATE)

pg.quit()
