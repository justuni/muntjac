
from muntjac.api import Link
from muntjac.ui.button import ClickEvent
from muntjac.ui.abstract_component import AbstractComponent
from muntjac.ui.component import Event


class ILinkActivatedListener(object):
    """ActiveLink click listener"""

    def linkActivated(self, event):
        """ActiveLink has been activated.

        @param event
                   ActiveLink click event.
        """
        raise NotImplementedError


_LINK_FOLLOWED_METHOD = getattr(ILinkActivatedListener, 'linkActivated')


class ActiveLink(Link):

    CLIENT_WIDGET = None #ClientWidget(VActiveLink)

    def __init__(self, caption=None, resource=None, targetName=None,
                width=None, height=None, border=None):
        self._listeners = set()

        if caption is None:
            super(ActiveLink, self).__init__()
        elif targetName is None:
            super(ActiveLink, self).__init__(caption, resource)
        else:
            super(ActiveLink, self).__init__(caption, resource, targetName,
                    width, height, border)


    def addListener(self, listener, iface):
        """Adds the link activated listener.

        @param listener
                   the Listener to be added.
        """
        if issubclass(iface, ILinkActivatedListener):
            self._listeners.add(listener)
            super(ActiveLink, self).registerListener(LinkActivatedEvent,
                    listener, _LINK_FOLLOWED_METHOD)
            if len(self._listeners) == 1:
                self.requestRepaint()
        else:
            super(ActiveLink, self).addListener(listener, iface)


    def addLinkActivatedListener(self, listener):
        self.addListener(listener, ILinkActivatedListener)


    def removeListener(self, listener, iface):
        """Removes the link activated listener.

        @param listener
                   the Listener to be removed.
        """
        if issubclass(iface, ILinkActivatedListener):
            self._listeners.remove(listener)
            super(ActiveLink, self).removeListener(ClickEvent, listener,
                    _LINK_FOLLOWED_METHOD)
            if len(self._listeners) == 0:
                self.requestRepaint()
        else:
            super(ActiveLink, self).removeListener(listener, iface)


    def removeLinkActivatedListener(self, listener):
        self.removeListener(listener, ILinkActivatedListener)


    def fireClick(self, linkOpened):
        """Emits the options change event."""
        self.fireEvent( LinkActivatedEvent(self, linkOpened) )


    def paintContent(self, target):
        super(ActiveLink, self).paintContent(target)
        if len(self._listeners) > 0:
            target.addVariable(self, 'activated', False)
            target.addVariable(self, 'opened', False)


    def changeVariables(self, source, variables):
        super(ActiveLink, self).changeVariables(source, variables)
        if not self.isReadOnly() and 'activated' in variables:
            activated = variables.get('activated')
            opened = variables.get('opened')
            if (activated is not None and bool(activated)
                    and not self.isReadOnly()):
                if (opened is not None) and bool(opened):
                    self.fireClick(True)
                else:
                    self.fireClick(False)


class LinkActivatedEvent(Event):

    def __init__(self, source, linkOpened):
        """New instance of text change event.

        @param source
                   the Source of the event.
        """
        super(LinkActivatedEvent, self).__init__(source)
        self._linkOpened = linkOpened


    def getActiveLink(self):
        """Gets the ActiveLink where the event occurred.

        @return the Source of the event.
        """
        return self.getSource()


    def isLinkOpened(self):
        """Indicates whether or not the link was opened on the client, i.e in a
        new window/tab. If the link was not opened, the listener should react
        to the event and "do something", otherwise the link does nothing.

        @return true if the link was opened on the client
        """
        return self._linkOpened
