drone_numbers(3).

!whoami.
!myid.
!wait_drones.

+!whoami <- .my_name(Me); .term2string(Me, SMe); +online(SMe).
+!myid <- .random(R); +myid(R*10).

+victim_in_need(N, Lat, Long)
	<-	!start_negotiation.

+!start_negotiation: .desire(negotiate)
	<- 	.suspend;
		!!start_negotiation.

@lg[atomic]
+!start_negotiation
	<- !negotiate.

+!negotiate
	<-	.findall([N, Lat, Long], victim_in_need(N,Lat,Long), V);
		.sort(V, SV);
		.nth(0, SV, Next);
		Next = [N, Lat, Long];

		!propose(N);
		.wait(2000);
		.findall([O, Id],propose(Id, N, O), L);
		!choose_proposal(N, L, Wid).

-!negotiate.

+!propose(N)
	<- 	.random(R);
		?myid(Id);
		+propose(Id, N, R);
		.broadcast(tell, propose(Id, N, R)).

+!choose_proposal(N, L, Wid)
	<-	.min(L, [Wo, Wid]);
		!check_winner(N, Wid);
		.abolish(propose(_,_,_)).

-!choose_proposal(N, L, Wid).

+!check_winner(N, Wid): myid(Wid)
	<-	.print("I am responsible for rescuing victim ", N);
		?victim_in_need(N, Lat, Long);
		.abolish(victim_in_need(N,Lat,Long));
		.broadcast(achieve, mark_as_rescued(N,Lat,Long));
		!rescueVictim(N, Lat, Long).

+!check_winner(N, Wid)
	<- 	.print("Not selected!").

+!rescueVictim(N, Lat, Long)
	<- 	!setMode("GUIDED");
		arm_motors(True);
		!takeOff(5);
		!goToPos(Lat, Long, 25);
		.print("Droping buoy to victim ", N,Lat,Long);
		.broadcast(tell, victim_rescued(N, Lat, Long));
		!returnToLand;
		.print("Landed! beginning charging and buoy replacement!");
		.wait(3000);
		.resume(start_negotiation).

+!mark_as_rescued(N, Lat, Long)
	<- .abolish(victim_in_need(N,Lat,Long)).

+!wait_drones: drone_numbers(N) & .count(online(X), N)
	<- 	.print("All drones in range!!").

+!wait_drones
	<- 	.broadcast(askOne, online(X));
		.wait(drone_numbers(N) & .count(online(X), N), 1000, __)
		!wait_drones.

+!setMode(Mode)
	<- 	set_mode(Mode);
		.wait(state(Mode)).

+!takeOff(Alt)
	<-	takeoff(Alt);
		.wait(altitude(A) & math.abs(A-Alt) <= 0.1).

+!goToPos(Lat, Long, Alt)
	<- 	setpoint(Lat, Long, Alt);
		.wait(global_pos(X,Y) & math.abs(X -(Lat)) <=0.00001 & math.abs(Y -(Long)) <=0.00001).

+!returnToLand
	<-	set_mode("RTL");
		.wait(global_pos(X,Y) & home_pos(X2,Y2) & math.abs(X -(X2)) <=0.00001 & math.abs(Y -(Y2)) <=0.00001 & altitude(A) & math.abs(A-0) <= 0.1).
