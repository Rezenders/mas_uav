import rospy
import mavros
import mavros_msgs.srv
import mavros_msgs.msg
import sensor_msgs.msg
import std_msgs.msg

class FlightController:

    def __init__(self):
        self. executable_missions =[
        "takeoff",
        "setpoint",
        "home",
        "land",
        ]

        self.state = mavros_msgs.msg.State()
        self.rel_alt = std_msgs.msg.Float64()
        self.global_pos = sensor_msgs.msg.NavSatFix()
        self.home_pos = mavros_msgs.msg.HomePosition()

        state_sub = rospy.Subscriber('/mavros/state', mavros_msgs.msg.State,
                                     self.state_callback)

        rel_alt_sub = rospy.Subscriber(
            '/mavros/global_position/rel_alt',
            std_msgs.msg.Float64,
            self.rel_alt_callback)

        global_pos_sub = rospy.Subscriber(
            '/mavros/global_position/global',
            sensor_msgs.msg.NavSatFix,
            self.global_pos_callback)

        home_pos_sub = rospy.Subscriber(
            '/mavros/home_position/home',
            mavros_msgs.msg.HomePosition,
            self.home_pos_callback)

    def set_mode(self, **kw):
        rospy.wait_for_service('/mavros/set_mode')
        try:
            set_mode_aux = rospy.ServiceProxy('/mavros/set_mode',
                                              mavros_msgs.srv.SetMode)
            set_mode_aux(**kw)
        except rospy.ServiceException as e:
            print("service set_mode call failed: %s." % e)

    def arm_motors(self, args, **kw):
        rospy.wait_for_service('mavros/cmd/arming')
        try:
            arm_motors_aux = rospy.ServiceProxy('mavros/cmd/arming',
                                                mavros_msgs.srv.CommandBool)
            is_motors_armed = arm_motors_aux(args, **kw)
        except rospy.ServiceException as e:
            print("service arming call failed: %s." % e)

    def takeoff(self, **kw):
        rospy.wait_for_service('mavros/cmd/takeoff')
        try:
            takeoff_aux = rospy.ServiceProxy('mavros/cmd/takeoff',
                                             mavros_msgs.srv.CommandTOL)
            takeoff_aux(**kw)
        except rospy.ServiceException as e:
            print("service takeoff call failed: %s." % e)

    def land(self, **kw):
        rospy.wait_for_service('mavros/cmd/land')
        try:
            land_aux = rospy.ServiceProxy('mavros/cmd/land',
                                             mavros_msgs.srv.CommandTOL)
            land_aux(**kw)
        except rospy.ServiceException as e:
            print("service land call failed: %s." % e)

    def setpoint_global(self, **kw):
        setpoint_global_pub = rospy.Publisher(
            '/mavros/setpoint_position/global',
            mavros_msgs.msg.GlobalPositionTarget,
            queue_size=1,
            latch=True)

        header = std_msgs.msg.Header()
        header.stamp = rospy.Time.now()
        kw['header'] = header

        setpoint_global_pub.publish(**kw)

    # Check if the mission is executable
    def executable_mission(self, mission):
        return (mission.action in self.executable_missions)

    # Execute mission
    def execute_mission(self, mission):
        if(mission.action == 'takeoff'):
            self.takeoff(**mission.params)
        elif(mission.action == 'setpoint'):
            self.setpoint_global(**mission.params)
        elif(mission.action == 'home'):
            self.set_mode(custom_mode='RTL')
        elif(mission.action == 'land'):
            self.land(**mission.params)
        else:
            print("There is no execution plan for this action!")

    #Verify if the mission is completed
    def mission_completed(self, mission):
        completed = False
        if(mission.action == 'takeoff'):
            if int(self.rel_alt.data) == mission.params['altitude']:
                completed = True
        elif(mission.action == 'setpoint'):
            if round(self.global_pos.latitude, 5) == round(mission.params['latitude'], 5) \
                and round(self.global_pos.longitude, 5) == round(mission.params['longitude'], 5):
                completed = True
        elif(mission.action == 'home'):
            if round(self.global_pos.latitude, 5) == round(self.home_pos.latitude, 5) \
                and round(self.global_pos.longitude, 5) == round(self.home_pos.longitude, 5):
                completed = True
        elif(mission.action == 'land'):
            completed = True #TODO:Fix this
        return completed


    # Drone State callback
    def state_callback(self, msg):
        self.state = msg

    # Drone rel_alt callback
    def rel_alt_callback(self, msg):
        self.rel_alt = msg

    # Drone global_pos callback
    def global_pos_callback(self, msg):
        self.global_pos = msg

    # Drone home_pos callback
    def home_pos_callback(self, msg):
        self.home_pos = msg

class Action:
    def __init__(self):
        self.action = None
        self.params = dict()

    def __init__(self, action, **params):
        self.action = action
        self.params = params
