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

UDPClient *client;


void robot_callback(ConstPosesStampedPtr &msg)
{
    float robot_time, robot_pose[7];
    uint8_t udp_msg[7 * sizeof(float)];

    for (int index = 0; index < msg->pose_size(); index++) {
        if (msg->pose(index).name() == "robot") {
            robot_time = msg->time().sec() + msg->time().nsec() / 1e9;

            robot_pose[0] = msg->pose(index).position().x();
            robot_pose[1] = msg->pose(index).position().y();
            robot_pose[2] = msg->pose(index).position().z();

            robot_pose[3] = msg->pose(index).orientation().x();
            robot_pose[4] = msg->pose(index).orientation().y();
            robot_pose[5] = msg->pose(index).orientation().z();
            robot_pose[6] = msg->pose(index).orientation().w();

            std::cout << "[" << robot_time << "] Robot pose" << std::endl;

            memcpy(udp_msg, robot_pose, 7 * sizeof(float));
            client->send(udp_msg, 7 * sizeof(float));
        }
    }
}

int main(int argc, char **argv)
{
    // UDP client
    boost::asio::io_service io_service;
    client = new UDPClient(io_service, "localhost", "9998");

    // Gazebo client
#if GAZEBO_MAJOR_VERSION >= 6
    gazebo::client::setup(argc, argv);
#else
    gazebo::setupClient(argc, argv);
#endif

    gazebo::transport::NodePtr node(new gazebo::transport::Node());
    node->Init();

    gazebo::transport::SubscriberPtr robot_sub = node->Subscribe("~/pose/local/info", robot_callback);

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
