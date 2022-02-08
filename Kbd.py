import sys, tty, termios
import threading, queue

UP      = 0x90
DOWN    = 0x91
LEFT    = 0x92
RIGHT   = 0x93
NOTHING = 0x00

# global state
buffer = None
state  = 0

def read(timeout = 0):
  ''' Unbuffered char read '''

  global buffer, state

  def readKeyPress():
    fd    = sys.stdin.fileno()
    attrs = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    while True:
        try:
          buffer.put(sys.stdin.read(1))
        except:
          break
    termios.tcsetattr(fd, termios.TCSADRAIN, attrs)

  if not buffer:
    buffer = queue.Queue()
    threading.Thread(target=readKeyPress, daemon=True).start()

  while True:
    try:
      ch = buffer.get(timeout=timeout)
    except:
      return NOTHING

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
