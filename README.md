# NHC Image Retrieval
This is a simple tool to download images from the NOAA NHC website. Today, it retrieves the latest available "uncertainty track" for an active storm in the Atlantic hurricane basin.

## Installation
This library can be installed via `pip`:

```
pip install nhc-image-retrieval
```

### Usage

#### Home Assistant
I initially wrote this library for Home Assistant. I have an automation setup to read from the NHC RSS feeds already - now, when those are read from, my Home Assistant instance also downloads the latest "Uncertainty Track" from the NHC.

![alt text](examples/home_assistant_example.png)

This is possible using [AppDaemon](https://appdaemon.readthedocs.io/en/latest/index.html), which can be downloaded as a Home Assistant Add-On.

The example in `examples/home_assistant_appdaemon.py` shows the script I use in my Home Assistant instance.

#### General
For any generic application, I've also included an `examples/main.py` that shows basic usage & the downloading of the Uncertainty Track image.