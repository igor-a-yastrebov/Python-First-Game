from dependency_injector import containers, providers

from player import Player
from eventhandler import EventHandler

class MainContainer(containers.DeclarativeContainer):
    player = providers.Singleton(Player)
    eventHandler = providers.Singleton(EventHandler)
