#include <gazebo/gazebo_config.h>
#include <gazebo/transport/transport.hh>
#include <gazebo/msgs/msgs.hh>

#if GAZEBO_MAJOR_VERSION >= 6
#include <gazebo/gazebo_client.hh>
#else
#include <gazebo/gazebo.hh>
#endif

#include <iostream>
#include <cstring>

#define LASER_SCAN_RANGES_SIZE 813

static float laser_time;
static float laser_scan[LASER_SCAN_RANGES_SIZE];

static float robot_time;
static float robot_position[3];
static float robot_orientation[4];

void print_array(float *array, int size)
{
    for (int index = 0; index < size; index++) {
        std::cout << array[index] << ' ';
    }
    std::cout << std::endl;
}

void laser_callback(ConstLaserScanStampedPtr &msg)
{
    laser_time = msg->time().sec() + msg->time().nsec() / 1e9;
    for (int index = 0; index < LASER_SCAN_RANGES_SIZE; index++) {
        laser_scan[index] = msg->scan().ranges(index);
    }
    std::cout << "[" << laser_time << "] Laser scan received!" << std::endl;
    print_array(laser_scan, LASER_SCAN_RANGES_SIZE);
}

void robot_callback(ConstPosesStampedPtr &msg)
{
    for (int index = 0; index < msg->pose_size(); index++) {

        if (msg->pose(index).name() == "robot") {
            robot_time = msg->time().sec() + msg->time().nsec() / 1e9;
            std::cout << "[" << robot_time << "] Robot pose received!" << std::endl;

            robot_position[0] = msg->pose(index).position().x();
            robot_position[1] = msg->pose(index).position().y();
            robot_position[2] = msg->pose(index).position().z();

            robot_orientation[0] = msg->pose(index).orientation().x();
            robot_orientation[1] = msg->pose(index).orientation().y();
            robot_orientation[2] = msg->pose(index).orientation().z();
            robot_orientation[3] = msg->pose(index).orientation().w();

            std::cout << "Position: " << std::endl;
            print_array(robot_position, 3);
            std::cout << "Orientation: " << std::endl;
            print_array(robot_orientation, 4);
        }
    }
}

int main(int argc, char **argv)
{
#if GAZEBO_MAJOR_VERSION >= 6
    gazebo::client::setup(argc, argv);
#else
    gazebo::setupClient(argc, argv);
#endif

    gazebo::transport::NodePtr node(new gazebo::transport::Node());
    node->Init();

    laser_time = 0.0f;
    memset(laser_scan, 0, LASER_SCAN_RANGES_SIZE * sizeof(float));

    robot_time = 0.0f;
    memset(robot_position, 0, 3 * sizeof(float));
    memset(robot_orientation, 0, 4 * sizeof(float));

    gazebo::transport::SubscriberPtr laser_sub = node->Subscribe("~/robot/link/laser/scan", laser_callback);
    gazebo::transport::SubscriberPtr robot_sub = node->Subscribe("~/pose/local/info", robot_callback);

    while (true) {
        gazebo::common::Time::MSleep(10);
    }

#if GAZEBO_MAJOR_VERSION >= 6
    gazebo::client::shutdown();
#else
    gazebo::shutdown();
#endif
}
