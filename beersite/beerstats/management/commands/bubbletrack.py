"""
Count bubbles using GPIO sensors
"""
from django.core.management.base import BaseCommand
import RPi.GPIO as GPIO
from beerstats.models import Brew
from beerstats.models import Bubble


class Command(BaseCommand):

    """Track Some Bubbles"""

    help = 'Tracks bubbles on a specified GPIO port'

    @staticmethod
    def track_bubbles():
        """ busy loop
        :returns:

        """
        while True:
            pass

    @staticmethod
    def callback(channel):
        "Create a Bubble object when the gpio is falling"
        if GPIO.input(channel):
            print('rising on {}'.format(channel))
        else:
            brew = Brew.objects.filter(bubble_sensor_gpio=channel)[0]
            Bubble.objects.create(brew_id=brew.id)

    def setup_gpio_pins(self, gpio_pins):
        """Sets the pins specified in gpio_pins as input
        :gpio_pins: list of gpio pins
        """
        GPIO.setmode(GPIO.BCM)
        for gpio_port in gpio_pins:
            GPIO.setup(gpio_port, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(gpio_port, GPIO.BOTH, callback=self.callback)

    def handle(self, *args, **options):
        """handle bubbletrack
        :*args: Add later
        :**options: ..
        """
        gpio_pins = []
        for brew in Brew.objects.all():
            if brew.bubble_sensor_gpio and not brew.finished:
                gpio_pins.append(brew.bubble_sensor_gpio)

        if len(gpio_pins) > 0 and GPIO:
            self.setup_gpio_pins(gpio_pins)
            self.track_bubbles()
        else:
            exit()
