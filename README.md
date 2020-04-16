# WeBack integration for Home Assistant
Based on my [package](https://github.com/opravdin/weback-unofficial).  
This thing is in early development status and currently support just a limited amount of devices - only robot vacuums (probably only without VSLAM camera tracking).

## Configuration
If you use your phone number as username, type it like +{region}-{number}. Email login is not working for now
```yaml
weback:
    username: +7-1234567890
    password: <password>
```

## Supported devices
Tested on:
* Neatsvor X500
* Neatsvor V392
* Tesvor X500
* Concept VR3000  

This integration supports any device that mentioned as "_CLEAN_ROBOT" in Amazon's API. You can check it this way:  
```
pip install weback-unofficial
```
```python
from weback_unofficial.client import WebackApi

client = WebackApi("login", "password")
devices = client.device_list()
for device in devices:
    print(f"Checking device {device['Thing_Name']}")
    description = client.get_device_description(device["Thing_Name"])
    print(f"Device type is {description.get('thingTypeName')}")
```

## Custom commands
Currently you can publish message to device's MQTT topic.  
Read more about available messages in [API's repository](https://github.com/opravdin/weback-unofficial)
```yaml
entity_id: vacuum.robot_name
command: any_text_here
params:
  working_status: AutoClean
```

## Known issues
* Mopping control is not supported for now
* Library in polling based but I am 100% sure that it could handle MQTT messages from vacuum/weback server but don't know how to implement that :(
