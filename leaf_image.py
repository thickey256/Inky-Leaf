from PIL import Image, ImageDraw, ImageFont
from inky import InkyWHAT
import datetime

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

# Temp vars until I can hook up the Nissan API
# I need to get a leaf first
charge_percent = 1
charging = 1
charge_eta = '3h 35m'
distance = '1 Miles'

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
    clock = Image.open('img/clock.png').convert('RGBA')
    charge = Image.open('img/charging.png').convert('RGBA')
    charge = Image.alpha_composite(clock, charge)

    # add charge eta to text layer
    d.text((80,125), str(charge_eta), font=fnt, fill=(0,0,0,255))

#Add the current range
d.text((80,200), str(distance), font=fnt, fill=(0,0,0,255))

#Add the updated text
currentDT = datetime.datetime.now()
d.text((255,275), 'Updated: '+ str(currentDT.hour) + ':' + str(currentDT.minute), font=fnt_small, fill=(0,0,0,255))

#Base and battery image merge
out = Image.alpha_composite(base, battery)

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
