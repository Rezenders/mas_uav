drone_numbers(3).

victim(1, -27.604011, -48.518338).
victim(2, -27.603716, -48.518078).
victim(3, -27.603585, -48.518465).
victim(4, -27.603693, -48.518641).

!whoami.
!scout_mission.

+!whoami <- .my_name(Me); .term2string(Me, SMe); +online(SMe).

+!scout_mission : true
	<-	!wait_drones;
			!!searchvictims;
			!fly.

+!fly
	<-	.wait(state(_,"True",_));
			!setMode("GUIDED");
			!armMotor;
			!takeOff(5);
			!goToPos(-27.603683, -48.518052, 40);
			!goToPos(-27.603518, -48.518329, 40);
			!goToPos(-27.603677, -48.518652, 40);
			!returnToLand.

+!searchvictims
	<-	.findall([N,X,Y],victim(N,X,Y),L);
			!isvictim(L);
			.wait(500);
			!searchvictims.

+!isvictim([H|T])
	<- 	H = [N, Lat, Long];
			?global_pos(X,Y) & math.abs(X -(Lat)) <=0.00001 & math.abs(Y -(Long)) <=0.00001;
			-victim(N, Lat, Long);
			.print("Found victim ", H);
			.broadcast(tell, victim_in_need(N,Lat,Long));
			!isvictim(T).

+!isvictim([]).

-!isvictim([H|T]) <- !isvictim(T).

+!wait_drones: drone_numbers(N) & .count(online(X), N)
	<- 	.print("All drones in range!!").

+!wait_drones
	<- 	.broadcast(askOne, online(X));
			.wait(drone_numbers(N) & .count(online(X), N), 1000, __)
			!wait_drones.

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

+!mark_as_rescued(N, Lat, Long).
