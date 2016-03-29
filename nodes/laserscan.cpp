#include <gazebo/gazebo_config.h>
#include <gazebo/transport/transport.hh>
#include <gazebo/msgs/msgs.hh>

#if GAZEBO_MAJOR_VERSION >= 6
#include <gazebo/gazebo_client.hh>
#else
#include <gazebo/gazebo.hh>
#endif

#include "UDPClient.hpp"
#include <iostream>
#include <cstring>

#define LASER_SCAN_RANGES_SIZE 813

UDPClient *client;


void laser_callback(ConstLaserScanStampedPtr &msg)
{
    float laser_time, laser_scan[LASER_SCAN_RANGES_SIZE];
    uint8_t udp_msg[LASER_SCAN_RANGES_SIZE * sizeof(float)];

    laser_time = msg->time().sec() + msg->time().nsec() * 1e-9;
    for (int index = 0; index < LASER_SCAN_RANGES_SIZE; index++) {
        laser_scan[index] = msg->scan().ranges(index);
    }
    std::cout << "[" << laser_time << "] Laser scan" << std::endl;

    memcpy(udp_msg, laser_scan, LASER_SCAN_RANGES_SIZE * sizeof(float));
    client->send(udp_msg, LASER_SCAN_RANGES_SIZE * sizeof(float));
}

int main(int argc, char **argv)
{
    // UDP client
    boost::asio::io_service io_service;
    client = new UDPClient(io_service, "localhost", "9999");

    // Gazebo client
#if GAZEBO_MAJOR_VERSION >= 6
    gazebo::client::setup(argc, argv);
#else
    gazebo::setupClient(argc, argv);
#endif

    gazebo::transport::NodePtr node(new gazebo::transport::Node());
    node->Init();

    gazebo::transport::SubscriberPtr laser_sub = node->Subscribe("~/robot/link/laser/scan", laser_callback);

    while (true) {
        gazebo::common::Time::MSleep(10);
    }

#if GAZEBO_MAJOR_VERSION >= 6
    gazebo::client::shutdown();
#else
    gazebo::shutdown();
#endif

    return 0;
}
