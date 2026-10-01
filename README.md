# mini-sumo-lakitu

## How to run the camera
To run one of the cameras use this command:

```
gst-launch-1.0 nvarguscamerasrc sensor-id=0 ! 'video/x-raw(memory:NVMM), width=1920, height=1080, framerate=30/1, format=NV12' ! nvvidconv flip-method=2 ! xvimagesink

```
To change to the other camera change sensor-id to 1


docker compose --profile native build robotics-native
docker compose --profile native run --rm robotics-native


echo "$DISPLAY"
xhost +SI:localuser:root
docker exec -it -e DISPLAY="$DISPLAY" 1dd04db80e2b bash