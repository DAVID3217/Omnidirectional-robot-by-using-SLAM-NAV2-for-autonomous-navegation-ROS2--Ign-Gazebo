import os, xacro
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command

robot_model = 'omnibot1.sdf'
robot_model_2 = 'omnibot2' #caster_diffbot (bug when V > 0.35), usabase, omnibot
robot_ns = 'r1' # Robot namespace (robot name)
pose = ['1.0', '0.0', '0.0', '0.0'] #Initial robot pose: x,y,z,th
robot_base_color = '0.0 0.0 1.0 0.98' #Ign and Rviz color of the robot's main body (rgba)
world_file = 'warehouse' # empty, building_map

def generate_launch_description():
    package_name = 'ign_robots_examples'

    this_pkg_path = os.path.join(get_package_share_directory(package_name))
    # ~/colcon_ws/install/rp_nav2/share/rp_nav2/

    simu_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Use simulation (Gazebo) clock if true')
    
    # Set ign sim resource path
    ign_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            os.path.join(this_pkg_path, 'worlds'), ':' + str(Path(this_pkg_path).parent.resolve())
        ]
    )

    open_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', str(this_pkg_path+"/rviz/one_robot.rviz")],
    )

    open_ign = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('ros_gz_sim'), 'launch'), '/gz_sim.launch.py']),
            launch_arguments=[
                ('gz_args', [this_pkg_path+"/worlds/"+world_file+".sdf", ' -v 4', ' -r'])

        ]
    )
    
    xacro_file = os.path.join(this_pkg_path, 'urdf', robot_model_2+'.xacro') #.urdf

    doc = xacro.process_file(xacro_file,
        mappings={'base_color' : robot_base_color})

    robot_desc = doc.toxml()

    sdf_file = os.path.join(this_pkg_path, 'sdf', robot_model)
    
    gz_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-string', robot_desc,
                   '-x', pose[0], '-y', pose[1], '-z', pose[2],
                   '-R', '0.0', '-P', '0.0', '-Y', pose[3],
                   '-name', robot_ns,
                   '-allow_renaming', 'false'],
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        # namespace=robot_ns,
        output="screen",
        parameters=[{'robot_description': robot_desc}]
    )

    # Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[             # ign topic -t <topic_name> --info
            '/model/'+robot_ns+'/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/model/'+robot_ns+'/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/lidar@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/world/world_model/model/'+robot_ns+'/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/camera/image_raw@sensor_msgs/msg/Image@ignition.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo@ignition.msgs.CameraInfo',
            '/depth_camera/points@sensor_msgs/msg/PointCloud2@ignition.msgs.PointCloudPacked',
            '/depth_camera/camera_info@sensor_msgs/msg/CameraInfo@ignition.msgs.CameraInfo',
            '/depth_camera/image@sensor_msgs/msg/Image@ignition.msgs.Image',
            '/imu@sensor_msgs/msg/Imu@ignition.msgs.IMU',
        ],
        parameters=[{'qos_overrides./model/'+robot_ns+'.subscriber.reliability': 'reliable'}],
        output='screen',
        remappings=[            # ign topic -l
            ('/model/'+robot_ns+'/cmd_vel', '/cmd_vel'),
            ('/model/'+robot_ns+'/odometry', '/odom'),
            ('/lidar', '/scan'),
            ('/world/world_model/model/'+robot_ns+'/joint_state', '/joint_states'),
        ]
    )

    tf_broadcaster_odom = Node(
        package=package_name,
        executable="tf_broadcaster",
        output="screen",
        arguments=[robot_ns]
    )


    return LaunchDescription(
        [
            simu_time,
            ign_resource_path,
            open_ign,
            gz_spawn_entity,
            robot_state_publisher,
            bridge,
            tf_broadcaster_odom,
            open_rviz
        ]
    )
