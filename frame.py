
# Colour constants
BLACK   = 0
RED     = 1
GREEN   = 2
YELLOW  = 3
BLUE    = 4
MAGENTA = 5
CYAN    = 6
WHITE   = 7

class Frame:
   ''' ANSI Terminal Frame Buffer '''

   def __init__(self, width, height, border = False):
      ''' Construct a new frame '''

      self.width  = width
      self.height = height

      if border:
         self.horz_border  = '+' + '-'*self.width + '+\n'
         self.left_border  = '|'
         self.right_border = '|\n'
      else:
         self.horz_border  = ''
         self.left_border  = ''
         self.right_border = '\n'

      self.frame = []
      for row in range(self.height):
         line = []
         for cell in range(self.width):
            line.append([' ', WHITE, BLACK])
         self.frame.append(line)

      printCursor(visible = False)
      printClear()
      self.redraw()

   def __del__(self):
      printCursor(visible = True)

   def clear(self, bg = BLACK):
      ''' Clear frame to empty '''
      for row in self.frame:
         for cell in row:
            cell[0] = ' '
            cell[1] = WHITE
            cell[2] = bg

   def plot(self, x, y, text, fg = WHITE, bg = BLACK):
      ''' Print text on the frame '''
      start_x = x
      for char in text:
         if char == '\n':
            x = start_x
            y += 1
         else:
            if x < 0 or x >= self.width or y < 0:
               continue
            if y >= self.height:
               break
            self.frame[y][x] = [char, fg, bg]
            x += 1

   def shout(self, colour, text):
      louder_text = ''
      for ch in text + ' !!!!':
         louder_text += ch + ' '
      x = (self.width - len(louder_text)) // 2
      self.plot(x, 10, louder_text, colour)
      self.redraw()

   def peek(self, x, y):
      ''' Peek contents of a frame position '''
      return self.frame[y][x][0]

   def clip(self, x, y, wrap):
      ''' clip (x, y) against frame size '''
      if x < 0:
         x = self.width - 1 if wrap else 0
      elif x >= self.width:
         x = 0 if wrap else self.width - 1
      if y < 0:
         y = self.height - 1 if wrap else 0
      elif y >= self.height:
         y = 0 if wrap else self.height - 1
      return x, y

   def redraw(self):
      ''' Redraw frame on the console '''
      printHome()
      printText(self.horz_border)
      for line in self.frame:
         printText(self.left_border)
         for cell in line:
            printText(cell[0], fg=cell[1], bg=cell[2])
         printText(self.right_border)
      printText(self.horz_border)

def printEsc(cmd):
   ''' Emit an escape sequence '''
   print('\033' + cmd, end='')

def printCursor(visible):
   ''' Control cursor visibility '''
   printEsc('[?25' + ('h' if visible else 'l'))

def printClear():
   ''' Clear console '''
   printEsc('[0;0H')
   printEsc('[0J')

def printFgColour(fg_colour):
   ''' Set the current foreground colour '''
   printEsc('[1;3'+str(fg_colour)+'m')
   global current_fg_colour
   current_fg_colour = fg_colour

def printBgColour(bg_colour):
   ''' Set the current background colour '''
   printEsc('[1;4'+str(bg_colour)+'m')
   global current_bg_colour
   current_bg_colour = bg_colour

def printHome():
   ''' Move cursor to top left corner '''
   printEsc('[0;0H')
   printFgColour(WHITE)
   printBgColour(BLACK)

def printText(text, fg = WHITE, bg = BLACK):
   ''' Print text with the specified colours '''
   if fg != current_fg_colour:
      printFgColour(fg)
   if bg != current_bg_colour:
      printBgColour(bg)
   print(text, end='')

# global state
current_fg_colour = WHITE
current_bg_colour = BLACK
