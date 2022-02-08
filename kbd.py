import sys, tty, termios
import threading, queue

# Special values
UP      = 0x90
DOWN    = 0x91
LEFT    = 0x92
RIGHT   = 0x93
NOTHING = 0x00

class Spooler(threading.Thread):
   ''' A thread to wait for keyboard input '''

   def __init__(self):
      self.fd    = sys.stdin.fileno()
      self.attrs = termios.tcgetattr(self.fd)
      tty.setcbreak(self.fd)

      self.buffer = queue.Queue()

      threading.Thread.__init__(self, daemon = True)
      self.start()

   def __del__(self):
      termios.tcsetattr(self.fd, termios.TCSADRAIN, self.attrs)

   def run(self):
      while True:
         try:
            self.buffer.put(sys.stdin.read(1))
         except:
            break

   def get(self, timeout):
      try:
         return self.buffer.get(timeout=timeout)
      except:
         return NOTHING

# global state
spooler = Spooler()
state   = 0

def read(timeout = 0):
   ''' Unbuffered char read '''

   global state

   while True:
      ch = spooler.get(timeout)

      # Decode ANSI escape sequence for cursor keys
      if state == 0:
         if ch == '\033':
            state = 1
         else:
            return ch

      elif state == 1:
         state = 2 if ch == '[' else 0

      elif state == 2:
         state = 0
         if   ch == 'A': return UP
         elif ch == 'B': return DOWN
         elif ch == 'C': return RIGHT
         elif ch == 'D': return LEFT
