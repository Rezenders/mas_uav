victm(1, -27.604011, -48.518338).
victm(2, -27.603716, -48.518078).
victm(3, -27.603585, -48.518465).
victm(4, -27.603693, -48.518641).

!whoami.
!scout_mission.

+!whoami <- .my_name(Me); .term2string(Me, SMe); +online(SMe).

+!scout_mission : true <-
	!wait_droneB;
	!!searchVictms;
	!fly;
	.

+!fly
	<-	!setMode("GUIDED");
		arm_motors(True);
		!takeOff(5);
		!goToPos(-27.603683, -48.518052, 40);
		!goToPos(-27.603518, -48.518329, 40);
		!goToPos(-27.603677, -48.518652, 40);
		set_mode("RTL");
		.

+!searchVictms
	<-	.findall([N,X,Y],victm(N,X,Y),L);
		!isVictm(L);
		.wait(500);
		!searchVictms;
		.

+!isVictm([H|T])
	<- 	H = [N, Lat, Long];
		?global_pos(X,Y) & math.abs(X -(Lat)) <=0.00001 & math.abs(Y -(Long)) <=0.00001;
		-victm(N, Lat, Long);
		.print("Found victm ", H);
		.send(droneB, tell, victm(N,Lat,Long));
		!isVictm(T);
		.

+!isVictm([]).

-!isVictm([H|T]) <- !isVictm(T).

+!wait_droneB: online("droneB")
	<- 	.print("Drone B in range");
		.

+!wait_droneB
	<- 	.send(droneB, askOne, online(X));
		.wait(1000);
		!wait_droneB;
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
