// Agent sample_agent in project rosbridge_agents

/* Initial beliefs and rules */

/* Initial goals */

!start.

/* Plans */

+!start : true <-
	.print("hello world.");
	set_mode("GUIDED");
	.wait(state(GUIDED));
	arm_motors(True);
	takeoff(5);
	.wait(altitude(A) & math.round(A)==5);
	setpoint(-27.603683, -48.518052,40);
	.wait(10000);
	set_mode("RTL");
	.wait(10000);
	land;
	.
