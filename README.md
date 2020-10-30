# WeBack integration for Home Assistant
Based on my [package](https://github.com/opravdin/weback-unofficial).  
This thing is in early development status and currently support just a limited amount of devices - only robot vacuums (probably only without VSLAM camera tracking).

## Configuration
If you use your phone number as username, type it like +{region}-{number}. Email login is working too - just place your email instead of number (like +7-abc@abc.com)

example telephone number: (+7)0123456789
```yaml
weback:
    username: +7-0123456789
    password: <password>
```

## Supported devices
Tested on:
* Neatsvor X500
* Neatsvor V392
* Tesvor X500
* Concept VR3000  
* Tesvor S6 (with map saving feature!)

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
## Zone cleaning
Zone cleaning setting is not that straightforwart, but you could set it with custom command feature. Check [this](https://github.com/opravdin/weback-unofficial/issues/7) discussion for more details.
You should manually send coordinates of your zone to vacuum cleaner. 

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
