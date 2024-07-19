from launch import LaunchDescription
from launch_ros.actions import LifecycleNode
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()
    
    number_node_name = "my_number_publisher"

    # we can do state transition from a launch file but it requires alot of boilerplate
    number_node = LifecycleNode(
        package='lifecycle_py',
        executable='number_publisher',
        name='my_number_publisher',
        namespace=''
    )

    LifecycleNode_node_manager = Node(
        package="lifecycle_py",
        executable="lifecycle_node_manager",
        parameters=[
            {"managed_node_names": number_node_name}
        ]
    )

    ld.add_action(number_node)
    ld.add_action(LifecycleNode_node_manager)

    return ld