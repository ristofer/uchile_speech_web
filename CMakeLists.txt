cmake_minimum_required(VERSION 2.8.3)
project(uchile_speech_web)

find_package(catkin REQUIRED COMPONENTS
  roslib
  rospy
  std_msgs
  message_generation
  actionlib_msgs
  actionlib
)

find_package(Boost REQUIRED COMPONENTS system signals thread)


add_action_files(
  DIRECTORY 
  action
  FILES
  DoRecognition.action
  CalibrateThreshold.action
)


generate_messages(
  DEPENDENCIES
  actionlib_msgs
)



catkin_package(
  CATKIN_DEPENDS rospy std_msgs message_runtime actionlib_msgs actionlib 

)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)
