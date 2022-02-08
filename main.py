#!/usr/bin/env Python3

import random
import time

import kbd
import frame
from sprite import Sprite

# Game configuration
PLAYER      = 'S'
BOWMAN      = 'B'
DEAD        = '#'
ARROW       = ['/', '|', '\\', '-']
NUM_BOWMEN  = 10
WRAP_ARROWS = False

# Game data
buffer = frame.Frame(width = 50, height = 30)
player = Sprite(buffer, frame.GREEN, PLAYER)
bowmen = []
arrows = []

for _ in range(NUM_BOWMEN):
   bowmen.append(Sprite(buffer, frame.CYAN, BOWMAN))

# The game
cycle = 0
while True:

   if not player.alive:
      buffer.shout(frame.RED, 'YOU DIED')
      break

   buffer.redraw()

   k = kbd.read(timeout = 0.05)

   hit = ' '
   if k == kbd.UP:
      hit = player.move(0, -1)
   elif k == kbd.DOWN:
      hit = player.move(0, +1)
   elif k == kbd.LEFT:
      hit = player.move(-1, 0)
   elif k == kbd.RIGHT:
      hit = player.move(+1, 0)

   if hit == BOWMAN:
      Sprite.listKillAt(bowmen, player.x, player.y, DEAD)
   elif hit == ARROW:
      player.kill(DEAD)

   cycle += 1
   if cycle < 5:
      continue
   cycle = 0

   for arrow in arrows:
      if arrow.num_moves == (buffer.height - 2):
         arrow.kill()
      else:
         hit = arrow.integrate(WRAP_ARROWS)
         if hit == PLAYER:
            player.kill(DEAD)
         elif hit == BOWMAN:
            Sprite.listKillAt(bowmen, arrow.x, arrow.y, DEAD)
         elif hit == 'STUCK':
            arrow.kill()

   bowmen = Sprite.listRemoveTheDead(bowmen)
   arrows = Sprite.listRemoveTheDead(arrows)

   if bowmen == []:
      buffer.shout(frame.GREEN, 'YOU WIN')
      break

   bowman = random.choice(bowmen)
   vx     = random.randint(-1,1)
   vy     = random.randint(-1,1)
   if vx != 0 or vy != 0:
      arrow = Sprite(buffer, frame.RED, ARROW,
                     bowman.x + vx, bowman.y + vy)
      arrow.setSpeed(vx, vy)
      arrows.append(arrow)
