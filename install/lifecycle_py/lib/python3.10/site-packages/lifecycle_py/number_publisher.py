#!/usr/bin/env python3
import rclpy
from rclpy.lifecycle.node import LifecycleState, TransitionCallbackReturn
from rclpy.node import Node
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle.node import LifecycleState , TransitionCallbackReturn
from example_interfaces.msg import Int64

# Any callback written here is optional, you dont have to implement all the callbacks
class NumberPublisherNode(LifecycleNode):
    def __init__(self):
        super().__init__("number_publisher")
        self.get_logger().info("IN constructor")
        self.number_ = 1
        self.publish_frequency_ = 1.0
        self.number_publisher_ = None
        self.number_timer_ = None


# Create ROS2 communication and hardware connection
    def on_configure(self, previous_state: LifecycleState):
# In this callback you intialize any subscriber or publisher or any ros2 comm or hardware connection    
        self.get_logger().info("IN on_configure")
        self.number_publisher_ = self.create_lifecycle_publisher(Int64, "number", 10)
        self.number_timer_ = self.create_timer(
            1.0 / self.publish_frequency_, self.publish_number)
        self.number_timer_.cancel()
        # raise Exception("IN on_configure")
        return TransitionCallbackReturn.SUCCESS
    
# Destroy ROS2 communication and hardware connection
    def on_cleanup(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_cleanup")
        self.destroy_publisher(self.number_publisher_)
        self.destroy_timer(self.number_timer_)
        return TransitionCallbackReturn.SUCCESS 
    # Activate/Enable Hardware
    def on_activate(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_activate")
        self.number_timer_.reset()
        super().on_activate(previous_state)
        return TransitionCallbackReturn.SUCCESS

    # Deactivate/Disable Hardware
    def on_deactivate(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_deactivate")
        self.number_timer_.cancel()   
        super().on_deactivate(previous_state)
        return TransitionCallbackReturn.SUCCESS
    
    def on_shutdown(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_shutdown")
        self.destroy_publisher(self.number_publisher_)
        self.destroy_timer(self.number_timer_)
        return TransitionCallbackReturn.SUCCESS 
    # process error, deactivate + cleanup 
    def on_error(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_error")
        self.destroy_publisher(self.number_publisher_)
        self.destroy_timer(self.number_timer_)
        # do some checks, if okay return TransitionCallbackReturn.SUCCESS else return TransitionCallbackReturn.FAILURE
        return TransitionCallbackReturn.SUCCESS 

    def publish_number(self):
        msg = Int64()
        msg.data = self.number_
        self.number_publisher_.publish(msg)
        self.number_ += 1

def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()
