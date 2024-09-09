from ament_index_python.packages import get_package_share_directory
from clearpath_config.common.utils.yaml import read_yaml
from clearpath_config.clearpath_config import ClearpathConfig
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    GroupAction,
    IncludeLaunchDescription,
    OpaqueFunction
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution
)
from launch_ros.actions import PushRosNamespace, Node

ARGUMENTS = [
    DeclareLaunchArgument('use_sim_time', default_value='false',
                          choices=['true', 'false'],
                          description='Use sim time'),
    DeclareLaunchArgument('setup_path',
                          default_value='/etc/clearpath/',
                          description='Clearpath setup path')
]

def launch_setup(context, *args, **kwargs):
    # Packages
    pkg_clearpath_nav2_demos = get_package_share_directory('my_nav_to_pose')
    pkg_nav2_bringup = get_package_share_directory('nav2_bringup')

    # Launch Configurations
    use_sim_time = LaunchConfiguration('use_sim_time')
    setup_path = LaunchConfiguration('setup_path')

    # Read robot YAML
    config = read_yaml('/root/clearpath/robot.yaml')
    clearpath_config = ClearpathConfig(config)

    namespace = clearpath_config.system.namespace
    platform_model = clearpath_config.platform.get_platform_model()

    file_parameters = PathJoinSubstitution([
        pkg_clearpath_nav2_demos,
        'config',
        'nav2.yaml'])

    launch_nav2 = PathJoinSubstitution(
      [pkg_nav2_bringup, 'launch', 'navigation_launch.py'])

    nav2 = GroupAction([
        PushRosNamespace(namespace),
        Node(
            package='my_nav_to_pose',
            executable='control_husky',
            name='control_husky',
            namespace='a200_0957',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'yaml_filename': '/map_storage_simulation.yaml'
            }],
            remappings=[
                ('/tf', '/a200_0957/tf'),
                ('/tf_static', '/a200_0957/tf_static')
            ]
        ),
        # Launch Nav2 Navigation stack
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(launch_nav2),
            launch_arguments=[
                ('use_sim_time', use_sim_time),
                ('params_file', file_parameters),
                ('use_composition', 'False'),
                ('namespace', namespace)
            ]
        ),
    ])

    return [nav2]

def generate_launch_description():
    return LaunchDescription(ARGUMENTS + [OpaqueFunction(function=launch_setup)])
