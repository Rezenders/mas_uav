!whoami.
!start_mision.

+!whoami <- .my_name(Me); .term2string(Me, SMe); +online(SMe).

+!start_mision : true <-
	!wait_droneA;
	!deliverBuoys;
	.

+!deliverBuoys: victm(_, _, _)
	<-	.findall([N, Lat,Long], victm(N,Lat,Long), V);
		.sort(V, SV);
		.nth(0, SV, Next);
		Next = [N, Lat, Long];
		
		!setMode("GUIDED");
		arm_motors(True);
		!takeOff(5);
		!goToPos(Lat, Long, 20);
		.print("Droping buoy to victm ", victm(N,Lat,Long));
		.abolish(victm(N, Lat, Long));
		set_mode("RTL");
		.wait(global_pos(X,Y) & home_pos(X2,Y2) & math.abs(X -(X2)) <=0.00001 & math.abs(Y -(Y2)) <=0.00001 & altitude(A) & math.abs(A-0) <= 0.1);
		.print("Landed! beginning charging and buoy replacement!");
		.wait(3000);
		!deliverBuoys;
		.

+!deliverBuoys
	<-	.wait(1000);
		!deliverBuoys;
		.

+!wait_droneA: online("droneA")
	<- 	.print("Drone A in range");
		.

+!wait_droneA
	<- 	.send(droneA, askOne, online(X));
		.wait(1000);
		!wait_droneA;
		.

+!setMode(Mode)
	<- 	set_mode(Mode);
		.wait(state(Mode));
		.

+!takeOff(Alt)
	<-	takeoff(Alt);
		.wait(altitude(A) & math.abs(A-Alt) <= 0.1);
		.

+!goToPos(Lat, Long, Alt)
	<- 	setpoint(Lat, Long, Alt);
		.wait(global_pos(X,Y) & math.abs(X -(Lat)) <=0.00001 & math.abs(Y -(Long)) <=0.00001);
		.
