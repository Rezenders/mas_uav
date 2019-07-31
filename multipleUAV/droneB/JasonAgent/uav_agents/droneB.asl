!whoami.
!start_mision.

+!whoami <- .my_name(Me); .term2string(Me, SMe); +online(SMe).

+!start_mision : true <-
	!inrange_droneA;
	// !connect;
	// !start_coordination;
	// .print("Starting Jason Agent node.");
	// set_mode("GUIDED");
	// .wait(state("GUIDED"));
	// arm_motors(True);
	// takeoff(5);
	// .wait(altitude(A) & math.abs(A-5) <= 0.1);
	// setpoint(-27.603683, -48.518052, 40);
	// .wait(global_pos(X,Y) & math.abs(X -(-27.603683)) <=0.00001 & math.abs(Y -(-48.518052)) <=0.00001);
	// set_mode("RTL");
	//
	.

+!inrange_droneA: online("droneA")
	<- 	.print("Drone A in range");
		.

+!inrange_droneA
	<- 	.send(droneA, askOne, online(X));
		.wait(1000);
		!inrange_droneA;
		.
