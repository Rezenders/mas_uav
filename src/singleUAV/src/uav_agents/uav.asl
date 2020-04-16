!fly.

+!fly : true <-
	.print("Starting Jason Agent node.");
	// .wait(state(_,"True",_,_));
	!setMode("GUIDED");
	!armMotor;
	!takeOff(5);
	!goToPos(-27.603683, -48.518052, 40);
	!returnToLand.

+!setMode(Mode)
	<- 	set_mode(Mode);
			.wait(state(Mode,_,_,_)).

+!armMotor
	<-  arm_motors(True);
			.wait(state(Mode,_,_,"True")).

+!takeOff(Alt)
	<-	takeoff(Alt);
			.wait(altitude(A) & math.abs(A-Alt) <= 0.1).

+!goToPos(Lat, Long, Alt)
	<- 	setpoint(Lat, Long, Alt);
			.wait(global_pos(X,Y) & math.abs(X -(Lat)) <=0.00001 & math.abs(Y -(Long)) <=0.00001).

+!returnToLand
	<-	set_mode("RTL");
			.wait(global_pos(X,Y) & home_pos(X2,Y2) & math.abs(X -(X2)) <=0.00001 & math.abs(Y -(Y2)) <=0.00001 & altitude(A) & math.abs(A-0) <= 0.1).
