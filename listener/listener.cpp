#include <gazebo/transport/transport.hh>
#include <gazebo/msgs/msgs.hh>
#include <gazebo/gazebo.hh>

#include <iostream>
#include <cstring>

#define LASER_SCAN_RANGES_SIZE 813

static float laser_time;
static float laser_scan[LASER_SCAN_RANGES_SIZE];

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
    std::cout << "[" << laser_time << "] Laser scan: " << std::endl;
    print_array(laser_scan, LASER_SCAN_RANGES_SIZE);
}

int main(int argc, char **argv)
{
    gazebo::setupClient(argc, argv);

    gazebo::transport::NodePtr node(new gazebo::transport::Node());
    node->Init();

    laser_time = 0.0f;
    memset(laser_scan, 0, LASER_SCAN_RANGES_SIZE * sizeof(float));

    gazebo::transport::SubscriberPtr sub = node->Subscribe("~/robot/link/laser/scan", laser_callback);

    while (true) {
        gazebo::common::Time::MSleep(10);
    }

    gazebo::shutdown();
}


