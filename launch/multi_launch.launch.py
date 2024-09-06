import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    namespace = 'a200_0957'
    setup_path = os.path.join(os.getenv('HOME'), 'clearpath/')

    map_path = '/map_storage_simulation.yaml'

    simulation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('clearpath_gz'), '/launch/simulation.launch.py'
        ])
    )

    visualization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('clearpath_viz'), '/launch/view_navigation.launch.py'
        ]),
        launch_arguments={'namespace': namespace}.items()
    )

    localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('my_nav_to_pose'), '/launch/localization.launch.py'
        ]),
        launch_arguments={
            'setup_path': setup_path,
            'use_sim_time': 'true',
            'map': map_path
        }.items()
    )

    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('my_nav_to_pose'), '/launch/nav2.launch.py'
        ]),
        launch_arguments={
            'setup_path': setup_path,
            'use_sim_time': 'true'
        }.items()
    )

    return LaunchDescription([
        simulation_launch,
        TimerAction(period=10.0, actions=[visualization_launch]),
        TimerAction(period=20.0, actions=[localization_launch]),
        TimerAction(period=25.0, actions=[navigation_launch])
    ])
