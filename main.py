import random
import curses
import time

#init
sc = curses.initscr()
h, w = sc.getmaxyx()
win = curses.newwin(h, w, 0, 0)
curses.noecho()
win.keypad(1)
curses.curs_set(0)

#Apple position
apple_position = [20, 20]

#snake 1
snake1_head = [10, 15]
snake1_position = [[15, 10], [14, 10], [13, 10]]
score1 = 0

prev_button_direction1 = 1
button_direction1 = 1
key1 = curses.KEY_RIGHT

#snake 2
snake2_head = [20, 20]
snake2_position = [[20, 20], [19, 20], [18, 20]]
score2 = 0

prev_button_direction2 = 0
button_direction2 = 0

# display apple
win.addch(apple_position[0], apple_position[1], curses.ACS_DIAMOND)


def collision_with_apple(score):
  apple_position = [random.randint(1, h - 2), random.randint(1, w - 2)]

  #check if snake 1 or 2 (scrap)
  score += 1
  return apple_position, score


def collision_with_boundaries(snake1_head):
  if snake1_head[0] >= h - 1 or snake1_head[0] <= 0 or snake1_head[
      1] >= w - 1 or snake1_head[1] <= 0:
    return 1
  else:
    return 0


def collision_with_boundaries(snake2_head):
  if snake2_head[0] >= h - 1 or snake2_head[0] <= 0 or snake2_head[
      1] >= w - 1 or snake2_head[1] <= 0:
    return 1
  else:
    return 0


def collision_with_self(snake1_position):
  snake1_head = snake1_position[0]
  if snake1_head in snake1_position[1:]:
    return 1
  else:
    return 0


def collision_with_self(snake2_position):
  snake2_head = snake2_position[0]
  if snake2_head in snake2_position[1:]:
    return 1
  else:
    return 0


def collision_with_opp(snake1_position, snake2_position):
  snake1_head = snake1_position[0]
  if snake1_head == snake2_position[1:]:
    return 1
  else:
    return 0


def collision_with_opp(snake2_position, snake1_position):
  snake2_head = snake2_position[0]

  if snake2_head in snake1_position[1:]:
    return 1
  else:
    return 0


a = []
key = 1
while True:
  win.border(0)
  win.timeout(100)
  win.addch(apple_position[0], apple_position[1], curses.ACS_DIAMOND)

  next_key = win.getch()

  if next_key == -1:
    key = key

  else:
    key = next_key
    key = chr(key)

    # 0-Left, 1-Right, 3-Up, 2-Down
    if key in 'Aa' and prev_button_direction2 != 1:
      button_direction2 = 0
    elif key in 'Dd' and prev_button_direction2 != 0:
      button_direction2 = 1
    elif key in 'Ww' and prev_button_direction2 != 2:
      button_direction2 = 3
    elif key in 'Ss' and prev_button_direction2 != 3:
      button_direction2 = 2
    else:
      pass

    key = next_key

    # 0-Left, 1-Right, 3-Up, 2-Down
    if key == curses.KEY_LEFT and prev_button_direction1 != 1:
      button_direction1 = 0

    elif key == curses.KEY_RIGHT and prev_button_direction1 != 0:
      button_direction1 = 1
    elif key == curses.KEY_UP and prev_button_direction1 != 2:
      button_direction1 = 3
    elif key == curses.KEY_DOWN and prev_button_direction1 != 3:
      button_direction1 = 2
    else:
      pass

  prev_button_direction2 = button_direction2
  prev_button_direction1 = button_direction1

  # Change the head position based on the button direction
  if button_direction1 == 1:
    snake1_head[1] += 1
  elif button_direction1 == 0:
    snake1_head[1] -= 1
  elif button_direction1 == 2:
    snake1_head[0] += 1
  elif button_direction1 == 3:
    snake1_head[0] -= 1

    #SNAKE 2
  if button_direction2 == 1:
    snake2_head[1] += 1
  elif button_direction2 == 0:
    snake2_head[1] -= 1
  elif button_direction2 == 2:
    snake2_head[0] += 1
  elif button_direction2 == 3:
    snake2_head[0] -= 1

  # Increase Snake length on eating apple SNAKE 1
  if snake1_head == apple_position:
    apple_position, score1 = collision_with_apple(score1)
    snake1_position.insert(0, list(snake1_head))
    a.append(apple_position)
    win.addch(apple_position[0], apple_position[1], curses.ACS_DIAMOND)
  else:
    snake1_position.insert(0, list(snake1_head))
    last = snake1_position.pop()
    win.addch(last[0], last[1], ' ')

  # Increase Snake length on eating apple SNAKE 2
  if snake2_head == apple_position:
    apple_position, score2 = collision_with_apple(score2)
    snake2_position.insert(0, list(snake2_head))
    a.append(apple_position)
    win.addch(apple_position[0], apple_position[1], curses.ACS_DIAMOND)
  else:
    snake2_position.insert(0, list(snake2_head))
    last = snake2_position.pop()
    win.addch(last[0], last[1], ' ')

  # display snake 1
  win.addch(snake1_position[0][0], snake1_position[0][1], '#')

  # display snake 2
  win.addch(snake2_position[0][0], snake2_position[0][1], '+')

  # On collision kill the snake 1
  if collision_with_boundaries(snake1_head) == 1 or collision_with_self(
      snake1_position) == 1:
    sc.addstr(10, 30, 'PLAYER 2 WINS(+)')
    break

  # On collision kill the snake 2
  if collision_with_boundaries(snake2_head) == 1 or collision_with_self(
      snake2_position) == 1:
    sc.addstr(10, 30, 'PLAYER 1 WINS (#)')
    break

  #slitherio kill snake 1
  if collision_with_opp(snake1_position, snake2_position) == 1:
    sc.addstr(10, 30, 'PLAYER 2 WINS (+)')
    break
  #slitherio kill snake 2
  if collision_with_opp(snake2_position, snake1_position) == 1:
    sc.addstr(10, 30, 'PLAYER 1 WINS (#)')
    break

sc.refresh()
time.sleep(2)
curses.endwin()
print(a)
print(w, h)
