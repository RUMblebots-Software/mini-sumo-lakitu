FROM osrf/ros:jazzy-desktop

# Prevents interactive keyboard and timezone prompts
ARG DEBIAN_FRONTEND=noninteractive

# Install desktop, virtual display, and VNC tools
RUN apt-get update && apt-get install -y \
    xfce4 \
    xfce4-terminal \
    novnc \
    websockify \
    x11vnc \
    xvfb \
    terminator \
    htop \
    ros-jazzy-ros-gz \ 
    ros-jazzy-xacro \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge \ 
    ros-jazzy-ackermann-msgs \
    libgl1 \ 
    libgl1 libglx-mesa0 \
    libgl1-mesa-dri \ 
    mesa-utils \
    ros-jazzy-navigation2 \
    ros-jazzy-nav2-bringup \
    && rm -rf /var/lib/apt/lists/*

# Install prerequisites for downloading VS Code
RUN apt-get update && apt-get install -y wget gpg apt-transport-https

run apt autoremove -y

# Add Microsoft's repository and install VS Code
RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg && \
    install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg && \
    sh -c 'echo "deb [arch=amd64,arm64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list' && \
    rm -f packages.microsoft.gpg && \
    apt-get update && apt-get install -y code && \
    rm -rf /var/lib/apt/lists/*

# Make a shortcut so VS Code runs properly as root
RUN echo "alias code='code --no-sandbox --user-data-dir=/root/.config/Code'" >> /root/.bashrc

# Copy startup script and make it executable
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

# Open the port for the web browser
EXPOSE 6080

RUN apt upgrade

# Setup ROS 2 environment, auto-sourcing, and development aliases in .bashrc
RUN cat << 'EOF' >> /root/.bashrc

# ==========================================
# ROS 2 & Simulation Development Environment
# ==========================================

# Sourcing ROS 2 & Workspace
source /opt/ros/jazzy/setup.bash
[ -f /root/Documents/ros2_ws/install/setup.bash ] && source /root/Documents/ros2_ws/install/setup.bash

# Colcon Autocomplete
[ -f /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash ] && source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash

# Environment Settings
export RCUTILS_COLORIZED_OUTPUT=1
export ROS_DOMAIN_ID=0

# Productivity Aliases
alias cb='cd /root/Documents/ros2_ws && colcon build --symlink-install && source install/setup.bash'
alias cbp='cd /root/Documents/ros2_ws && colcon build --symlink-install --packages-select'
alias ws='source /root/Documents/ros2_ws/install/setup.bash'
alias killros='killall -9 gz-sim parameter_bridge rviz2 robot_state_publisher 2>/dev/null || true'
alias teleop='ros2 run teleop_twist_keyboard teleop_twist_keyboard'

EOF

CMD ["/startup.sh"]