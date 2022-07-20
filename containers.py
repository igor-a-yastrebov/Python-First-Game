from dependency_injector import containers, providers

from hero import Hero
from eventhandler import EventHandler

class MainContainer(containers.DeclarativeContainer):
    player = providers.Singleton(Hero)
    eventHandler = providers.Singleton(EventHandler)
