#!/usr/bin/env Python3

import random
import time

import kbd
import frame
from sprite import Sprite

# Game configuration
NUM_BOWMEN  = 10
WRAP_ARROWS = False
DEAD        = '#'

# Game data
PLAYER = 0
BOWMAN = 1
ARROW  = 2

# Game code
screen = frame.Frame(width = 50, height = 30)
player = Sprite(PLAYER, screen, frame.GREEN, 'S')

for _ in range(NUM_BOWMEN):
   Sprite(BOWMAN, screen, frame.CYAN, 'B')

cycle = 0

while True:

   screen.clear()
   Sprite.redrawAll(screen)
   screen.redraw()

   if not player.alive:
      screen.shout(frame.RED, 'YOU DIED')
      break

   k = kbd.read(timeout = 0.05)

   if k == kbd.UP:
      ok, hit = player.move(0, -1)
   elif k == kbd.DOWN:
      ok, hit = player.move(0, +1)
   elif k == kbd.LEFT:
      ok, hit = player.move(-1, 0)
   elif k == kbd.RIGHT:
      ok, hit = player.move(+1, 0)
   elif k == 'q':
      screen.shout(frame.YELLOW, 'BYE BYE')
      break
   else:
      ok, hit = True, None

   if ok and hit:
      if hit.key == BOWMAN:
         hit.kill(DEAD)
      elif hit.key == ARROW:
         player.kill(DEAD)

   cycle += 1
   if cycle < 5:
      continue
   cycle = 0

   for arrow in Sprite.listGet(ARROW):
      ok, hit = arrow.integrate(WRAP_ARROWS)
      if not ok or hit:
         arrow.kill()
         if hit:
            hit.kill(DEAD)

   Sprite.listCull()

   bowmen = Sprite.listGet(BOWMAN)

   if bowmen == []:
      screen.shout(frame.GREEN, 'YOU WIN')
      break

   bowman = random.choice(bowmen)
   vx     = random.randint(-1,1)
   vy     = random.randint(-1,1)
   if vx != 0 or vy != 0:
      arrow = Sprite(ARROW, screen, frame.RED, ['/', '|', '\\', '-'],
                     bowman.x + vx, bowman.y + vy)
      arrow.setSpeed(vx, vy)
      arrow.setLifeSpan(screen.height - 2)
