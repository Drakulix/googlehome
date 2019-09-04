## Google Home Integration for Home-Assistant

### Fork of the original component before the [deprecation](https://github.com/home-assistant/home-assistant/pull/26035) with a workaround.

**Note**: Since sometime in June the [unofficial Google Home Local API](https://rithvikvibhu.github.io/GHLocalApi/) now [requires authentication](https://github.com/rithvikvibhu/GHLocalApi/issues/39#issuecomment-511214195). This broke the original integration. Optaining the necessary token requires a *rooted* android device. For every user having a spare device (or a VM) connected to their home-assistant you may use this custom_component. Tokens are automatically refreshed and extracted when outdated, the device needs to be always accessible and have the Google Home App installed.

### Configuration

```yaml
googlehome:
  adb_host: "<running adb server address, defaults to localhost>"
  adb_port: 5037 #default
  adb_device: my-android:5555 # device serial number (via usb) or host:port (via tcp)
  # config just like it used to be:
  # https://github.com/home-assistant/home-assistant.io/blob/d3ef85208ea08ba685dba4b23d34ffad0282a84d/source/_components/googlehome.markdown
  devices:
    - host: 192.168.178.67
      track_alarms: true
      track_devices: false
```

## License

The Project is Licensed under the Apache License just like the original home-assistant code.

The fork of the googledevices python lib is licensed under the MIT License just like the original.

I do only own the copyright on the patches to the original code, everything else is not mine.