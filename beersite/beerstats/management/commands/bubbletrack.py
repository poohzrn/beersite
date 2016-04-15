from django.core.management.base import BaseCommand
from beerstats.models import Brew
from beerstats.models import Bubble
from random import randint
import time

try:
    import RPi.GPIO as GPIO
    DEBUG = False
except RuntimeError as e:
    DEBUG = True


class Command(BaseCommand):

    """Track Some Bubbles"""

    help = 'Tracks bubbles on a specified GPIO port'

    def track_bubbles(self):
        """TODO: Docstring for track_bubbles.
        :returns: TODO

        """
        while True:
            pass

    def callback(channel):
        # GPIO.wait_for_edge(channel, GPIO.FALLING)
        if GPIO.input(channel):
            print('rising on {}'.format(channel))
        else:
            brew = Brew.objects.filter(bubble_sensor_gpio=channel)[0]
            Bubble.objects.create(brew_id=brew.id)
            print('falling on {}; bubble added to \n {}'
                  .format(channel, brew.name))

    def setup_GPIO_pins(gpio_pins):
        """Sets the pins specified in gpio_pins as input
        :gpio_pins: list of gpio pins
        """
        GPIO.setmode(GPIO.BCM)
        for gpio_port in gpio_pins:
            GPIO.setup(gpio_port, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(gpio_port, GPIO.BOTH, callback=self.callback)

    def debug(self, gpio_pins):
        """TODO: Docstring for debug.
        :gpio_pins: TODO
        """
        while True:
            brew = Brew.objects.filter(bubble_sensor_gpio=23)[0]
            Bubble.objects.create(brew_id=brew.id)
            time.sleep(randint(0, 100))

    def handle(self, *args, **options):
        """TODO: handle bubbletrack
        :*args: Add later
        :**options: ..
        """
        gpio_pins = []
        for brew in Brew.objects.all():
            if(brew.bubble_sensor_gpio):
                gpio_pins.append(brew.bubble_sensor_gpio)
                print("Tracking pin {} for brew: {} ".
                      format(brew.bubble_sensor_gpio, brew.name))

        if gpio_pins and not DEBUG:
            self.setup_GPIO_pins(gpio_pins)
            self.track_bubbles()
        elif gpio_pins:
            self.debug(gpio_pins)
