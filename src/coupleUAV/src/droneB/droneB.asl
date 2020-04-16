!whoami.
!start_mision.

+!whoami <- .my_name(Me); .term2string(Me, SMe); +online(SMe).

+!start_mision : true
	<-	!wait_droneA;
			!deliverBuoys.

+!deliverBuoys: victim(_, _, _)
	<-	.findall([N, Lat,Long], victim(N,Lat,Long), V);
			.sort(V, SV);
			.nth(0, SV, Next);
			Next = [N, Lat, Long];

			!rescueVictim(N, Lat, Long)
			!deliverBuoys.

+!deliverBuoys
	<-	.wait(1000);
			!deliverBuoys.

+!rescueVictim(N, Lat, Long)
	<- 	!setMode("GUIDED");
			!armMotor;
			!takeOff(5);
			!goToPos(Lat, Long, 25);
			.print("Droping buoy to victim ", victim(N,Lat,Long));
			.abolish(victim(N, Lat, Long));
			!returnToLand;
			.print("Landed! beginning charging and buoy replacement!");
			.wait(3000).

+!wait_droneA: online("droneA")
	<- 	.print("Drone A in range").

+!wait_droneA
	<- 	.send(droneA, askOne, online(X));
		.wait(1000);
		!wait_droneA.

+!setMode(Mode) : not state(Mode,_,_,_)
	<- 	set_mode(Mode);
			.wait(state(Mode,_,_), 1000).

+!setMode(Mode).

-!setMode(Mode) <- !setMode(Mode).

+!armMotor : not state(Mode,_,"True")
	<-	arm_motors(True);
			.wait(state(Mode,_,"True"), 1000).

+!armMotor.

-!armMotor <- !armMotor.

+!takeOff(Alt)
	<-	takeoff(Alt);
			.wait(altitude(A) & math.abs(A-Alt) <= 0.1).

+!goToPos(Lat, Long, Alt)
	<- 	setpoint(Lat, Long, Alt);
			.wait(global_pos(X,Y) & math.abs(X -(Lat)) <=0.00001 & math.abs(Y -(Long)) <=0.00001).

+!returnToLand
	<-	set_mode("RTL");
			.wait(global_pos(X,Y) & home_pos(X2,Y2) & math.abs(X -(X2)) <=0.00001 & math.abs(Y -(Y2)) <=0.00001 & altitude(A) & math.abs(A-0) <= 0.1).
