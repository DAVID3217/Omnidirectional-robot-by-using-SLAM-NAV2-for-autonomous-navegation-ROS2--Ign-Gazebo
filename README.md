

## List of robots and plugins (using URDF)

So far, this repo supports the following robots type and plugins:

+ 2 wheeled differential drive mobile robot with passive wheel (caster_diffbot):
  * 1 diff-drive with encoder odometry plugin.

+ The caster_diffbot with passive wheel and sensors (sensors_diffbot):
  * 1 diff-drive and world odometry plugins.
  * 1 IMU, 1 LiDAR, 1 velodyne, 1 monocular camera, 1 RGBD camera, 1 linear battery.
  * Namespace is used for all links and joints.

+ 4 wheeled differential drive mobile robot (ugv_4wheels):
  * Minimum skid steering configuration using both the diff-drive and the world odometry plugn.
  * All wheels are defined using a macro.
  * No other sensor.

+ Omnidirectional mobile robot composed of 4 mecanum wheels (omnibot):
  * All wheels are defined using a macro.
  * The light, on the base link, is optional according to the user by an argument from launcher.
  * No other sensor.


> [!IMPORTANT]
> To obtain a correct behavior of the sensors, the world.sdf file MUST be correctly set by adding the corresponding 'plugin' tag inside the 'world' tag. For more information. please refer to https://gazebosim.org/docs/latest/sensors/.


# Information source
- Main source: https://github.com/gazebosim/ros_gz/tree/ros2
- URDF xacro:
    + http://wiki.ros.org/urdf/XML
    + http://wiki.ros.org/urdf/Tutorials
- ROS 2 Control with Ignition: https://control.ros.org/humble/doc/getting_started/getting_started.html
- Gz ROS Control repo: https://github.com/ros-controls/gz_ros2_control/tree/humble


# Installing ROS 2 packages

To avoid possible errors, please update your system and install the following ROS 2 dependencies.

```
sudo apt-get update
```

ROS 2 dependencies for robot description:

```bash
sudo apt-get install ros-$ROS_DISTRO-joint-state-publisher ros-$ROS_DISTRO-xacro ros-$ROS_DISTRO-joint-state-publisher-gui ros-$ROS_DISTRO-tf2-* ros-$ROS_DISTRO-gazebo-* ros-$ROS_DISTRO-rviz-default-plugins ros-$ROS_DISTRO-ros2-control ros-$ROS_DISTRO-ros2-controllers ros-$ROS_DISTRO-controller-manager
```

If the following error appears:<br>
_LookupError: Could not find the resource '<package_name>' of type 'packages'_

Try to install the corresponding ROS dependency with

`sudo apt-get install ros-$ROS_DISTRO-<package-name>`

For example:

`sudo apt-get install ros-$ROS_DISTRO-joint-state-publisher-gui`

<br>

It is assumed that both 'ros_gz' and 'ros_ign_bridge' packages were already installed, otherwise

```
sudo apt-get install ros-${ROS_DISTRO}-ros-gz ros-${ROS_DISTRO}-ros-ign-bridge
```


## Adding this repo

Please, paste this package in the src folder. Then:
```bash
cd ~/colcon_ws
rosdep install -i --from-path src --rosdistro $ROS_DISTRO -y
```

If you already have all your dependencies, the console will return:<br>
#All required rosdeps installed successfully

**Note:** _This is made only once for the whole workspace._

Then, build colcon ws:
```bash
colcon build --packages-select ign_robots_examples --symlink-install
source install/setup.bash
```

**IMPORTANT:** This builds the package and sets a symbolic link to the python files (nodes and launch files). With this, re-build every time that a python file is modified, is not required.<br>
In ROS 2, launch files may be written in yaml, xml or python languages, but it is extremely recommended to use python. Also, the name of all launch files must finish with 'launch.py'. Otherwise, the file will not be recognized.

If some warnings appear, run `colcon build --packages-select ign_robots_examples --symlink-install` again and they will disappear.


# Launching the robot in Gazebo

The 'one_robot_gz_launch.py' launch file, opens Gazebo using an empty world, and spawns a robot which is selected in the file.

**_Note: The first time may take a while._**<br>

```
ros2 launch ign_robots_examples one_robot_gz_launch.py
```

To change the robot model, initial robot pose, world file, color base and namespace, please edit 'one_robot_gz_launch.py' file.


## Teleoperating the robot

To teleoperate both the _differential_ and _omnidirectional_ mobile robot, use the package node:

`ros2 run ign_robots_examples omni_teleop_keyboard.py`

To use a namespace, to remap topics, services and node name, please use:

`ros2 run ign_robots_examples omni_teleop_keyboard.py --ros-args -r __ns:=/r1`

To publish a velocity from terminal:

`ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.1, y: 0.1}, angular: {z: 0.3}}"`

`ros2 topic pub --once /r1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.1, y: 0.1}, angular: {z: 0.3}}"`


ign topic -t "/model/r1/cmd_vel" -m ignition.msgs.Twist -p "linear: {x: 0.5, y: 0.5}"
