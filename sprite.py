
import random
import frame

class Sprite:

   dict = {}

   def __init__(self, buffer, fg_colour, text,
                x = -1, y = -1, bg_colour = frame.BLACK):
      ''' Construct a new Sprite '''

      if x == -1 or y == -1:
         while True:
            if x == -1:
               x = random.randint(0, buffer.width  - 1)
            if y == -1:
               y = random.randint(0, buffer.height - 1)
            if buffer.peek(x, y) == ' ':
               break

      if not type(text) is list:
         text = [text]

      self.buffer    = buffer 
      self.x, self.y = buffer.clip(x, y, wrap = False)
      self.fg_colour = fg_colour
      self.bg_colour = bg_colour
      self.text      = text
      self.inst      = 0
      self.num_moves = 0
      self.life_span = 0
      self.alive     = True
      self.height    = 0
      self.width     = 0

      x = 0
      y = 0
      for ch in self.text[0]:
         if ch == '\n':
            self.height += 1
            x = 0
         else:
            x += 1
            if x > self.width:
               self.width = x
            if y > self.height:
               self.height = y

      # Add sprite to the dictionary
      key = self.id()
      if not key in Sprite.dict:
         Sprite.dict[key] = []
      Sprite.dict[key].append(self)

   def id(self):
      return self.__class__

   def setSpeed(self, vx, vy):
      ''' Change sprite velocity '''
      self.vx = vx
      self.vy = vy
   
   def setPos(self, x, y):
      ''' Change sprite position '''
      self.x = x
      self.y = y

   def setLifeSpan(self, n):
      ''' Set limited lifetime '''
      self.life_span = n

   def hit(self, x, y):
      for key in Sprite.dict:
         for s in Sprite.dict[key]:
            if s != self and x == s.x and y == s.y:
               return s
      return None

   def move(self, dx, dy, wrap = False):
      ''' Move the sprite '''

      self.num_moves += 1
      if self.num_moves == self.life_span:
         self.kill()

      x = self.x + dx
      y = self.y + dy
      x, y = self.buffer.clip(x, y, wrap)

      if x == self.x and y == self.y:
         self.moveBlocked()
         return

      target = self.hit(x, y)
      if target:
         if not self.moveHit(target):
            return

      self.inst += 1
      if self.inst == len(self.text):
         self.inst = 0

      self.setPos(x, y)

   def integrate(self, wrap = False):
      ''' Move sprite according to it's velocity '''
      return self.move(self.vx, self.vy, wrap)

   def kill(self, dead_text = ' '):
      self.alive = False
      self.text  = [dead_text]
      self.inst  = 0

   def moveBlocked(self):
      pass

   def moveHit(self, target):
      return True

   @staticmethod
   def listGet(key):
      ''' Get the list of sprites with the given key '''
      if key in Sprite.dict:
          return Sprite.dict[key]
      return []

   @staticmethod
   def listEmpty(key):
      ''' Check if any sprites of a type exist '''
      return Sprite.listGet(key) == []

   @staticmethod
   def redrawAll(buffer):
      ''' Redraw all the sprites on the frame buffer '''
      for key in Sprite.dict:
         Sprite.dict[key] = [s for s in Sprite.dict[key] if s.alive]
         for s in Sprite.dict[key]:
            buffer.plot(s.x, s.y, s.text[s.inst], s.fg_colour, s.bg_colour)

