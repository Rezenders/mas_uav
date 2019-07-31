!whoami.
!start_mision.

+!whoami <- .my_name(Me); .term2string(Me, SMe); +online(SMe).

+!start_mision : true <-
	.send(droneB, tell, handshake("A"));
	.send(droneB, askOne, online("droneB"), A, 2000);

	.print(A);
	// !wait_droneB;
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
	.

// +!wait_droneB
// 	<- 	.send(droneB, tell, online("droneB"), A, 2000);
// 		!is_droneB(A);
// 		.
//
// +!is_droneB(A): A
// 	<- .print("droneB detected!").
//
// +!is_droneB(A)
// 	<- .print("droneB not found");
// 		!wait_droneB.


+!connect: ack("B") & know("A")  <- .print("Connection estabilished!").

+!connect
	<-	!wave;
	 	!ack;
		!connect;
		.

+!ack: 	handshake("B")[source(droneB)]
	<- 	.send(droneB, tell, ack("A"));
		.print("Aknowledged B!");
		+know("A").

+!ack: 	handshake("B")
	<- 	.send(droneB, tell, ack("A"));
		.print("Aknowledged B!");
		+know("A").

+!ack: 	handshake(X)
	<- 	.send(droneB, tell, ack("A"));
		.print("Aknowledged B!");
		+know("A");
		.

+!ack <- .print("ACK BBBB").

+!wave : not ack("B")
	<- 	.print("Advertising drone A");
		.send(droneB, tell, handshake("A"));
		.wait(2000);
		.
+!wave.
