import pygame, sys, time, random
from main import *

class CardTypes(Card):
    super.__init__()
    def __init__(self, cardrole):
        self.role = cardrole


    def role(self):
        pass