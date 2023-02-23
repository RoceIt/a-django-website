from django.conf import settings

class ChoiceMenu():
    """A class to create menus for easy templating.

    """

    def __init__(self, name):
        self.name = name
        self.choices = dict()

    def add_item(self, name, action):
        self.choices[name] = action


MENU = ChoiceMenu(settings.MENU_NAME)
