// Agent sample_agent in project rosbridge_agents

/* Initial beliefs and rules */

/* Initial goals */

!start.

/* Plans */

+!start : true <-
	.print("hello world.");
	set_mode("custom_mode=GUIDED");
	arm_motors("value=True");
	takeoff("altitude=5");
	.wait(10000);
	setpoint("latitude= -27.603683", "longitude= -48.518052","altitude=40");
	.wait(10000);
	set_mode("custom_mode=RTL");
	.wait(10000);
	land;
	.
