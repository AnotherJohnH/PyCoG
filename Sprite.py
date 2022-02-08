
import random
from Frame import Frame

class Sprite:

  def __init__(self, frame, fg_colour, text,
               x = -1, y = -1, bg_colour = Frame.BLACK):
    ''' Construct a new Sprite '''

    if x == -1 or y == -1:
      while True:
        if x == -1:
          x = random.randint(0, frame.width  - 1)
        if y == -1:
          y = random.randint(0, frame.height - 1)
        if frame.peek(x, y) == ' ':
          break

    if not type(text) is list:
       text = [text]

    self.frame     = frame
    self.x, self.y = frame.clip(x, y, wrap = False)
    self.fg_colour = fg_colour
    self.bg_colour = bg_colour
    self.fr_colour = Frame.BLACK
    self.text      = text
    self.untext    = ''
    self.inst      = 0
    self.num_moves = 0
    self.visible   = True
    self.alive     = True

    self.height    = 0
    self.width     = 0
    x = 0
    y = 0
    for ch in self.text[0]:
      if ch == '\n':
        self.untext += '\n'
        self.height += 1
        x = 0
      else:
        self.untext += ' '
        x += 1
        if x > self.width:
          self.width = x
        if y > self.height:
          self.height = y

    self.plot()

  def plot(self):
    ''' Plot the sprite '''
    self.frame.plot(self.x, self.y,    
                    self.fg_colour,
                    self.text[self.inst], self.bg_colour)

  def erase(self, bg_colour = Frame.BLACK):
    ''' Erase the sprite '''
    self.frame.plot(self.x, self.y,
                    self.fg_colour,
                    self.untext, self.fr_colour)

  def setVisibile(visible = True):
    ''' Change sprite visibility '''
    self.visible = visible
    if self.visible:
      self.plot()
    else:
      self.erase()

  def setSpeed(self, vx, vy):
    ''' Change sprite velocity '''
    self.vx = vx
    self.vy = vy
  
  def setPos(self, x, y):
    ''' Change sprite position '''
    if self.visible:
      self.erase()
    self.x = x
    self.y = y
    if self.visible:
      self.plot()

  def move(self, dx, dy, wrap = False):
    ''' Move the sprite '''
    x = self.x + dx
    y = self.y + dy
    x, y = self.frame.clip(x, y, wrap)

    if x == self.x and y == self.y:
      return 'STUCK'

    self.inst += 1
    if self.inst == len(self.text):
      self.inst = 0
    self.num_moves += 1

    prev = self.frame.peek(x, y)
    self.setPos(x, y)
    return prev

  def integrate(self, wrap = False):
    ''' Move sprite according to it's velocity '''
    return self.move(self.vx, self.vy, wrap)

  def kill(self, dead_text = ' '):
    self.alive = False
    self.text  = [dead_text]
    self.inst  = 0
    self.plot()

  @staticmethod
  def listKillAt(list_of_sprites, x, y, dead_text = ' '):
    for sprite in list_of_sprites:
      if sprite.x == x and sprite.y == y:
          sprite.kill(dead_text)
 
  @staticmethod
  def listRemoveTheDead(list_of_sprites):
    return [sprite for sprite in list_of_sprites if sprite.alive]