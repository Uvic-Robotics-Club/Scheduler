import scheduler
import workAdder

from scheduler_types import *
from sample_material import *

def main():
	# List of functions for the scheduler to loop through
	pollFuncts = []

	# ----- Create everything here ----

	# ----------------------------------------------------------------
	# Part 1
	# Create a timer and add it to the our list of poll functions

	timer = Self_contained_timer(1)
	pollFuncts.append(timer.poll_function)

	# ----------------------------------------------------------------
	# Part 2
	# Create a producer, and link it two different consumers

	# p = Simple_producer()
	# pollFuncts.append(p.poll_function)
	#
	# c1 = Simple_consumer(2)
	# p.add_function_to_call(c1.on_event)
	# c2 = Simple_consumer(3)
	# p.add_function_to_call(c2.on_event)

	# ----------------------------------------------------------------
	# Part 3
	# one producer, a middleman, and two end consumers

	# p2 = Simple_producer()
	# pollFuncts.append(p2.poll_function)
	#
	# m = Simple_middleman()
	# p2.add_function_to_call(m.on_event)
	#
	# c3 = Simple_consumer(2)
	# m.add_function_to_call(c3.on_event)
	# c4 = Simple_consumer(3)

	# Note that c4.on_event is being called by two different sources.
	# There's no restriction on who can call what as long as (a) you don't create any loops, and
	# (b) the parameters of the producer match the consumer

	# m.add_function_to_call(c4.on_event)
	# p2.add_function_to_call(c4.on_event)

	# ----- Below here will rarely need to change -----

	# Initialize and start the program
	# '8' is the maximum number of simultaneous threads, and 'functs' is the polling function list
	s = scheduler.Scheduler(8, pollFuncts)
	# Create the workAdder singleton
	wA = workAdder.workAdder(s)
	s.run()


if __name__ == '__main__':
	main()
