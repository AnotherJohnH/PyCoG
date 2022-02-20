import random
import frame

class Sprite:

    dict = {}

    def __init__(self, text, fg_colour, x = 0, y = 0):
        ''' Construct a new Sprite '''

        # Add sprite to the dictionary
        key = self.id()
        if not key in Sprite.dict:
            Sprite.dict[key] = []
        Sprite.dict[key].append(self)

        self.text      = text if type(text) is list else [text]
        self.fg_colour = fg_colour
        self.bg_colour = frame.BLACK
        self.x, self.y = x, y

        self.num_move  = 0
        self.width     = 0
        self.height    = 0
        self.alive     = True

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

    def id(self):
        return self.__class__

    def setPos(self, x, y):
        ''' Change sprite position '''
        self.x = x
        self.y = y

    def setRandomPos(self, buffer):
        ''' Change sprite position to a random place '''
        while True:
           x = random.randint(0, buffer.width - 1)
           y = random.randint(0, buffer.height - 1)
           if buffer.peek(x, y) == ' ':
              break
        self.setPos(x, y)

    def setSpeed(self, vx, vy):
        ''' Change sprite velocity '''
        self.vx = vx
        self.vy = vy

    def hit(self, x, y):
        for key in Sprite.dict:
            for s in Sprite.dict[key]:
                if s != self and x == s.x and y == s.y:
                    return s
        return None

    def move(self, dx, dy, wrap=False):
        ''' Move the sprite '''

        x = self.x + dx
        y = self.y + dy

        if x == self.x and y == self.y:
            self.moveBlocked()
            return

        target = self.hit(x, y)
        if target:
            if not self.moveHit(target):
                return

        self.num_move += 1

        self.setPos(x, y)

    def integrate(self, wrap=False):
        ''' Move sprite according to it's velocity '''
        return self.move(self.vx, self.vy, wrap)

    def kill(self, dead_text=' '):
        self.alive = False
        self.text = [dead_text]

    def spriteUpdate(self):
        pass

    def moveBlocked(self):
        pass

    def moveHit(self, target):
        return True

    @staticmethod
    def listClearAll():
        Sprite.dict = {}

    @staticmethod
    def listGet(key):
        ''' Get the list of sprites with the given key '''
        return Sprite.dict[key] if key in Sprite.dict else []

    @staticmethod
    def listEmpty(key):
        ''' Check if any sprites of a type exist '''
        return Sprite.listGet(key) == []

    @staticmethod
    def redrawAll(buffer):
        ''' Redraw all the sprites on the frame buffer '''
        for key in Sprite.dict:

            for s in Sprite.dict[key]:
                s.spriteUpdate()

            # Garbage collect
            Sprite.dict[key] = [s for s in Sprite.dict[key] if s.alive]

            for s in Sprite.dict[key]:
                i = s.num_move % len(s.text)
                buffer.plot(s.x, s.y, s.text[i], s.fg_colour, s.bg_colour)
