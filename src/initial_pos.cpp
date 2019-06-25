
   //..................... www.IRANROS.com ..........................\\
  //////////////////////////////////////////////////////////////////////
       // set initial position of turtle with calling services //
  //////////////////////////////////////////////////////////////////////


#include <ros/ros.h>
#include <turtlesim/Kill.h>
#include <turtlesim/Spawn.h>

      
int main(int argc, char **argv) {
  ros::init(argc, argv, "initial_pos");
  ros::NodeHandle nh;

  // Wait until the clear service is available, which
  // indicates that turtlesim has started up, and has
  // set the background color parameters.
  ros::service::waitForService("kill");  //this is optional
  ros::service::waitForService("spawn");  //this is optional

 
 // calling kill service for delete defult turtle:
 
    ros::ServiceClient killClient = nh.serviceClient<turtlesim::Kill>("kill");
	  turtlesim::Kill srv;
	  srv.request.name="turtle1";
	  killClient.call(srv);
	  
	  ROS_INFO("kill");
    
  // calling spawn service for locate robot in initial position:
  
    ros::ServiceClient spawnClient = nh.serviceClient<turtlesim::Spawn>("spawn");
	  turtlesim::Spawn srv2;
	  srv2.request.x=2.2777;  //initial pose.x
	  srv2.request.y=4.9757;  //initial pose.y
	  srv2.request.theta=0.0; //initial orientation
	  srv2.request.name="turtle2";
	  spawnClient.call(srv2);
	 
      ROS_INFO("spawn"); 


  return 0;
}
