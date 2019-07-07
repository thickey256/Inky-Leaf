# Inky Leaf
![Image of Inky-Leaf](https://raw.githubusercontent.com/thickey256/Inky-Leaf/master/inky-leaf.png)
This project uses an eInk display ([an Inky wHAT Red](https://shop.pimoroni.com/products/inky-what)) to display the current status of a Nissan Leaf.

## Video of Inky-Leaf working
[![Inky-Leaf updating (and a cat)](http://img.youtube.com/vi/oBnODEGz_D8/0.jpg)](http://www.youtube.com/watch?v=oBnODEGz_D8 "Inky-Leaf updating (and a cat)")

## Software Requirements
I did try this with the latest version of Raspbain (Raspbian Buster) with no success, I don't think the Inky library has been updated to work with this yet. So you are better off using Stretch [archive here](http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-04-09/)

### installing python packages
This process should be quite simple, you just need a little bit of time as it's a bit slow downloading and installing everything.

#### Setting up the Pi
This stumped me for a while, it's made totally obvious in the docs but you need to enabled SPI and I2C on the Raspberry Pi (also do SSH!) using [raspi-config](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)

#### Inky wHAT package
You will need the Inky package, you can install this by running
```curl https://get.pimoroni.com/inky | bash```
and making yourself a cup of tea.
[You can and should have a play with the tutorial here](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-what)

#### Pycarwings2
This installs the library needed to talk to Nissan. (This may not work for your location, [take a look here for more up to date info.](https://github.com/jdhorne/pycarwings2/issues/35))
```pip install git+https://github.com/jdhorne/pycarwings2.git```

#### Config.ini
Now you just need to enter your login and password to the config file and you should be good to go.

### Making it run
So now everything is installed you want to see if this works.

#### Via the terminal
Simply type
```python ~/Inky-Leaf/inky-leaf.py```
and it should work

#### Via cron
You don't want to manually update the display yourself, I did think about putting a sleep command in the code so it keeps running but having it run once every 15 minutes seems like a better idea, that way updates will continue after reboots etc.

Load up the crontab with the command

```crontab -e```

Select nano as your editor if it asks (unless you want to use Vi)

Add the following line to the bottom of the page

```*/15 * * * * python ~/Inky-Leaf/inky-leaf.py >/dev/null 2>&1```

You can make it run more/less frequently but when charging it's not going to change that much so 15 minutes seems like a good place to have it.

Save and exit.. Job done!

I would love to know if someone else uses this, if so please let me know! thickey@thickey.com
