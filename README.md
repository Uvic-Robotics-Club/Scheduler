# Scheduler
The new central software.

This readme is currently a rough outline for Greg and Andrew's scheme to replace ROS in the UVic Robotics Rover.

We are ditching ROS because of many reasons including the steep learning curve, its incompatibility with Windows, and its inability to teach transferable skills to new recruits.

The new scheme will be written in Python and C++, with a central Python threading mechanism.

Rather than having ROS subscribers and publishers, methods will be called when data comes which put tasks into the priority queue ("published")

SHELL.PY would run basically everything; it is replacing "roscore"
It's also where the threading magic happens

Thread 1: communication
  Mostly for inputs. When given something by an Arduino or the phone, it converts that input into a task for Thread 2
Thread 2: Priority Queue of tasks
  Tasks being custom objects holding function pointers and input parameters
  Priority scale 1-5 (tentatively) - too many levels would cause backlogs of low-priority tasks
	By tasks, we mean MAJOR method calls likely to call many smaller methods
	Added by timer or external request
Threads 3-X: Tasks
	Whenever a task finishes, pop the Priority Queue

Most information will be held by individual tasks. Most information transfer will be carried out by tasks themselves, but we WILL want a database that logs science data, performance statistics, system monitoring, and keeping other records


OUTBOUND COMMUNICATION
(to microcontrollers and base station)

Microcontrollers are spoken to through USB
	Need to look into means of communication between Brain and Arduinos

