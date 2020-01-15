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
  Tasks being custom objects holding function pointers and inmput parameters
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

# Documentation

The `Scheduler` class is driven by 2 main threads of execution. When a `Scheduler` instance is instantiated, a list of poll functions (`pollFunctionsList` in the constructor) is stored. The essence of the class is that each function stored in `pollFunctionsList` will be executed at a regular interval defined in the scheduler class.

 Then, when `run()` is called, this creates and starts the 2 main threads. The 2 threads are created with the following lines:

``` 
	t = threading.Thread(target=self.poll_loop)
	t.start()
	t = threading.Thread(target=self.event_loop)
	t.start()
```

The `Scheduler` class in scheduler.py is executed and interacted with the help of those 2 main threads. This is illustrated in the following sequence diagram.

![Scheduler Sequence Diagram](images/scheduler_sequence_diagram.png)

It is helpful to begin tracing the behavior of the `Scheduler` class by following _Thread 1_. At a defined interval, the thread will fetch all the functions in `pollFunctionsList` (a.k.a `self.pfl` in the class), and push each function onto `pq`, which is the queue of tasks that need to be executed.

On the other hand, _Thread 2_ handles the actual execution of each function that has been pushed in `pq`, as it continuously fetches any functions that are in `pq`. After fetching a function from it, it starts a thread for **each** function.

![Scheduler Example Diagram](images/scheduler_example.png)