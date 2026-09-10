# ============================================================
# ROS 2 Humble Development Environment for NVIDIA Jetson
# ============================================================

FROM ros:humble-ros-base-jammy

# Prevent interactive keyboard/timezone prompts
ENV DEBIAN_FRONTEND=noninteractive

# ROS environment
ENV RCUTILS_COLORIZED_OUTPUT=1
ENV ROS_DOMAIN_ID=0

# ============================================================
# Install ROS 2 packages + Desktop/GUI tools
# ============================================================

RUN apt-get update && apt-get install -y \
    # Desktop environment
    xfce4 \
    xfce4-terminal \
    terminator \
    \
    # VNC / Web GUI
    novnc \
    websockify \
    x11vnc \
    xvfb \
    \
    # Utilities
    htop \
    wget \
    gpg \
    apt-transport-https \
    \
    # OpenGL / Mesa
    libgl1 \
    libglx-mesa0 \
    libgl1-mesa-dri \
    mesa-utils \
    \
    # ROS 2
    ros-humble-xacro \
    ros-humble-ros-gz \
    ros-humble-ros-gz-sim \
    ros-humble-ros-gz-bridge \
    ros-humble-ackermann-msgs \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-teleop-twist-keyboard \
    \
    && rm -rf /var/lib/apt/lists/*

# ============================================================
# Install Microsoft VS Code
# ============================================================

RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | \
    gpg --dearmor > /tmp/packages.microsoft.gpg && \
    install -D -o root -g root -m 644 \
    /tmp/packages.microsoft.gpg \
    /etc/apt/keyrings/packages.microsoft.gpg && \
    echo "deb [arch=arm64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" \
    > /etc/apt/sources.list.d/vscode.list && \
    rm -f /tmp/packages.microsoft.gpg && \
    apt-get update && \
    apt-get install -y code && \
    rm -rf /var/lib/apt/lists/*

# ============================================================
# VS Code alias for running as root
# ============================================================

RUN echo "alias code='code --no-sandbox --user-data-dir=/root/.config/Code'" \
    >> /root/.bashrc

# ============================================================
# ROS 2 Workspace
# ============================================================

RUN mkdir -p /root/Documents/ros2_ws/src

# ============================================================
# Automatically source ROS 2 and workspace
# ============================================================

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc && \
    echo '[ -f /root/Documents/ros2_ws/install/setup.bash ] && source /root/Documents/ros2_ws/install/setup.bash' \
    >> /root/.bashrc && \
    echo '[ -f /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash ] && source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash' \
    >> /root/.bashrc

# ============================================================
# Development aliases
# ============================================================

RUN echo "alias cb='cd /root/Documents/ros2_ws && colcon build --symlink-install && source install/setup.bash'" \
    >> /root/.bashrc && \
    echo "alias cbp='cd /root/Documents/ros2_ws && colcon build --symlink-install --packages-select'" \
    >> /root/.bashrc && \
    echo "alias ws='source /root/Documents/ros2_ws/install/setup.bash'" \
    >> /root/.bashrc && \
    echo "alias killros='killall -9 gz-sim parameter_bridge rviz2 robot_state_publisher 2>/dev/null || true'" \
    >> /root/.bashrc && \
    echo "alias teleop='ros2 run teleop_twist_keyboard teleop_twist_keyboard'" \
    >> /root/.bashrc

# ============================================================
# Startup script
# ============================================================

COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

# ============================================================
# noVNC
# ============================================================

EXPOSE 6080

# ============================================================
# Start container
# ============================================================

CMD ["/startup.sh"]