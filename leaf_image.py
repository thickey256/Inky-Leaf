from PIL import Image, ImageDraw, ImageFont
from inky import InkyWHAT
import datetime
import pycarwings2
import time
from ConfigParser import SafeConfigParser
import logging
import sys
import math

# setup inky for display
inky_display = InkyWHAT("red")
inky_display.set_border(inky_display.RED)

# get an image
base = Image.open('img/base.png').convert('RGBA')

# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', base.size, (255,255,255,0))

# get a font
fnt = ImageFont.truetype('fonts/roboto/Roboto-Regular.ttf', 40)
fnt_small = ImageFont.truetype('fonts/roboto/Roboto-Regular.ttf', 20)

# get a drawing context
d = ImageDraw.Draw(txt)

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

parser = SafeConfigParser()
candidates = [ 'config.ini', 'my_config.ini' ]
found = parser.read(candidates)

username = parser.get('get-leaf-info', 'username')
password = parser.get('get-leaf-info', 'password')

s = pycarwings2.Session(username, password , "NE")
l = s.get_leaf()

leaf_info = l.get_latest_battery_status()

charge_percent = float(leaf_info.state_of_charge)

if leaf_info.charging_status == 'NOT_CHARGING':
	charging = 0
else:
	charging = 1

#How long to charge to 100%
charge_time_hours = leaf_info.answer["BatteryStatusRecords"]["TimeRequiredToFull200_6kW"]["HourRequiredToFull"]
charge_time_mins = leaf_info.answer["BatteryStatusRecords"]["TimeRequiredToFull200_6kW"]["MinutesRequiredToFull"]
if len(charge_time_mins) == 1:
	charge_time_mins = "0" + charge_time_mins
total_charge_time = charge_time_hours + ":" + charge_time_mins

#How much range is left?
range_in_km = float(leaf_info.answer["BatteryStatusRecords"]["CruisingRangeAcOn"]) / 1000
range_in_miles = range_in_km / 1.609
range_in_miles = math.ceil(range_in_miles)
range_in_miles = str(range_in_miles) + ' Miles'

#Which battery image do we want?
if charge_percent < 10:
    battery_img = 'battery_0.png';
elif charge_percent < 25:
    battery_img = 'battery_1.png';
elif charge_percent < 50:
    battery_img = 'battery_2.png';
elif charge_percent < 75:
    battery_img = 'battery_3.png';
else:
    battery_img = 'battery_4.png';

battery = Image.open('img/'+battery_img).convert('RGBA')

# add battery % to text layer
d.text((200,30), str(charge_percent) + '%', font=fnt, fill=(0,0,0,255))

#Do we want the charging image?
if charging == 1:
	charge = Image.open('img/charging.png').convert('RGBA')

# add charge eta to text layer
d.text((80,125), str(total_charge_time), font=fnt, fill=(0,0,0,255))

#Add the current range
d.text((80,200), str(range_in_miles), font=fnt, fill=(0,0,0,255))

#Add the updated text
d.text((10,275), 'Updated: '+ leaf_info.answer["BatteryStatusRecords"]["NotificationDateAndTime"], font=fnt_small, fill=(255,0,0,255))

#Base and battery image merge
out = Image.alpha_composite(base, battery)

#Merge the clock layer
clock = Image.open('img/clock.png').convert('RGBA')
out = Image.alpha_composite(out, clock)

#Merge the charging layer
if charging == 1:
    out = Image.alpha_composite(out, charge)

#Merge the text layer
out = Image.alpha_composite(out, txt)

# Convert the image to use a white / black / red colour palette
pal_img = Image.new("P", (1, 1))
pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

# Makes our image work with our pallet
img = out.convert("RGB").quantize(palette=pal_img)

# Displays the image
inky_display.set_image(img)
inky_display.show()
