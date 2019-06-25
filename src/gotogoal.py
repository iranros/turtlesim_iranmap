#!/usr/bin/env python
#!/usr/bin/env python

# /////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////// www.IRANROS.com /////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////

#................................ Turtlesim_IranMap Project .........................

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


class TurtleBot:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle2/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle2/cmd_vel',
                                                  Twist, queue_size=10)

        # A subscriber to the topic '/turtle2/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/turtle2/pose',
                                               Pose, self.update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(10)
    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
         return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=6):
         return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self):
	
        """Moves the turtle to the goal."""
        goal_pose = Pose()
       
       # latitude and  longitude of Iran boundries (normalized)   
        yy=[4.9757,5.2422,5.5389,5.9397,6.2290,6.4821,7.0084,7.6029,7.9349,8.4058,8.9055,9.6517,9.8965,9.5268,9.4584,9.8283,9.7003,9.2960,9.2313,8.8037,8.6863,8.3656,8.4471,8.6615,9.0417,8.9710,8.5277,8.3213,7.3428,6.2604,5.7545,5.6777,5.4247,4.9203,4.4076,4.2203,4.1304,3.6278,3.5848,3.3156,3.1512,2.6109,2.6884,3.2980,3.5704,3.5348,3.2733,3.4411,3.7613,3.8625,3.8625,4.4040,4.8056,5.0832,5.0916,4.9822,4.9757,4.7726,4.1873,3.6145,3.1581,2.5190,2.8706,3.0362,2.8373,2.4098,2.0003,2.0728,2.1265,2.5738,2.8819,3.0750,2.9837,2.5445,1.9702,1.7004,1.7351,2.5174,2.5492,3.1512] 
        xx=[2.2777,2.0158,1.8374,1.9234,1.7224,1.0192,0.7252,1.0648,0.9262,0.4333,0.2306,0.0218,0.2756,0.6784,1.2943,1.9546,2.1615,2.2343,2.4368,2.5767,3.0716,3.5328,4.9025,4.9797,5.8376,6.7861,7.9688,8.5460,8.5072,8.3632,8.4699,8.8492,8.9020,8.4449,8.8306,9.1910,9.3980,9.4201,9.6478,9.5764,8.9685,8.7808,8.1111,6.5252,6.3661,5.9319,5.3480,4.7403,4.2765,4.1003,4.1003,3.4323,3.2581,3.0175,2.6338,2.2995,2.2777,2.0492,2.2535,2.6457,3.1146,3.3452,3.4471,3.6407,3.7709,3.7596,3.8969,4.5440,5.1820,5.5310,5.9070,6.1418,6.2194,6.1636,6.5577,8.6394,9.0766,9.1688,8.7900,8.9685] 
     
       
	for i in range(0,79):
			goal_pose.x = xx[i]
			goal_pose.y = yy[i]

			# Please, insert a number slightly greater than 0 (e.g. 0.01).
			distance_tolerance =0.1

			vel_msg = Twist()
			
			while self.euclidean_distance(goal_pose) >= distance_tolerance:

				# Porportional controller.
			
				# Linear velocity in the x-axis.
				vel_msg.linear.x = 2*self.linear_vel(goal_pose)
				vel_msg.linear.y = 0
				vel_msg.linear.z = 0

				# Angular velocity in the z-axis.
				vel_msg.angular.x = 0
				vel_msg.angular.y = 0
				vel_msg.angular.z =2* self.angular_vel(goal_pose)

				# Publishing our vel_msg
				self.velocity_publisher.publish(vel_msg)

				# Publish at the desired rate.
				self.rate.sleep()
			i+=i
			
            	
	print(" //////////// Turtle traversed the Iran map boundries succesfully /////////////")
        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)

        # If we press control + C, the node will stop.
	print("\n press control + C for close. ")
        rospy.spin()

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass
