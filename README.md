# mini-sumo-lakitu

## How to run the camera
To run one of the cameras use this command:

```
gst-launch-1.0 nvarguscamerasrc sensor-id=0 ! 'video/x-raw(memory:NVMM), width=1920, height=1080, framerate=30/1, format=NV12' ! nvvidconv flip-method=2 ! xvimagesink

```
To change to the other camera change sensor-id to 1


## Running ROS2


### Depricated version, not deleted for the record
```docker compose --profile native build robotics-native

docker compose --profile native run --rm robotics-native


echo "$DISPLAY"
xhost +SI:localuser:root
docker exec -it -e DISPLAY="$DISPLAY" 1dd04db80e2b bash
```

### Updated Version

To run on wsl:

```
cd /path/to/your/folder
chmod +x run.sh startup.sh

# Build
docker compose --profile wsl build

# Build if needed, start, and open a shell
./run.sh
``` 

To run on Jetson (untested)

```
cd /path/to/your/folder
chmod +x run.sh startup.sh

# Build (slow the first time)
docker compose --profile native build        # or: docker-compose --profile native build

# Build if needed, start, and open a shell
./run.sh
``` 












xhost +si:localuser:root
ls
cd ~/mini-sumo-lakitu/visualizer/docker
docker compose exec -e DISPLAY="$DISPLAY" robotics-native bash -lc \
  'source /opt/ros/humble/setup.bash && rviz2'


echo "$DISPLAY"
xhost