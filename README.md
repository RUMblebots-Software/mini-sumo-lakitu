# mini-sumo-lakitu

## How to run the camera

Run this command on the Jetson host:

```bash
gst-launch-1.0 nvarguscamerasrc sensor-id=0 ! 'video/x-raw(memory:NVMM), width=1920, height=1080, framerate=30/1, format=NV12' ! nvvidconv flip-method=2 ! xvimagesink
```

Change `sensor-id` to `1` to use the other camera.

## Running ROS 2 in Docker

The image contains ROS 2 Humble, RViz2, and Gazebo Fortress.

### Jetson native desktop

Run this from a terminal in the Jetson's graphical desktop session:

```bash
cd ~/mini-sumo-lakitu/visualizer/docker
bash run.sh native
```

The launcher uses the desktop session's actual `DISPLAY`. The tested Jetson used `:1`; forcing `:0` targeted the wrong display. Native mode stops if `DISPLAY` is unset.

The launcher:

- Checks command failures, unset variables, and pipeline failures with `set -euo pipefail`.
- Switches to its own directory so Compose finds the configuration.
- Runs `xhost +si:localuser:root` on the host to let the container's root user open desktop windows. It stops if authorization fails.
- Builds and starts `robotics-native`, reusing cached build layers where possible.
- Creates `/tmp/runtime-root` inside the container with permissions `700` for Qt.
- Sources ROS Humble and the workspace setup, if the workspace has been built.
- Opens an interactive Bash shell. It does not launch RViz or Gazebo automatically.

The host's `visualizer/ros2_ws` directory is mounted at `/root/Documents/ros2_ws`. Type `exit` to leave the shell; the detached service stays running.

### Launch RViz or Gazebo inside the container

For RViz:

```bash
rviz2
```

The equivalent ROS command is `ros2 run rviz2 rviz2`. The executable is named `rviz2`, not `rviz`.

For a Gazebo sample world:

```bash
env -u QSG_RENDER_LOOP LIBGL_DRI3_DISABLE=1 ign gazebo shapes.sdf --render-engine ogre2
```

For your own world, substitute its path inside the container:

```bash
env -u QSG_RENDER_LOOP LIBGL_DRI3_DISABLE=1 ign gazebo /path/to/world.sdf --render-engine ogre2
```

Click **Play** in Gazebo to start the simulation. Fortress uses `ign gazebo`. On the tested CPU profile, Ogre 1 flickered and Qt's basic render loop did not fix it. Ogre 2 with `LIBGL_DRI3_DISABLE=1` produced a stable scene, but simulation was slow. This workaround applies to CPU mode; do not carry it into the GPU test below. See the [Gazebo Fortress troubleshooting documentation](https://gazebosim.org/docs/fortress/troubleshooting/).

### Jetson Nano GPU profile (hardware validation pending)

The separate `jetson-gpu` profile uses `Dockerfile.jetson-gpu`, based on the digest-pinned `dustynv/ros:humble-desktop-l4t-r32.7.1` image. Its tag was verified on Docker Hub, and ARM64 Fortress packages were verified in OSRF's Bionic and Focal package indexes. NVIDIA's forum identifies this Humble image for JetPack 4.6: [image reference](https://forums.developer.nvidia.com/t/ros2-humble-in-jetson-nano/302692/3).

This profile targets the Jetson Nano with L4T 32.7.1. It uses the NVIDIA runtime and installs Fortress through `ignition-tools` and `libignition-gazebo6-dev` for the base image's Ubuntu release. The latter pulls in the simulator plugins, GUI/QML dependencies, physics, and Ogre renderers. It does not mount the host's Tegra libraries manually or enable Mesa CPU-rendering overrides. The image build, NVIDIA rendering, and Gazebo simulation still need verification on the Jetson; registry and configuration checks alone do not prove GPU compatibility.

The GPU Dockerfile refreshes the base image's expired ROS signing key before its first APT update. It avoids the `ignition-fortress` metapackage because the Bionic ARM64 version requires an unavailable `python3-ignition-gazebo6` package. The direct package installation omits that Python API binding and checks that `ign gazebo --versions` reports version 6 during the build.

After copying these repository changes to the Jetson, run from its desktop terminal:

```bash
cd ~/mini-sumo-lakitu/visualizer/docker
bash run.sh jetson-gpu
```

The first build downloads the separate ROS image and Fortress packages. Before opening the shell, the launcher runs `glxinfo -B` and requires an NVIDIA OpenGL vendor. Expect an NVIDIA Tegra X1 renderer, not `llvmpipe`. If the check fails or crashes, keep the output for diagnosis; do not treat that run as GPU-ready.

Once the shell opens, launch applications manually:

```bash
rviz2
ign gazebo -v 4 shapes.sdf --render-engine ogre2
```

Run each application separately for the initial check. GPU rendering can improve the viewport and rendering-based sensors, while physics still uses CPU resources.

The GPU profile shares workspace source files but uses separate named volumes for `build`, `install`, and `log`. Rebuild your workspace inside this profile before using its packages; Ubuntu 22.04 build outputs are not reused. This initial profile provides Humble desktop and standalone Fortress, not all the extra Nav2 and ROS/Gazebo bridge packages from the CPU Dockerfile. Additional ROS packages may need source builds for this older base.

To stop the GPU service and return to the tested CPU setup, run on the host:

```bash
docker compose --profile jetson-gpu stop robotics-jetson-gpu
bash run.sh native
```

Default auto-detection still selects `native` on Jetson. GPU mode must be requested explicitly.

### Why native mode uses CPU rendering on the Jetson Nano

Testing used a Jetson Nano Developer Kit running L4T 32.7.1 and an Ubuntu 22.04 container. Host-side `glxinfo -B` reported NVIDIA Tegra X1 and OpenGL 4.6, confirming that the host GPU and display worked.

The container initially had X11 authorization errors. After authorization was corrected, it still could not find an RGB GLX visual or framebuffer configuration. Its library cache contained no NVIDIA GLX driver despite the NVIDIA runtime being active.

Manually exposing the host's Tegra libraries made `glxinfo` crash. A debugger backtrace placed the crash inside `libnvidia-glcore.so.32.7.1`, reached through `libGLX_nvidia.so.0`, before RViz started. This located the failure in the container's graphics stack; it did not prove the exact compatibility defect. An ARM64-compatible Ubuntu base image alone does not establish compatibility with the Nano's NVIDIA graphics libraries.

The working configuration bypasses NVIDIA's container runtime and uses Mesa software rendering:

```yaml
runtime: runc
environment:
  LIBGL_ALWAYS_SOFTWARE: "1"
  __GLX_VENDOR_LIBRARY_NAME: mesa
  QT_X11_NO_MITSHM: "1"
```

These settings are already in `docker-compose.yaml`, along with the display, runtime directory, workspace mount, and read-only X11 socket mount. Explicit `runtime: runc` also bypasses NVIDIA when it is Docker's default runtime. The earlier software-rendering attempt still used the NVIDIA runtime and failed; the test with `runc` succeeded.

RViz opens on the Jetson desktop, with rendering performed by the CPU. This configuration does not provide NVIDIA GPU acceleration; complex scenes and simulations can be slow. See [Mesa's rendering environment variables](https://docs.mesa3d.org/envvars.html).

To inspect the active renderer inside the container:

```bash
glxinfo -B
```

A software renderer such as `llvmpipe` is expected. RViz's `Stereo is NOT SUPPORTED` message alone does not indicate a startup failure.

### WSL and browser desktop

From the repository's `visualizer/docker` directory, select WSLg with:

```bash
bash run.sh wsl
```

Running `bash run.sh` without an argument detects WSL from `/proc/version`; otherwise it selects native mode. WSL keeps its separate D3D12/WSLg configuration.

To start the browser desktop:

```bash
bash run.sh web
```

Open [noVNC](http://localhost:6080/vnc.html) on the Docker host. For a remote Jetson, forward port 6080 over SSH from your computer, replacing `JETSON_HOST` with its hostname or IP:

```bash
ssh -N -L 6080:127.0.0.1:6080 rumblebots@JETSON_HOST
```

Then open the same noVNC URL on your computer. Web mode uses `startup.sh` to start Xvfb, XFCE, VNC, and noVNC. Native mode overrides that startup command with Bash.

Starting native mode does not stop an already running web service. To stop web mode while leaving native mode running, execute on the host from `visualizer/docker`:

```bash
docker compose --profile web stop robotics-web
```

To stop native mode:

```bash
docker compose --profile native stop robotics-native
```

### Launcher consolidation

`run-native.sh` was added during troubleshooting, then merged into the existing `run.sh` and removed. `run.sh` now contains its strict shell settings, native display check, X11 authorization, runtime-directory creation, and ROS environment setup, while retaining WSL and web support.

Use `bash run.sh native` instead of the old separate launcher or container-ID-based commands. A plain `docker exec ... bash` bypasses the launcher's host authorization and runtime-directory setup, and an old container may retain an outdated display or runtime configuration.
