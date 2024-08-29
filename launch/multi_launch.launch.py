import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetLaunchConfiguration, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    namespace = 'a200_0000'
    setup_path = os.path.join(os.getenv('HOME'), 'clearpath/')

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

    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('clearpath_nav2_demos'), '/launch/slam.launch.py'
        ]),
        launch_arguments={
            'setup_path': setup_path,
            'use_sim_time': 'true'
        }.items()
    )

    localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('clearpath_nav2_demos'), '/launch/localization.launch.py'
        ]),
        launch_arguments={
            'setup_path': setup_path,
            'use_sim_time': 'true'
        }.items()
    )

    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare('clearpath_nav2_demos'), '/launch/nav2.launch.py'
        ]),
        launch_arguments={
            'setup_path': setup_path,
            'use_sim_time': 'true'
        }.items()
    )

    return LaunchDescription([
        simulation_launch,
        TimerAction(period=5.0, actions=[visualization_launch]),
        TimerAction(period=10.0, actions=[slam_launch]),
        TimerAction(period=15.0, actions=[localization_launch]),
        TimerAction(period=20.0, actions=[navigation_launch])
    ])
