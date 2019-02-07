// Agent sample_agent in project rosbridge_agents

/* Initial beliefs and rules */

/* Initial goals */

!start.

/* Plans */

+!start : true <-
	.print("hello world.");
	takeoff("altitude=40");
	.

+done(takeoff)
	<-	!follow_trajectory
		.

+!follow_trajectory
	<-	setpoint("latitude= -27.603683", "longitude= -48.518052","altitude=40")
		.
