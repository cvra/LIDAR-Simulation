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

void laser_callback(ConstLaserScanStampedPtr &msg)
{
    laser_time = msg->time().sec() + msg->time().nsec() * 1e-9;
    for (int index = 0; index < LASER_SCAN_RANGES_SIZE; index++) {
        laser_scan[index] = msg->scan().ranges(index);
    }
    std::cout << "[" << laser_time << "] Laser scan received!" << std::endl;
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

    gazebo::transport::SubscriberPtr laser_sub = node->Subscribe("~/robot/link/laser/scan", laser_callback);

    while (true) {
        gazebo::common::Time::MSleep(10);
    }

#if GAZEBO_MAJOR_VERSION >= 6
    gazebo::client::shutdown();
#else
    gazebo::shutdown();
#endif
}
