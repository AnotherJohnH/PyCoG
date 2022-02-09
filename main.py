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

buffer = frame.Frame(width = 50, height = 30)
player = Sprite(PLAYER, buffer, frame.GREEN, 'S')

for _ in range(NUM_BOWMEN):
   Sprite(BOWMAN, buffer, frame.CYAN, 'B')

cycle = 0

# The game
while True:

   if not player.alive:
      buffer.shout(frame.RED, 'YOU DIED')
      break

   buffer.clear()
   Sprite.redrawAll(buffer)
   buffer.redraw()

   k = kbd.read(timeout = 0.05)

   if k == kbd.UP:
      hit = player.move(0, -1)
   elif k == kbd.DOWN:
      hit = player.move(0, +1)
   elif k == kbd.LEFT:
      hit = player.move(-1, 0)
   elif k == kbd.RIGHT:
      hit = player.move(+1, 0)
   elif k == 'q':
      buffer.shout(frame.YELLOW, 'BYE BYE')
      break
   else:
      hit = None

   if hit and hit != "STUCK":
      if hit.key == BOWMAN:
         hit.kill(DEAD)
      elif hit.key == ARROW:
         player.kill(DEAD)

   cycle += 1
   if cycle < 5:
      continue
   cycle = 0

   for arrow in Sprite.listGet(ARROW):
      if arrow.num_moves == (buffer.height - 2):
         arrow.kill()
      else:
         hit = arrow.integrate(WRAP_ARROWS)
         if hit == 'STUCK':
            arrow.kill()
         elif hit:
            hit.kill(DEAD)

   Sprite.listCull()

   bowmen = Sprite.listGet(BOWMAN)

   if bowmen == []:
      buffer.shout(frame.GREEN, 'YOU WIN')
      break

   bowman = random.choice(bowmen)
   vx     = random.randint(-1,1)
   vy     = random.randint(-1,1)
   if vx != 0 or vy != 0:
      arrow = Sprite(ARROW, buffer, frame.RED, ['/', '|', '\\', '-'],
                     bowman.x + vx, bowman.y + vy)
      arrow.setSpeed(vx, vy)