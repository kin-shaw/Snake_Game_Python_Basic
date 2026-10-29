import random
import curses
import time

s=curses.initscr()
curses.curs_set(0)
sh,sw=s.getmaxyx()

w=curses.newwin(sh,sw,0,0)
w.keypad(1)
w.timeout(100)

snk_x=int(3*sw/4)
snk_y=int(sh/2)
snake=[
    [snk_y,snk_x],
    [snk_y,snk_x+1],
    [snk_y,snk_x+2]
]

food1=[random.randint(1,sh-2), random.randint(1,sw-2)]
w.addch(food1[0],food1[1],curses.ACS_DIAMOND)

food2=[random.randint(1,sh-2), random.randint(1,sw-2)]
w.addch(food2[0],food2[1],curses.ACS_DIAMOND)

key=curses.KEY_LEFT
cnt=0
score=0

PI_TIME_LIMIT = 7 
food1_is_pi = food2_is_pi = False
food1_expires_at = food2_expires_at = None

while True:
    next_key=w.getch()
    key=key if next_key==-1 else next_key

    new_head=[snake[0][0],snake[0][1]]

    if key==curses.KEY_DOWN:
        new_head[0]+=1
    if key==curses.KEY_UP:
        new_head[0]-=1
    if key==curses.KEY_LEFT:
        new_head[1]-=1
    if key==curses.KEY_RIGHT:
        new_head[1]+=1

    if (
        new_head[0] <= 0
        or new_head[0] >= sh - 1
        or new_head[1] <= 0
        or new_head[1] >= sw - 1
        or new_head in snake[:-1]
    ):
        break

    snake.insert(0,new_head)

    if snake[0]==food1: 
                 if(cnt%4==0 and cnt!=0):
                       cnt+=1
                       score+=5
                       food1=None
                       while food1 is None:
                            nf1=[random.randint(1,sh-2), random.randint(1,sw-2)]
                            food1=nf1 if nf1 not in snake else None
                       food1_is_pi = True
                       food1_expires_at = time.monotonic() + PI_TIME_LIMIT
                       w.addch(food1[0], food1[1], curses.ACS_PI)
                 else:
                    cnt+=1
                    score+=1
                    food1= None
                    while food1 is None:
                       nf1=[random.randint(1,sh-2), random.randint(1,sw-2)]
                       food1=nf1 if nf1 not in snake else None
                    food1_is_pi = False
                    food1_expires_at = None
                    w.addch(food1[0],food1[1],curses.ACS_DIAMOND)
    elif snake[0]==food2:
                 if(cnt%4==0 and cnt!=0):
                    cnt+=1
                    score+=5
                    food2=None
                    while food2 is None:
                       nf2=[random.randint(1,sh-2), random.randint(1,sw-2)]
                       food2=nf2 if nf2 not in snake else None
                    food2_is_pi = True
                    food2_expires_at = time.monotonic() + PI_TIME_LIMIT
                    w.addch(food2[0], food2[1], curses.ACS_PI)
     
                 else: 
                   cnt+=1
                   score+=1
                   food2= None
                   while food2 is None:
                     nf2=[random.randint(1,sh-2), random.randint(1,sw-2)]
                     food2=nf2 if nf2 not in snake else None
                   food2_is_pi = False
                   food2_expires_at = None
                   w.addch(food2[0],food2[1],curses.ACS_DIAMOND)
    else: 
             tail=snake.pop()
             w.addch(tail[0],tail[1], ' ')
    now = time.monotonic()

    if food1_is_pi and food1_expires_at is not None and now >= food1_expires_at:
      w.addch(food1[0], food1[1], curses.ACS_DIAMOND)
      score-=4
      food1_is_pi = False
      food1_expires_at = None

    if food2_is_pi and food2_expires_at is not None and now >= food2_expires_at:
      w.addch(food2[0], food2[1], curses.ACS_DIAMOND)
      score-=4
      food2_is_pi = False
      food2_expires_at = None

    w.addch(snake[0][0],snake[0][1],curses.ACS_CKBOARD)

curses.endwin()
print("Game Over! Your score is:", score)
