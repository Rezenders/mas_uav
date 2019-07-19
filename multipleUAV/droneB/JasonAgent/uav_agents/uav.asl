!fly.

+!fly : true <-
	!connect;
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

// +!start_coordination : message("A")
// 	<- .print("Connected to drone A").
//
// +!start_coordination
// 	<- .print("Can't find drone A");
// 		send_msg("B");
// 		.wait(500);
// 		!start_coordination.


+message("?")[source(percept)]
	<- 	send_msg("B");
	    .wait(1000);
		-message("?")[source(percept)].

+!connect : message("A")[source(percept)]
	<- 	.print("Connected to drone A").

+!connect
	<- 	.print("Can't find drone A");
		send_msg("?");
		.wait(1000);
		!connect.
