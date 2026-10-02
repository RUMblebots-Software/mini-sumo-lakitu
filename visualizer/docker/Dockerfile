# Multi-arch base (was arm64v8/ubuntu): builds natively on Jetson (arm64) and WSL (amd64)
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV RCUTILS_COLORIZED_OUTPUT=1
ENV ROS_DOMAIN_ID=0
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    dbus-x11 \
    gpg \
    gnupg2 \
    htop \
    libgl1 \
    libgl1-mesa-dri \
    libglx-mesa0 \
    locales \
    lsb-release \
    mesa-utils \
    novnc \
    python3-argcomplete \
    software-properties-common \
    terminator \
    websockify \
    wget \
    x11-utils \
    x11vnc \
    xfce4 \
    xfce4-terminal \
    xauth \
    xvfb \
    && locale-gen en_US.UTF-8 \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# arch is detected at build time (arm64 on Jetson, amd64 on WSL)
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu jammy main" \
    > /etc/apt/sources.list.d/ros2.list

RUN apt-get update && apt-get install -y \
    python3-colcon-common-extensions \
    ros-humble-ackermann-msgs \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-ros-base \
    ros-humble-ros-gz \
    ros-humble-ros-gz-bridge \
    ros-humble-ros-gz-sim \
    ros-humble-rqt-graph \
    ros-humble-rviz2 \
    ros-humble-teleop-twist-keyboard \
    ros-humble-xacro \
    && rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc \
    && echo '[ -f /root/Documents/ros2_ws/install/setup.bash ] && source /root/Documents/ros2_ws/install/setup.bash' \
    >> /root/.bashrc \
    && echo "alias cb='cd /root/Documents/ros2_ws && colcon build --symlink-install && source install/setup.bash'" \
    >> /root/.bashrc \
    && echo "alias ws='source /root/Documents/ros2_ws/install/setup.bash'" \
    >> /root/.bashrc

COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

EXPOSE 6080

CMD ["/startup.sh"]