# Web IVI

![web_ivi_screenshot](web_ivi_screenshot.png)

The Demo Web IVI is a simple web application showing a three column layout with a speedometer in the first column, followed by a free to use info section and the torque meter as the third column. The intention is to provide you with a web based IVI that can be easily extended. The web IVI is intended to run inside the test vehicle and is used to display some information to the user during a drive. The web application is designed for simplicity, not for production use.

By default, the web backend receives vehicle dynamics data via the eCAL topic `vehicle_dynamics` (JSON) once a client browser connects to `http://127.0.0.1:5500`. The web backend passes the vehicle dynamics JSON to the client via [SSE (Server Side Event)](https://en.wikipedia.org/wiki/Server-sent_events). It extracts the current vehicle speed value `signals.speedDisplayed` from the JSON message and displays it within the speedometer. For simplicity, the torque-speed relationship is simulated within code.

The `div` with the id `info-screen` in `static/index.html` can be used to display custom information to the driver. Feel free to append data to it. If this does not suit your needs, you can also customise the whole Web IVI. Feel also free to extract and display any other relevant data from the vehicle dynamics JSON data.

## Build

For usage outside of the devcontainer as containerized application:

```shell
podman build -t web_ivi:latest -f .devcontainer/Dockerfile .
```

**Note:** Inside the test-vehicle the Web IVI will run on ARM-Platform. Test the build by running the command above and ask the hack coaches to build your finished image to run inside the test vehicle.

## Run

Start the Web IVI as containerized application:

```shell
podman run -it --rm --ipc=host --pid=host --network=host web_ivi:latest
```

Open the Google Chrome browser on `http://127.0.0.1:5500`.

**Note:** The app was tested on Google Chrome browser. Other browsers might not work.

In the test vehicle the Web IVI container image will be started and managed by Eclipse Ankaios. Finally, it will be displayed on a separate display within the test vehicle. So, please make sure the `podman build` and `podman run` command above will work after you have adapted the code.

## Development

### Run

Start the app inside the devcontainer for local development:

```shell
uvicorn main:app --port 5500 --reload
```

Open the Google Chrome browser on `http://127.0.0.1:5500`.

### Testing with mock data

Ask the hack coaches for an eCAL recording to play back a recorded driving scenario with eCAL and to receive the vehicle dynamics data in the Web IVI for development.

Place the downloaded eCAL recording in a `measurements/` folder next to the current file.

Start the eCAL recording within the devcontainer, replace `<recording_folder>` with the recording folder you received from the hack coaches:

```shell
ecal_play -m measurements/<recording_folder>
```

Start the Web IVI inside the devcontainer as shown above.

You should see logs of the JSON data received, and in the web browser the tachometer should show some speed values.

For debugging reasons you can start the eCAL Monitor terminal UI in a separate terminal window by running:

```shell
ecal_mon_tui
```

This lists all eCAL topics with their contents and meta information the host or container can see.