// Agent sample_agent in project rosbridge_agents

/* Initial beliefs and rules */

/* Initial goals */

!start.

/* Plans */

+!start : true <-
	.print("hello world.");
	takeoff.
