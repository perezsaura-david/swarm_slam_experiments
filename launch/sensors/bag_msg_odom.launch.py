import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.actions import SetParameter


def launch_setup(context, *args, **kwargs):

    return [
        DeclareLaunchArgument('bag_file', default_value='', description=''),
        DeclareLaunchArgument('previous_namespace', default_value='/robot0',
                              description='namespace of the bag file'),
        DeclareLaunchArgument('namespace', default_value='/r0',
                              description='namespace of the cslam nodes'),
        DeclareLaunchArgument('rate', default_value='1.0', description=''),
        DeclareLaunchArgument('bag_start_delay',
                              default_value='5.0',
                              description=''),
        TimerAction(
            period=LaunchConfiguration('bag_start_delay'),
            actions=[
                ExecuteProcess(
                    cmd=[
                        'ros2', 'bag', 'play',
                        LaunchConfiguration('bag_file').perform(context),
                        '-r',
                        LaunchConfiguration('rate'), '--remap',

                        LaunchConfiguration('previous_namespace').perform(context) +
                        '/odometry:=' +
                        LaunchConfiguration('namespace').perform(context) +
                        '/odom',

                        LaunchConfiguration('previous_namespace').perform(context) +
                        '/velodyne_points:=' +
                        LaunchConfiguration('namespace').perform(context) +
                        '/pointcloud',

                        # '--clock', '1',

                        # LaunchConfiguration('previous_namespace').perform(context) +
                        # '/imu/data:=' +
                        # LaunchConfiguration('namespace').perform(context) +
                        # '/imu/data_no',

                        # '/kitti/camera_color/left/camera_info:=' +
                        # LaunchConfiguration('namespace').perform(context) +
                        # '/stereo_camera/left/camera_info',
                        # '/kitti/camera_color/left/image_rect_color:=' +
                        # LaunchConfiguration('namespace').perform(context) +
                        # '/stereo_camera/left/image_rect_color',
                        # '/kitti/camera_color/right/camera_info:=' +
                        # LaunchConfiguration('namespace').perform(context) +
                        # '/stereo_camera/right/camera_info',
                        # '/kitti/camera_color/right/image_rect_color:=' +
                        # LaunchConfiguration('namespace').perform(context) +
                        # '/stereo_camera/right/image_rect_color',
                        # '/kitti/velo/pointcloud:=' +
                        # LaunchConfiguration('namespace').perform(context) +
                        # '/pointcloud',
                        # '/kitti/oxts/gps/fix:=' +
                        # LaunchConfiguration('namespace').perform(context) +
                        # '/gps/fix',
                        # '/kitti/oxts/imu:=' +
                        # LaunchConfiguration('namespace').perform(context) +
                        # '/imu/data',
                    ],
                    name='bag',
                    output='screen',
                )
            ]),
    ]


def generate_launch_description():

    return LaunchDescription([OpaqueFunction(function=launch_setup)])
