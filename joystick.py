import shelltypes
import pygame
from time import time

#This is a stepping-stone class used to interact with the joystick as simply as possible before getting it hooked up to shell.py.
#Based on code found at https://www.pygame.org/docs/ref/joystick.html
#NOT ACTUALLY USED IN THE ROVER!

pygame.init()

#Initialize the joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()


name = joystick.get_name()
print(name)

numaxes = joystick.get_numaxes()
print("{} axes".format(numaxes))

buttons = []
numbuttons = joystick.get_numbuttons()
print("{} buttons".format(numbuttons))
for i in range(numbuttons):
    buttons.append(joystick.get_button(i))

numhats = joystick.get_numhats()
print("{} hats".format(numhats))

#Timer setup
lasttime=0
position_interval=1

# MAIN PROGRAM LOOP
while True:

    if time()-lasttime > position_interval:
        lasttime = time()
        print("JOYSTICK POSITION:\nFront/back: {:>6.3f}\nLeft/right: {:>6.3f}\nYaw: {:>6.3f}\nThrottle: {:>6.3f}".format(joystick.get_axis(1), joystick.get_axis(0), joystick.get_axis(3), joystick.get_axis(2)))
        for i in range(numhats):
            print("HAT {} POSITION: {}".format(i, str(joystick.get_hat(i))))

    for i in range(numbuttons):
        if buttons[i] == 0 and joystick.get_button(i) == 1:
            buttons[i] = 1
            print("Button {} pressed.".format(i))
        elif buttons[i] == 1 and joystick.get_button(i) == 0:
            buttons[i] = 0
            print("Button {} released.".format(i))

    # If you remove this line the code breaks. Don't ask me why
    for event in pygame.event.get(): ''''''

