# quietcool-homeassistant

This component integrates with the [QuietCool Python Library](https://github.com/bbrendon/quietcool-python) to control QuietCool fans from [Home Assistant](https://www.home-assistant.io/)

This is a fork of [stabbylambda/homeassistant-quietcool](https://github.com/stabbylambda/homeassistant-quietcool)


## Usage

Add the quietcool platform to the fan section of your configuration.yaml file:

```yaml
fan:
  - platform: quietcool
    host: 10.0.0.1 # Obviously you should change this to match the IP address of your own Master Hub
```

