import curses
from curses import textpad

import _thread
import threading
from time import sleep

vx = -25
vy = 5
score = '0000'

class Operation(threading.Timer):
    def __init__(self, *args, **kwargs):
        threading.Timer.__init__(self, *args, **kwargs)
        self.setDaemon(True)

    def run(self):
        while True:
            self.finished.clear()
            self.finished.wait(self.interval)
            if not self.finished.isSet():
                self.function(*self.args, **self.kwargs)
            else:
                return
            self.finished.set()

class Manager(object):

    ops = []

    def add_operation(self, operation, interval, args=[], kwargs={}):
        op = Operation(interval, operation, args, kwargs)
        self.ops.append(op)
        _thread.start_new_thread(op.run, ())

    def stop(self):
        for op in self.ops:
            op.cancel()
        self._event.set()


def main(stdscr):
    curses.curs_set(0)

    sh, sw = stdscr.getmaxyx()
    box = [[20,50], [sh-20, sw-50]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    paddle1 = [[52, sh//2], [52, sh//2 + 1], [52, sh//2 + 2], [52, sh//2 + 3], [52, sh//2 + 4]]
    wall = [[150, i] for i in range(21, 41)]

    ball = [sw//2+1, sh//2]

    coords = [[50, 19], [51, 19], [52, 19], [53, 19]]
    prev_paddle = []

    def move_ball():
        global vx
        global vy
        global score
        global prev_paddle

        if ball[1] + vy <= 21:
            ball[1] = 22
            vy = vy * -1

        if ball[1] + vy >= 41:
            ball[1] = 40
            vy = vy * -1

        # hit paddle 1
        if ball[0] + vx <= 52:
            if [52, ball[1]] in paddle1:
                score = str(int(score) + 1).rjust(4, '0')
                for j in range(len(coords)):
                    x,y = coords[j]
                    stdscr.addstr(y,x,score[j])

                stdscr.addstr(ball[1], ball[0], " ")
                ball.insert(0, 54)
                ball.pop(1)

                y_move = (((ball[0] + vx) - 52)/vx)*vy

                ball.insert(1, ball[1] + vy)
                ball.pop(2)

                stdscr.addstr(ball[1], ball[0], "•")

                change_y = paddle1[0][1] - prev_paddle[0][1]

                if change_y > vy:
                    vy += 1
                elif change_y < vy:
                    vy -= 1
                else:
                    vy = 0

                vx = -1 * vx
            else:
                msg = 'Game over! (press q to quit)'
                stdscr.addstr(sh//2, sw//2-len(msg)//2, msg)
                stdscr.nodelay(0)

                q = stdscr.getch()
                while q != 113:
                    q = stdscr.getch()
                
                exit(0)
        # hit paddle 2
        elif ball[0] + vx >= 150:
            stdscr.addstr(ball[1], ball[0], " ")
            ball.insert(0, 148)
            ball.pop(1)

            y_move = (((ball[0] + vx) - 52)/vx)*vy

            ball.insert(1, ball[1] + vy)
            ball.pop(2)

            stdscr.addstr(ball[1], ball[0], "•")

            vx = -1 * vx
        # no paddle hit
        else:
            stdscr.addstr(ball[1], ball[0], " ")
            ball.insert(0, ball[0] + vx)
            ball.pop(1)
            ball.insert(1, ball[1] + vy)
            ball.pop(2)
            stdscr.addstr(ball[1], ball[0], "•")

        prev_paddle = paddle1.copy()
        stdscr.refresh()

    for i in range(len(coords)):
        x,y = coords[i]
        stdscr.addstr(y,x,score[i])

    for x,y in paddle1:
        stdscr.addstr(y,x,"#")

    for x,y in wall:
        stdscr.addstr(y,x,"#")

    stdscr.addstr(ball[1], ball[0], "•")

    timer = Manager()
    timer.add_operation(move_ball, 0.5)

    while True:
        sleep(0.01)
        key = stdscr.getch()

       
        
        if key == 119 and paddle1[0][1] > 21:
            stdscr.addstr(paddle1[-1][1], paddle1[-1][0], ' ')
            paddle1.pop(len(paddle1) - 1)
            paddle1.insert(0, [paddle1[0][0], paddle1[0][1] - 1])
            stdscr.addstr(paddle1[0][1], paddle1[0][0], '#')

        if key == 115 and paddle1[0][1] < 36:
            stdscr.addstr(paddle1[0][1], paddle1[0][0], ' ')
            paddle1.pop(0)
            paddle1.insert(len(paddle1), [paddle1[-1][0], paddle1[-1][1] + 1])
            stdscr.addstr(paddle1[-1][1], paddle1[-1][0], '#')

        stdscr.refresh()

    msg = 'Game over! (press q to quit)'
    stdscr.addstr(sh//2, sw//2-len(msg)//2, msg)
    stdscr.nodelay(0)

    q = stdscr.getch()
    while q != 113:
        q = stdscr.getch()

    

if __name__ == '__main__':
    curses.wrapper(main)
