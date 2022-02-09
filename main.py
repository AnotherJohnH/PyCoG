#!/usr/bin/env Python3

import random

import kbd, frame
from sprite import Sprite

# Game configuration
NUM_BOWMEN  = 10
WRAP_ARROWS = False
DEAD        = '#'

class Player(Sprite):
   def __init__(self):
      Sprite.__init__(self, screen, frame.GREEN, 'S')

   def moveHit(self, target):
      if target.id() == Bowman:
         target.kill(DEAD)
      elif target.id() == Arrow:
         self.kill(DEAD)


class Bowman(Sprite):
   def __init__(self):
      Sprite.__init__(self, screen, frame.CYAN, 'B')


class Arrow(Sprite):
   def __init__(self, source):
      while True:
         vx = random.randint(-1,1)
         vy = random.randint(-1,1)
         if vx != 0 or vy !=0:
            Sprite.__init__(self, screen,
                            source.fg_colour,
                            ['/', '|', '\\', '-'],
                            source.x + vx, source.y + vy)
            self.setLifeSpan(screen.height - 2)
            self.setSpeed(vx, vy)
            break

   def moveBlocked(self):
      self.kill()

   def moveHit(self, target):
      self.kill()
      target.kill(DEAD)


# Game code
screen = frame.Frame(width = 50, height = 30)
player = Player()
for _ in range(NUM_BOWMEN):
   Bowman()

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
      player.move(0, -1)
   elif k == kbd.DOWN:
      player.move(0, +1)
   elif k == kbd.LEFT:
      player.move(-1, 0)
   elif k == kbd.RIGHT:
      player.move(+1, 0)
   elif k == 'f':
      Arrow(player)
   elif k == 'q':
      screen.shout(frame.YELLOW, 'Bye Bye')
      break

   cycle += 1
   if cycle < 5:
      continue
   cycle = 0

   for arrow in Sprite.listGet(Arrow):
      arrow.integrate(WRAP_ARROWS)

   if Sprite.listEmpty(Bowman):
      screen.shout(frame.GREEN, 'YOU WIN')
      break

   bowman = random.choice(Sprite.listGet(Bowman))
   Arrow(bowman)
