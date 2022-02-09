
import random
import frame

class Sprite:

   sprite_dict = {}

   def __init__(self, key, buffer, fg_colour, text,
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

      self.key       = key
      self.buffer    = buffer 
      self.x, self.y = buffer.clip(x, y, wrap = False)
      self.fg_colour = fg_colour
      self.bg_colour = bg_colour
      self.text      = text
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
            self.height += 1
            x = 0
         else:
            x += 1
            if x > self.width:
               self.width = x
            if y > self.height:
               self.height = y

      if not key in Sprite.sprite_dict:
         Sprite.sprite_dict[key] = []
      Sprite.sprite_dict[key].append(self)

   def setVisibile(visible = True):
      ''' Change sprite visibility '''
      self.visible = visible

   def setSpeed(self, vx, vy):
      ''' Change sprite velocity '''
      self.vx = vx
      self.vy = vy
   
   def setPos(self, x, y):
      ''' Change sprite position '''
      self.x = x
      self.y = y

   def move(self, dx, dy, wrap = False):
      ''' Move the sprite '''
      x = self.x + dx
      y = self.y + dy
      x, y = self.buffer.clip(x, y, wrap)

      if x == self.x and y == self.y:
         return 'STUCK'

      self.inst += 1
      if self.inst == len(self.text):
         self.inst = 0
      self.num_moves += 1

      self.setPos(x, y)
      return self.hit(x, y)

   def integrate(self, wrap = False):
      ''' Move sprite according to it's velocity '''
      return self.move(self.vx, self.vy, wrap)

   def kill(self, dead_text = ' '):
      self.alive = False
      self.text  = [dead_text]
      self.inst  = 0

   def hit(self, x, y):
      for key in Sprite.sprite_dict:
         for s in Sprite.sprite_dict[key]:
            if s != self and x == s.x and y == s.y:
               return s
      return None

   @staticmethod
   def listGet(key):
      return Sprite.sprite_dict[key]


   @staticmethod
   def listCull():
      ''' Remove all the dead sprites '''
      for key in Sprite.sprite_dict:
          Sprite.sprite_dict[key] = [s for s in Sprite.sprite_dict[key] if s.alive]

   @staticmethod
   def redrawAll(buffer):
      buffer.clear()
      for key in Sprite.sprite_dict:
         for s in Sprite.sprite_dict[key]:
            if s.visible:
               buffer.plot(s.x, s.y, s.text[s.inst], s.fg_colour, s.bg_colour)
      buffer.redraw()
