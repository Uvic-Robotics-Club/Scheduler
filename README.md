# Scheduler

The new central software.

We are ditching ROS because of many reasons including the steep learning curve, its incompatibility with Windows, and its inability to teach transferable skills to new recruits.

The new scheme will be written in Python and C++, with a central Python threading mechanism.

Rather than having ROS subscribers and publishers, methods will be called when data comes which put tasks into the priority queue ("published")

SHELL.PY would run basically everything; it is replacing "roscore"
It's also where the threading magic happens

Most information will be held by individual tasks. Most information transfer will be carried out by tasks themselves, but we WILL want a database that logs science data, performance statistics, system monitoring, and keeping other records

# Explanation

The Scheduler is a mechanism that allows us to place a sequence of tasks into a queue, and executes each task in an ordered fashion that streamlines communication between different parts of the system. For example, instead of a class having to directly reference multiple other classes, it does not have to worry about that, and is only concerned with passing the data to the scheduler when needed.

`Scheduler` is driven by 2 main threads. When a `Scheduler` instance is instantiated, a list of functions (`pollFunctionsList` in the constructor) is stored. The meaning of a "polling" function is essentially that it is a function that is called on a regular interval. The essence of the class is that each function in `pollFunctionsList` "produces" data (perhaps a number or a list with useful information) that will be "consumed" (i.e used one way or another) by a consumer, likely another class somewhere in the application.

 Then, when `Scheduler.run()` is called on the scheduler instance, this creates and starts the 2 main threads. The 2 threads are created with the following lines:

``` 
	t = threading.Thread(target=self.poll_loop)
	t.start()
	t = threading.Thread(target=self.event_loop)
	t.start()
```

The `Scheduler` class in scheduler.py is executed and interacted with the help of those 2 main threads. This is illustrated in the following sequence diagram.

![Scheduler Sequence Diagram](images/scheduler_sequence_diagram.png)

To explain the behavior of the class, we must known what each thread does:
- **Thread 1**: Used as an "input" to the scheduler. It calls the function defined by the producer, and places the list of functions to be called (all of them located in "consumer" classes) into the priority queue.
- **Thread 2**: Priority queue execution; the thread pulls functions from the queue and creates a new thread for the function to run in. By the nature of the priority queue, when the thread pulls functions from the queue, it gets given the functions with the highest priority first.
- **Thread 3-X**: Each thread is associated with a task, which when the function completes, the thread completes.


It is helpful to begin understanding the behavior of `Scheduler` by following _Thread 1_. At a defined interval, the thread will fetch all the functions in `pollFunctionsList` (a.k.a `self.pfl` in the class), and push each function onto `pq`, which is the queue of tasks that need to be executed.

On the other hand, _Thread 2_ handles the actual execution of each function that has been pushed in `pq`, as it continuously fetches any functions that are in `pq`. After fetching a function from it, it starts a thread for **each** function.

![Scheduler Example Diagram](images/scheduler_example.png)

# Use Cases

The scheduler is expected to be used for the folllowing main use cases:
- Outbound communication from rover to base station 
- Inbound communication from base station to rover
- Communication between microcontrollers on the rover 

# Improvements

Microcontrollers are spoken to through USB
	Need to look into means of communication between Brain and Arduinos