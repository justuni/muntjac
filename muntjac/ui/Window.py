# Copyright (C) 2011 Vaadin Ltd
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __pyjamas__ import (ARGERROR, POSTINC,)
from com.vaadin.event.ShortcutListener import (ShortcutListener,)
from com.vaadin.ui.Panel import (Panel,)
from com.vaadin.terminal.URIHandler import (URIHandler,)
from com.vaadin.terminal.gwt.client.ui.VView import (VView,)
from com.vaadin.terminal.ParameterHandler import (ParameterHandler,)
from com.vaadin.terminal.Sizeable import (Sizeable,)
# from java.io.Serializable import (Serializable,)
# from java.lang.reflect.Method import (Method,)
# from java.net.MalformedURLException import (MalformedURLException,)
# from java.net.URL import (URL,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Collections import (Collections,)
# from java.util.Iterator import (Iterator,)
# from java.util.LinkedHashSet import (LinkedHashSet,)
# from java.util.LinkedList import (LinkedList,)
# from java.util.Map import (Map,)
# from java.util.Set import (Set,)


class Window(Panel, URIHandler, ParameterHandler, FocusNotifier, BlurNotifier):
    """A component that represents an application (browser native) window or a sub
    window.
    <p>
    If the window is a application window or a sub window depends on how it is
    added to the application. Adding a {@code Window} to a {@code Window} using
    {@link Window#addWindow(Window)} makes it a sub window and adding a
    {@code Window} to the {@code Application} using
    {@link Application#addWindow(Window)} makes it an application window.
    </p>
    <p>
    An application window is the base of any view in a Vaadin application. All
    applications contain a main application window (set using
    {@link Application#setMainWindow(Window)} which is what is initially shown to
    the user. The contents of a window is set using
    {@link #setContent(ComponentContainer)}. The contents can in turn contain
    other components. For multi-tab applications there is one window instance per
    opened tab.
    </p>
    <p>
    A sub window is floating popup style window that can be added to an
    application window. Like the application window its content is set using
    {@link #setContent(ComponentContainer)}. A sub window can be positioned on
    the screen using absolute coordinates (pixels). The default content of the
    Window is set to be suitable for application windows. For sub windows it
    might be necessary to set the size of the content to work as expected.
    </p>
    <p>
    Window caption is displayed in the browser title bar for application level
    windows and in the window header for sub windows.
    </p>
    <p>
    Certain methods in this class are only meaningful for sub windows and other
    parts only for application windows. These are marked using <b>Sub window
    only</b> and <b>Application window only</b> respectively in the javadoc.
    </p>
    <p>
    Sub window is to be split into a separate component in Vaadin 7.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # <b>Application window only</b>. A border style used for opening resources
    # in a window without a border.

    BORDER_NONE = 0
    # <b>Application window only</b>. A border style used for opening resources
    # in a window with a minimal border.

    BORDER_MINIMAL = 1
    # <b>Application window only</b>. A border style that indicates that the
    # default border style should be used when opening resources.

    BORDER_DEFAULT = 2
    # <b>Application window only</b>. The user terminal for this window.
    _terminal = None
    # <b>Application window only</b>. The application this window is attached
    # to or null.

    _application = None
    # <b>Application window only</b>. List of URI handlers for this window.
    _uriHandlerList = None
    # <b>Application window only</b>. List of parameter handlers for this
    # window.

    _parameterHandlerList = None
    # <b>Application window only</b>. List of sub windows in this window. A sub
    # window cannot have other sub windows.

    _subwindows = LinkedHashSet()
    # <b>Application window only</b>. Explicitly specified theme of this window
    # or null if the application theme should be used.

    _theme = None
    # <b>Application window only</b>. Resources to be opened automatically on
    # next repaint. The list is automatically cleared when it has been sent to
    # the client.

    _openList = LinkedList()
    # <b>Application window only</b>. Unique name of the window used to
    # identify it.

    _name = None
    # <b>Application window only.</b> Border mode of the Window.
    _border = BORDER_DEFAULT
    # <b>Sub window only</b>. Top offset in pixels for the sub window (relative
    # to the parent application window) or -1 if unspecified.

    _positionY = -1
    # <b>Sub window only</b>. Left offset in pixels for the sub window
    # (relative to the parent application window) or -1 if unspecified.

    _positionX = -1
    # <b>Application window only</b>. A list of notifications that are waiting
    # to be sent to the client. Cleared (set to null) when the notifications
    # have been sent.

    _notifications = None
    # <b>Sub window only</b>. Modality flag for sub window.
    _modal = False
    # <b>Sub window only</b>. Controls if the end user can resize the window.
    _resizable = True
    # <b>Sub window only</b>. Controls if the end user can move the window by
    # dragging.

    _draggable = True
    # <b>Sub window only</b>. Flag which is true if the window is centered on
    # the screen.

    _centerRequested = False
    # Should resize recalculate layouts lazily (as opposed to immediately)
    _resizeLazy = False
    # Component that should be focused after the next repaint. Null if no focus
    # change should take place.

    _pendingFocus = None
    # <b>Application window only</b>. A list of javascript commands that are
    # waiting to be sent to the client. Cleared (set to null) when the commands
    # have been sent.

    _jsExecQueue = None
    # The component that should be scrolled into view after the next repaint.
    # Null if nothing should be scrolled into view.

    _scrollIntoView = None

    def __init__(self, *args):
        """Creates a new unnamed window with a default layout.
        ---
        Creates a new unnamed window with a default layout and given title.

        @param caption
                   the title of the window.
        ---
        Creates a new unnamed window with the given content and title.

        @param caption
                   the title of the window.
        @param content
                   the contents of the window
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__('', None)
        elif _1 == 1:
            caption, = _0
            self.__init__(caption, None)
        elif _1 == 2:
            caption, content = _0
            super(Window, self)(caption, content)
            self.setScrollable(True)
            self.setSizeUndefined()
        else:
            raise ARGERROR(0, 2)

    # (non-Javadoc)
    # 
    # @see com.vaadin.ui.Panel#addComponent(com.vaadin.ui.Component)

    def addComponent(self, c):
        if isinstance(c, Window):
            raise self.IllegalArgumentException('Window cannot be added to another via addComponent. ' + 'Use addWindow(Window) instead.')
        super(Window, self).addComponent(c)

    def getTerminal(self):
        """<b>Application window only</b>. Gets the user terminal.

        @return the user terminal
        """
        # *********************************************************************
        return self._terminal

    def getWindow(self):
        """Gets the parent window of the component.
        <p>
        This is always the window itself.
        </p>

        @see Component#getWindow()
        @return the window itself
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.AbstractComponent#getApplication()

        return self

    def getApplication(self):
        if self.getParent() is None:
            return self._application
        return self.getParent().getApplication()

    def getParent(self):
        """Gets the parent component of the window.

        <p>
        The parent of an application window is always null. The parent of a sub
        window is the application window the sub window is attached to.
        </p>

        @return the parent window
        @see Component#getParent()
        """
        # *********************************************************************
        return super(Window, self).getParent()

    def addURIHandler(self, handler):
        """<b>Application window only</b>. Adds a new URI handler to this window. If
        this is a sub window the URI handler is attached to the parent
        application window.

        @param handler
                   the URI handler to add.
        """
        if self.getParent() is not None:
            # this is subwindow, attach to main level instead
            # TODO hold internal list also and remove on detach
            mainWindow = self.getParent()
            mainWindow.addURIHandler(handler)
        else:
            if self._uriHandlerList is None:
                self._uriHandlerList = LinkedList()
            if not self._uriHandlerList.contains(handler):
                self._uriHandlerList.addLast(handler)

    def removeURIHandler(self, handler):
        """<b>Application window only</b>. Removes the URI handler from this window.
        If this is a sub window the URI handler is removed from the parent
        application window.

        @param handler
                   the URI handler to remove.
        """
        if self.getParent() is not None:
            # this is subwindow
            mainWindow = self.getParent()
            mainWindow.removeURIHandler(handler)
        else:
            if (handler is None) or (self._uriHandlerList is None):
                return
            self._uriHandlerList.remove(handler)
            if self._uriHandlerList.isEmpty():
                self._uriHandlerList = None

    def handleURI(self, context, relativeUri):
        """<b>Application window only</b>. Handles an URI by passing the URI to all
        URI handlers defined using {@link #addURIHandler(URIHandler)}. All URI
        handlers are called for each URI but no more than one handler may return
        a {@link DownloadStream}. If more than one stream is returned a
        {@code RuntimeException} is thrown.

        @param context
                   The URL of the application
        @param relativeUri
                   The URI relative to {@code context}
        @return A {@code DownloadStream} that one of the URI handlers returned,
                null if no {@code DownloadStream} was returned.
        """
        # *********************************************************************
        result = None
        if self._uriHandlerList is not None:
            handlers = list(self._uriHandlerList)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(handlers)):
                    break
                ds = handlers[i].handleURI(context, relativeUri)
                if ds is not None:
                    if result is not None:
                        raise RuntimeError('handleURI for ' + context + ' uri: \'' + relativeUri + '\' returns ambigious result.')
                    result = ds
        return result

    def addParameterHandler(self, handler):
        """<b>Application window only</b>. Adds a new parameter handler to this
        window. If this is a sub window the parameter handler is attached to the
        parent application window.

        @param handler
                   the parameter handler to add.
        """
        if self.getParent() is not None:
            # this is subwindow
            # TODO hold internal list also and remove on detach
            mainWindow = self.getParent()
            mainWindow.addParameterHandler(handler)
        else:
            if self._parameterHandlerList is None:
                self._parameterHandlerList = LinkedList()
            if not self._parameterHandlerList.contains(handler):
                self._parameterHandlerList.addLast(handler)

    def removeParameterHandler(self, handler):
        """<b>Application window only</b>. Removes the parameter handler from this
        window. If this is a sub window the parameter handler is removed from the
        parent application window.

        @param handler
                   the parameter handler to remove.
        """
        if self.getParent() is not None:
            # this is subwindow
            mainWindow = self.getParent()
            mainWindow.removeParameterHandler(handler)
        else:
            if (handler is None) or (self._parameterHandlerList is None):
                return
            self._parameterHandlerList.remove(handler)
            if self._parameterHandlerList.isEmpty():
                self._parameterHandlerList = None

    def handleParameters(self, parameters):
        """<b>Application window only</b>. Handles parameters by passing the
        parameters to all {@code ParameterHandler}s defined using
        {@link #addParameterHandler(ParameterHandler)}. All
        {@code ParameterHandler}s are called for each set of parameters.

        @param parameters
                   a map containing the parameter names and values
        @see ParameterHandler#handleParameters(Map)
        """
        # *********************************************************************
        if self._parameterHandlerList is not None:
            handlers = list(self._parameterHandlerList)
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(handlers)):
                    break
                handlers[i].handleParameters(parameters)

    def getTheme(self):
        """<b>Application window only</b>. Gets the theme for this window.
        <p>
        If the theme for this window is not explicitly set, the application theme
        name is returned. If the window is not attached to an application, the
        terminal default theme name is returned. If the theme name cannot be
        determined, null is returned
        </p>
        <p>
        Subwindows do not support themes and return the theme used by the parent
        window
        </p>

        @return the name of the theme used for the window
        """
        if self.getParent() is not None:
            return self.getParent().getTheme()
        if self._theme is not None:
            return self._theme
        if self._application is not None and self._application.getTheme() is not None:
            return self._application.getTheme()
        if self._terminal is not None:
            return self._terminal.getDefaultTheme()
        return None

    def setTheme(self, theme):
        """<b>Application window only</b>. Sets the name of the theme to use for
        this window. Changing the theme will cause the page to be reloaded.

        @param theme
                   the name of the new theme for this window or null to use the
                   application theme.
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.Panel#paintContent(com.vaadin.terminal.PaintTarget)

        if self.getParent() is not None:
            raise self.UnsupportedOperationException('Setting theme for sub-windows is not supported.')
        self._theme = theme
        self.requestRepaint()

    def paintContent(self, target):
        # Sets the window name
        # *********************************************************************
        name = self.getName()
        target.addAttribute('name', '' if name is None else name)
        # Sets the window theme
        theme = self.getTheme()
        target.addAttribute('theme', '' if theme is None else theme)
        if self._modal:
            target.addAttribute('modal', True)
        if self._resizable:
            target.addAttribute('resizable', True)
        if self._resizeLazy:
            target.addAttribute(VView.RESIZE_LAZY, self._resizeLazy)
        if not self._draggable:
            # Inverted to prevent an extra attribute for almost all sub windows
            target.addAttribute('fixedposition', True)
        if self._bringToFront is not None:
            target.addAttribute('bringToFront', self._bringToFront.intValue())
            self._bringToFront = None
        if self._centerRequested:
            target.addAttribute('center', True)
            self._centerRequested = False
        if self._scrollIntoView is not None:
            target.addAttribute('scrollTo', self._scrollIntoView)
            self._scrollIntoView = None
        # Marks the main window
        if (
            self.getApplication() is not None and self == self.getApplication().getMainWindow()
        ):
            target.addAttribute('main', True)
        if self.getContent() is not None:
            if self.getContent().getHeightUnits() == Sizeable.UNITS_PERCENTAGE:
                target.addAttribute('layoutRelativeHeight', True)
            if self.getContent().getWidthUnits() == Sizeable.UNITS_PERCENTAGE:
                target.addAttribute('layoutRelativeWidth', True)
        # Open requested resource
        if not self._openList.isEmpty():
            _0 = True
            i = self._openList
            while True:
                if _0 is True:
                    _0 = False
                if not i.hasNext():
                    break
                i.next().paintContent(target)
            self._openList.clear()
        # Contents of the window panel is painted
        super(Window, self).paintContent(target)
        # Add executable javascripts if needed
        if self._jsExecQueue is not None:
            for script in self._jsExecQueue:
                target.startTag('execJS')
                target.addAttribute('script', script)
                target.endTag('execJS')
            self._jsExecQueue = None
        # Window position
        target.addVariable(self, 'positionx', self.getPositionX())
        target.addVariable(self, 'positiony', self.getPositionY())
        # Window closing
        target.addVariable(self, 'close', False)
        if self.getParent() is None:
            # Paint subwindows
            _1 = True
            i = self._subwindows
            while True:
                if _1 is True:
                    _1 = False
                if not i.hasNext():
                    break
                w = i.next()
                w.paint(target)
        else:
            # mark subwindows
            target.addAttribute('sub', True)
        # Paint notifications
        if self._notifications is not None:
            target.startTag('notifications')
            _2 = True
            it = self._notifications
            while True:
                if _2 is True:
                    _2 = False
                if not it.hasNext():
                    break
                n = it.next()
                target.startTag('notification')
                if n.getCaption() is not None:
                    target.addAttribute('caption', n.getCaption())
                if n.getMessage() is not None:
                    target.addAttribute('message', n.getMessage())
                if n.getIcon() is not None:
                    target.addAttribute('icon', n.getIcon())
                target.addAttribute('position', n.getPosition())
                target.addAttribute('delay', n.getDelayMsec())
                if n.getStyleName() is not None:
                    target.addAttribute('style', n.getStyleName())
                target.endTag('notification')
            target.endTag('notifications')
            self._notifications = None
        if self._pendingFocus is not None:
            # ensure focused component is still attached to this main window
            if (
                (self._pendingFocus.getWindow() == self) or (self._pendingFocus.getWindow() is not None and self._pendingFocus.getWindow().getParent() == self)
            ):
                target.addAttribute('focused', self._pendingFocus)
            self._pendingFocus = None

    def scrollIntoView(self, component):
        """Scrolls any component between the component and window to a suitable
        position so the component is visible to the user. The given component
        must be inside this window.

        @param component
                   the component to be scrolled into view
        @throws IllegalArgumentException
                    if {@code component} is not inside this window
        """
        if component.getWindow() != self:
            raise self.IllegalArgumentException('The component where to scroll must be inside this window.')
        self._scrollIntoView = component
        self.requestRepaint()

    def open(self, *args):
        """Opens the given resource in this window. The contents of this Window is
        replaced by the {@code Resource}.

        @param resource
                   the resource to show in this window
        ---
        Opens the given resource in a window with the given name.
        <p>
        The supplied {@code windowName} is used as the target name in a
        window.open call in the client. This means that special values such as
        "_blank", "_self", "_top", "_parent" have special meaning. An empty or
        <code>null</code> window name is also a special case.
        </p>
        <p>
        "", null and "_self" as {@code windowName} all causes the resource to be
        opened in the current window, replacing any old contents. For
        downloadable content you should avoid "_self" as "_self" causes the
        client to skip rendering of any other changes as it considers them
        irrelevant (the page will be replaced by the resource). This can speed up
        the opening of a resource, but it might also put the client side into an
        inconsistent state if the window content is not completely replaced e.g.,
        if the resource is downloaded instead of displayed in the browser.
        </p>
        <p>
        "_blank" as {@code windowName} causes the resource to always be opened in
        a new window or tab (depends on the browser and browser settings).
        </p>
        <p>
        "_top" and "_parent" as {@code windowName} works as specified by the HTML
        standard.
        </p>
        <p>
        Any other {@code windowName} will open the resource in a window with that
        name, either by opening a new window/tab in the browser or by replacing
        the contents of an existing window with that name.
        </p>

        @param resource
                   the resource.
        @param windowName
                   the name of the window.
        ---
        Opens the given resource in a window with the given size, border and
        name. For more information on the meaning of {@code windowName}, see
        {@link #open(Resource, String)}.

        @param resource
                   the resource.
        @param windowName
                   the name of the window.
        @param width
                   the width of the window in pixels
        @param height
                   the height of the window in pixels
        @param border
                   the border style of the window. See {@link #BORDER_NONE
                   Window.BORDER_* constants}
        """
        # *********************************************************************
        _0 = args
        _1 = len(args)
        if _1 == 1:
            resource, = _0
            if not self._openList.contains(resource):
                self._openList.add(self.OpenResource(resource, None, -1, -1, self.BORDER_DEFAULT))
            self.requestRepaint()
        elif _1 == 2:
            resource, windowName = _0
            if not self._openList.contains(resource):
                self._openList.add(self.OpenResource(resource, windowName, -1, -1, self.BORDER_DEFAULT))
            self.requestRepaint()
        elif _1 == 5:
            resource, windowName, width, height, border = _0
            if not self._openList.contains(resource):
                self._openList.add(self.OpenResource(resource, windowName, width, height, border))
            self.requestRepaint()
        else:
            raise ARGERROR(1, 5)

    # *********************************************************************

    def getURL(self):
        """Gets the full URL of the window. The returned URL is window specific and
        can be used to directly refer to the window.
        <p>
        Note! This method can not be used for portlets.
        </p>

        @return the URL of the window or null if the window is not attached to an
                application
        """
        if self._application is None:
            return None
        try:
            return URL(self._application.getURL(), self.getName() + '/')
        except MalformedURLException, e:
            raise RuntimeError('Internal problem getting window URL, please report')

    def getName(self):
        """<b>Application window only</b>. Gets the unique name of the window. The
        name of the window is used to uniquely identify it.
        <p>
        The name also determines the URL that can be used for direct access to a
        window. All windows can be accessed through
        {@code http://host:port/app/win} where {@code http://host:port/app} is
        the application URL (as returned by {@link Application#getURL()} and
        {@code win} is the window name.
        </p>
        <p>
        Note! Portlets do not support direct window access through URLs.
        </p>

        @return the Name of the Window.
        """
        return self._name

    def getBorder(self):
        """Returns the border style of the window.

        @see #setBorder(int)
        @return the border style for the window
        """
        return self._border

    def setBorder(self, border):
        """Sets the border style for this window. Valid values are
        {@link Window#BORDER_NONE}, {@link Window#BORDER_MINIMAL},
        {@link Window#BORDER_DEFAULT}.
        <p>
        <b>Note!</b> Setting this seems to currently have no effect whatsoever on
        the window.
        </p>

        @param border
                   the border style to set
        """
        self._border = border

    def setApplication(self, application):
        """Sets the application this window is attached to.

        <p>
        This method is called by the framework and should not be called directly
        from application code. {@link com.vaadin.Application#addWindow(Window)}
        should be used to add the window to an application and
        {@link com.vaadin.Application#removeWindow(Window)} to remove the window
        from the application.
        </p>
        <p>
        This method invokes {@link Component#attach()} and
        {@link Component#detach()} methods when necessary.
        <p>

        @param application
                   the application the window is attached to
        """
        # If the application is not changed, dont do nothing
        if application == self._application:
            return
        # Sends detach event if the window is connected to application
        if self._application is not None:
            self.detach()
        # Connects to new parent
        self._application = application
        # Sends the attach event if connected to a window
        if application is not None:
            self.attach()

    def setName(self, name):
        """<b>Application window only</b>. Sets the unique name of the window. The
        name of the window is used to uniquely identify it inside the
        application.
        <p>
        The name also determines the URL that can be used for direct access to a
        window. All windows can be accessed through
        {@code http://host:port/app/win} where {@code http://host:port/app} is
        the application URL (as returned by {@link Application#getURL()} and
        {@code win} is the window name.
        </p>
        <p>
        This method can only be called before the window is added to an
        application.
        </p>
        <p>
        Note! Portlets do not support direct window access through URLs.
        </p>

        @param name
                   the new name for the window or null if the application should
                   automatically assign a name to it
        @throws IllegalStateException
                    if the window is attached to an application
        """
        # The name can not be changed in application
        if self.getApplication() is not None:
            raise self.IllegalStateException('Window name can not be changed while ' + 'the window is in application')
        self._name = name

    def setTerminal(self, type):
        """Sets the user terminal. Used by the terminal adapter, should never be
        called from application code.

        @param type
                   the terminal to set.
        """
        self._terminal = type

    class OpenResource(Serializable):
        """Private class for storing properties related to opening resources."""
        # The resource to open
        # (non-Javadoc)
        # 
        # @see com.vaadin.ui.Panel#changeVariables(java.lang.Object, java.util.Map)

        _resource = None
        # The name of the target window
        _name = None
        # The width of the target window
        _width = None
        # The height of the target window
        _height = None
        # The border style of the target window
        _border = None

        def __init__(self, resource, name, width, height, border):
            """Creates a new open resource.

            @param resource
                       The resource to open
            @param name
                       The name of the target window
            @param width
                       The width of the target window
            @param height
                       The height of the target window
            @param border
                       The border style of the target window
            """
            self._resource = resource
            self._name = name
            self._width = width
            self._height = height
            self._border = border

        def paintContent(self, target):
            """Paints the open request. Should be painted inside the window.

            @param target
                       the paint target
            @throws PaintException
                        if the paint operation fails
            """
            target.startTag('open')
            target.addAttribute('src', self._resource)
            if self._name is not None and len(self._name) > 0:
                target.addAttribute('name', self._name)
            if self._width >= 0:
                target.addAttribute('width', self._width)
            if self._height >= 0:
                target.addAttribute('height', self._height)
            _0 = self._border
            _1 = False
            while True:
                if _0 == Window.BORDER_MINIMAL:
                    _1 = True
                    target.addAttribute('border', 'minimal')
                    break
                if (_1 is True) or (_0 == Window.BORDER_NONE):
                    _1 = True
                    target.addAttribute('border', 'none')
                    break
                break
            target.endTag('open')

    def changeVariables(self, source, variables):
        sizeHasChanged = False
        # size is handled in super class, but resize events only in windows ->
        # so detect if size change occurs before super.changeVariables()
        if (
            'height' in variables and (self.getHeightUnits() != self.UNITS_PIXELS) or (variables['height'] != self.getHeight())
        ):
            sizeHasChanged = True
        if (
            'width' in variables and (self.getWidthUnits() != self.UNITS_PIXELS) or (variables['width'] != self.getWidth())
        ):
            sizeHasChanged = True
        super(Window, self).changeVariables(source, variables)
        # Positioning
        positionx = variables['positionx']
        if positionx is not None:
            x = positionx.intValue()
            # This is information from the client so it is already using the
            # position. No need to repaint.
            self.setPositionX(-1 if x < 0 else x, False)
        positiony = variables['positiony']
        if positiony is not None:
            y = positiony.intValue()
            # This is information from the client so it is already using the
            # position. No need to repaint.
            self.setPositionY(-1 if y < 0 else y, False)
        if self.isClosable():
            # Closing
            close = variables['close']
            if close is not None and close.booleanValue():
                close()
        # fire event if size has really changed
        if sizeHasChanged:
            self.fireResize()
        if self.FocusEvent.EVENT_ID in variables:
            self.fireEvent(self.FocusEvent(self))
        elif self.BlurEvent.EVENT_ID in variables:
            self.fireEvent(self.BlurEvent(self))

    def close(self):
        """Method that handles window closing (from UI).

        <p>
        By default, sub-windows are removed from their respective parent windows
        and thus visually closed on browser-side. Browser-level windows also
        closed on the client-side, but they are not implicitly removed from the
        application.
        </p>

        <p>
        To explicitly close a sub-window, use {@link #removeWindow(Window)}. To
        react to a window being closed (after it is closed), register a
        {@link CloseListener}.
        </p>
        """
        parent = self.getParent()
        if parent is None:
            self.fireClose()
        else:
            # focus is restored to the parent window
            parent.focus()
            # subwindow is removed from parent
            parent.removeWindow(self)

    def getPositionX(self):
        """Gets the distance of Window left border in pixels from left border of the
        containing (main window).

        @return the Distance of Window left border in pixels from left border of
                the containing (main window). or -1 if unspecified.
        @since 4.0.0
        """
        return self._positionX

    def setPositionX(self, *args):
        """Sets the distance of Window left border in pixels from left border of the
        containing (main window).

        @param positionX
                   the Distance of Window left border in pixels from left border
                   of the containing (main window). or -1 if unspecified.
        @since 4.0.0
        ---
        Sets the distance of Window left border in pixels from left border of the
        containing (main window).

        @param positionX
                   the Distance of Window left border in pixels from left border
                   of the containing (main window). or -1 if unspecified.
        @param repaintRequired
                   true if the window needs to be repainted, false otherwise
        @since 6.3.4
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            positionX, = _0
            self.setPositionX(positionX, True)
        elif _1 == 2:
            positionX, repaintRequired = _0
            self._positionX = positionX
            self._centerRequested = False
            if repaintRequired:
                self.requestRepaint()
        else:
            raise ARGERROR(1, 2)

    def getPositionY(self):
        """Gets the distance of Window top border in pixels from top border of the
        containing (main window).

        @return Distance of Window top border in pixels from top border of the
                containing (main window). or -1 if unspecified .

        @since 4.0.0
        """
        return self._positionY

    def setPositionY(self, *args):
        """Sets the distance of Window top border in pixels from top border of the
        containing (main window).

        @param positionY
                   the Distance of Window top border in pixels from top border of
                   the containing (main window). or -1 if unspecified

        @since 4.0.0
        ---
        Sets the distance of Window top border in pixels from top border of the
        containing (main window).

        @param positionY
                   the Distance of Window top border in pixels from top border of
                   the containing (main window). or -1 if unspecified
        @param repaintRequired
                   true if the window needs to be repainted, false otherwise

        @since 6.3.4
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            positionY, = _0
            self.setPositionY(positionY, True)
        elif _1 == 2:
            positionY, repaintRequired = _0
            self._positionY = positionY
            self._centerRequested = False
            if repaintRequired:
                self.requestRepaint()
        else:
            raise ARGERROR(1, 2)

    _WINDOW_CLOSE_METHOD = None
    # This should never happen
    try:
        _WINDOW_CLOSE_METHOD = self.CloseListener.getDeclaredMethod('windowClose', [self.CloseEvent])
    except java.lang.NoSuchMethodException, e:
        raise java.lang.RuntimeException('Internal error, window close method not found')

    class CloseEvent(Component.Event):

        def __init__(self, source):
            """@param source"""
            super(CloseEvent, self)(source)

        def getWindow(self):
            """Gets the Window.

            @return the window.
            """
            return self.getSource()

    class CloseListener(Serializable):
        """An interface used for listening to Window close events. Add the
        CloseListener to a browser level window or a sub window and
        {@link CloseListener#windowClose(CloseEvent)} will be called whenever the
        user closes the window.

        <p>
        Since Vaadin 6.5, removing windows using {@link #removeWindow(Window)}
        does fire the CloseListener.
        </p>
        """

        def windowClose(self, e):
            """Called when the user closes a window. Use
            {@link CloseEvent#getWindow()} to get a reference to the
            {@link Window} that was closed.

            @param e
                       Event containing
            """
            pass

    def addListener(self, *args):
        """Adds a CloseListener to the window.

        For a sub window the CloseListener is fired when the user closes it
        (clicks on the close button).

        For a browser level window the CloseListener is fired when the browser
        level window is closed. Note that closing a browser level window does not
        mean it will be destroyed.

        <p>
        Since Vaadin 6.5, removing windows using {@link #removeWindow(Window)}
        does fire the CloseListener.
        </p>

        @param listener
                   the CloseListener to add.
        ---
        Add a resize listener.

        @param listener
        ---
        Note, that focus/blur listeners in Window class are only supported by sub
        windows. Also note that Window is not considered focused if its contained
        component currently has focus.

        @see com.vaadin.event.FieldEvents.FocusNotifier#addListener(com.vaadin.event.FieldEvents.FocusListener)
        ---
        Note, that focus/blur listeners in Window class are only supported by sub
        windows. Also note that Window is not considered focused if its contained
        component currently has focus.

        @see com.vaadin.event.FieldEvents.BlurNotifier#addListener(com.vaadin.event.FieldEvents.BlurListener)
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BlurListener):
                listener, = _0
                self.addListener(self.BlurEvent.EVENT_ID, self.BlurEvent, listener, self.BlurListener.blurMethod)
            elif isinstance(_0[0], CloseListener):
                listener, = _0
                self.addListener(self.CloseEvent, listener, self._WINDOW_CLOSE_METHOD)
            elif isinstance(_0[0], FocusListener):
                listener, = _0
                self.addListener(self.FocusEvent.EVENT_ID, self.FocusEvent, listener, self.FocusListener.focusMethod)
            else:
                listener, = _0
                self.addListener(self.ResizeEvent, listener, self._WINDOW_RESIZE_METHOD)
        else:
            raise ARGERROR(1, 1)

    def removeListener(self, *args):
        """Removes the CloseListener from the window.

        <p>
        For more information on CloseListeners see {@link CloseListener}.
        </p>

        @param listener
                   the CloseListener to remove.
        ---
        Remove a resize listener.

        @param listener
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BlurListener):
                listener, = _0
                self.removeListener(self.BlurEvent.EVENT_ID, self.BlurEvent, listener)
            elif isinstance(_0[0], CloseListener):
                listener, = _0
                self.removeListener(self.CloseEvent, listener, self._WINDOW_CLOSE_METHOD)
            elif isinstance(_0[0], FocusListener):
                listener, = _0
                self.removeListener(self.FocusEvent.EVENT_ID, self.FocusEvent, listener)
            else:
                listener, = _0
                self.removeListener(self.ResizeEvent, listener)
        else:
            raise ARGERROR(1, 1)

    def fireClose(self):
        # Method for the resize event.
        self.fireEvent(Window.CloseEvent(self))

    _WINDOW_RESIZE_METHOD = None
    # This should never happen
    try:
        _WINDOW_RESIZE_METHOD = self.ResizeListener.getDeclaredMethod('windowResized', [self.ResizeEvent])
    except java.lang.NoSuchMethodException, e:
        raise java.lang.RuntimeException('Internal error, window resized method not found')

    class ResizeEvent(Component.Event):
        """Resize events are fired whenever the client-side fires a resize-event
        (e.g. the browser window is resized). The frequency may vary across
        browsers.
        """

        def __init__(self, source):
            """@param source"""
            super(ResizeEvent, self)(source)

        def getWindow(self):
            """Get the window form which this event originated

            @return the window
            """
            return self.getSource()

    class ResizeListener(Serializable):
        """Listener for window resize events.

        @see com.vaadin.ui.Window.ResizeEvent
        """

        def windowResized(self, e):
            pass

    def fireResize(self):
        """Fire the resize event."""
        self.fireEvent(self.ResizeEvent(self))

    def attachWindow(self, w):
        self._subwindows.add(w)
        w.setParent(self)
        self.requestRepaint()

    def addWindow(self, window):
        """Adds a window inside another window.

        <p>
        Adding windows inside another window creates "subwindows". These windows
        should not be added to application directly and are not accessible
        directly with any url. Addding windows implicitly sets their parents.
        </p>

        <p>
        Only one level of subwindows are supported. Thus you can add windows
        inside such windows whose parent is <code>null</code>.
        </p>

        @param window
        @throws IllegalArgumentException
                    if a window is added inside non-application level window.
        @throws NullPointerException
                    if the given <code>Window</code> is <code>null</code>.
        """
        if window is None:
            raise self.NullPointerException('Argument must not be null')
        if window.getApplication() is not None:
            raise self.IllegalArgumentException('Window was already added to application' + ' - it can not be added to another window also.')
        elif self.getParent() is not None:
            raise self.IllegalArgumentException('You can only add windows inside application-level windows.')
        elif len(window.subwindows) > 0:
            raise self.IllegalArgumentException('Only one level of subwindows are supported.')
        self.attachWindow(window)

    def removeWindow(self, window):
        """Remove the given subwindow from this window.

        Since Vaadin 6.5, {@link CloseListener}s are called also when explicitly
        removing a window by calling this method.

        Since Vaadin 6.5, returns a boolean indicating if the window was removed
        or not.

        @param window
                   Window to be removed.
        @return true if the subwindow was removed, false otherwise
        """
        if not self._subwindows.remove(window):
            # Window window is not a subwindow of this window.
            return False
        window.setParent(None)
        window.fireClose()
        self.requestRepaint()
        return True

    _bringToFront = None
    # This sequesnce is used to keep the right order of windows if multiple
    # windows are brought to front in a single changeset. Incremented and saved
    # by childwindows. If sequence is not used, the order is quite random
    # (depends on the order getting to dirty list. e.g. which window got
    # variable changes).

    _bringToFrontSequence = 0

    def bringToFront(self):
        """If there are currently several sub windows visible, calling this method
        makes this window topmost.
        <p>
        This method can only be called if this window is a sub window and
        connected a top level window. Else an illegal state exception is thrown.
        Also if there are modal windows and this window is not modal, and illegal
        state exception is thrown.
        <p>
        <strong> Note, this API works on sub windows only. Browsers can't reorder
        OS windows.</strong>
        """
        parent = self.getParent()
        if parent is None:
            raise self.IllegalStateException('Window must be attached to parent before calling bringToFront method.')
        for w in parent.getChildWindows():
            if w.isModal() and not self.isModal():
                raise self.IllegalStateException('There are modal windows currently visible, non-modal window cannot be brought to front.')
        self._bringToFront = POSTINC(self.getParent().bringToFrontSequence)
        self.requestRepaint()

    def getChildWindows(self):
        """Get the set of all child windows.

        @return Set of child windows.
        """
        return Collections.unmodifiableSet(self._subwindows)

    def setModal(self, modality):
        """Sets sub-window modal, so that widgets behind it cannot be accessed.
        <b>Note:</b> affects sub-windows only.

        @param modality
                   true if modality is to be turned on
        """
        self._modal = modality
        self.center()
        self.requestRepaint()

    def isModal(self):
        """@return true if this window is modal."""
        return self._modal

    def setResizable(self, resizeability):
        """Sets sub-window resizable. <b>Note:</b> affects sub-windows only.

        @param resizable
                   true if resizability is to be turned on
        """
        self._resizable = resizeability
        self.requestRepaint()

    def isResizable(self):
        """@return true if window is resizable by the end-user, otherwise false."""
        return self._resizable

    def isResizeLazy(self):
        """@return true if a delay is used before recalculating sizes, false if
                sizes are recalculated immediately.
        """
        return self._resizeLazy

    def setResizeLazy(self, resizeLazy):
        """Should resize operations be lazy, i.e. should there be a delay before
        layout sizes are recalculated. Speeds up resize operations in slow UIs
        with the penalty of slightly decreased usability.

        Note, some browser send false resize events for the browser window and
        are therefore always lazy.

        @param resizeLazy
                   true to use a delay before recalculating sizes, false to
                   calculate immediately.
        """
        self._resizeLazy = resizeLazy
        self.requestRepaint()

    def center(self):
        """Request to center this window on the screen. <b>Note:</b> affects
        sub-windows only.
        """
        self._centerRequested = True
        self.requestRepaint()

    def showNotification(self, *args):
        """Shows a notification message on the middle of the window. The message
        automatically disappears ("humanized message").

        @see #showNotification(com.vaadin.ui.Window.Notification)
        @see Notification

        @param caption
                   The message
        ---
        Shows a notification message the window. The position and behavior of the
        message depends on the type, which is one of the basic types defined in
        {@link Notification}, for instance Notification.TYPE_WARNING_MESSAGE.

        @see #showNotification(com.vaadin.ui.Window.Notification)
        @see Notification

        @param caption
                   The message
        @param type
                   The message type
        ---
        Shows a notification consisting of a bigger caption and a smaller
        description on the middle of the window. The message automatically
        disappears ("humanized message").

        @see #showNotification(com.vaadin.ui.Window.Notification)
        @see Notification

        @param caption
                   The caption of the message
        @param description
                   The message description
        ---
        Shows a notification consisting of a bigger caption and a smaller
        description. The position and behavior of the message depends on the
        type, which is one of the basic types defined in {@link Notification},
        for instance Notification.TYPE_WARNING_MESSAGE.

        @see #showNotification(com.vaadin.ui.Window.Notification)
        @see Notification

        @param caption
                   The caption of the message
        @param description
                   The message description
        @param type
                   The message type
        ---
        Shows a notification message.

        @see Notification
        @see #showNotification(String)
        @see #showNotification(String, int)
        @see #showNotification(String, String)
        @see #showNotification(String, String, int)

        @param notification
                   The notification message to show
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Notification):
                notification, = _0
                self.addNotification(notification)
            else:
                caption, = _0
                self.addNotification(self.Notification(caption))
        elif _1 == 2:
            if isinstance(_0[1], int):
                caption, type = _0
                self.addNotification(self.Notification(caption, type))
            else:
                caption, description = _0
                self.addNotification(self.Notification(caption, description))
        elif _1 == 3:
            caption, description, type = _0
            self.addNotification(self.Notification(caption, description, type))
        else:
            raise ARGERROR(1, 3)

    def addNotification(self, notification):
        if self._notifications is None:
            self._notifications = LinkedList()
        self._notifications.add(notification)
        self.requestRepaint()

    def setFocusedComponent(self, focusable):
        """This method is used by Component.Focusable objects to request focus to
        themselves. Focus renders must be handled at window level (instead of
        Component.Focusable) due we want the last focused component to be focused
        in client too. Not the one that is rendered last (the case we'd get if
        implemented in Focusable only).

        To focus component from Vaadin application, use Focusable.focus(). See
        {@link Focusable}.

        @param focusable
                   to be focused on next paint
        """
        if self.getParent() is not None:
            # focus is handled by main windows
            self.getParent().setFocusedComponent(focusable)
        else:
            self._pendingFocus = focusable
            self.requestRepaint()

    class Notification(Serializable):
        """A notification message, used to display temporary messages to the user -
        for example "Document saved", or "Save failed".
        <p>
        The notification message can consist of several parts: caption,
        description and icon. It is usually used with only caption - one should
        be wary of filling the notification with too much information.
        </p>
        <p>
        The notification message tries to be as unobtrusive as possible, while
        still drawing needed attention. There are several basic types of messages
        that can be used in different situations:
        <ul>
        <li>TYPE_HUMANIZED_MESSAGE fades away quickly as soon as the user uses
        the mouse or types something. It can be used to show fairly unimportant
        messages, such as feedback that an operation succeeded ("Document Saved")
        - the kind of messages the user ignores once the application is familiar.
        </li>
        <li>TYPE_WARNING_MESSAGE is shown for a short while after the user uses
        the mouse or types something. It's default style is also more noticeable
        than the humanized message. It can be used for messages that do not
        contain a lot of important information, but should be noticed by the
        user. Despite the name, it does not have to be a warning, but can be used
        instead of the humanized message whenever you want to make the message a
        little more noticeable.</li>
        <li>TYPE_ERROR_MESSAGE requires to user to click it before disappearing,
        and can be used for critical messages.</li>
        <li>TYPE_TRAY_NOTIFICATION is shown for a while in the lower left corner
        of the window, and can be used for "convenience notifications" that do
        not have to be noticed immediately, and should not interfere with the
        current task - for instance to show "You have a new message in your
        inbox" while the user is working in some other area of the application.</li>
        </ul>
        </p>
        <p>
        In addition to the basic pre-configured types, a Notification can also be
        configured to show up in a custom position, for a specified time (or
        until clicked), and with a custom stylename. An icon can also be added.
        </p>
        """
        TYPE_HUMANIZED_MESSAGE = 1
        TYPE_WARNING_MESSAGE = 2
        TYPE_ERROR_MESSAGE = 3
        TYPE_TRAY_NOTIFICATION = 4
        POSITION_CENTERED = 1
        POSITION_CENTERED_TOP = 2
        POSITION_CENTERED_BOTTOM = 3
        POSITION_TOP_LEFT = 4
        POSITION_TOP_RIGHT = 5
        POSITION_BOTTOM_LEFT = 6
        POSITION_BOTTOM_RIGHT = 7
        DELAY_FOREVER = -1
        DELAY_NONE = 0
        _caption = None
        _description = None
        _icon = None
        _position = POSITION_CENTERED
        _delayMsec = 0
        _styleName = None

        def __init__(self, *args):
            """Creates a "humanized" notification message.

            @param caption
                       The message to show
            ---
            Creates a notification message of the specified type.

            @param caption
                       The message to show
            @param type
                       The type of message
            ---
            Creates a "humanized" notification message with a bigger caption and
            smaller description.

            @param caption
                       The message caption
            @param description
                       The message description
            ---
            Creates a notification message of the specified type, with a bigger
            caption and smaller description.

            @param caption
                       The message caption
            @param description
                       The message description
            @param type
                       The type of message
            """
            _0 = args
            _1 = len(args)
            if _1 == 1:
                caption, = _0
                self.__init__(caption, None, self.TYPE_HUMANIZED_MESSAGE)
            elif _1 == 2:
                if isinstance(_0[1], int):
                    caption, type = _0
                    self.__init__(caption, None, type)
                else:
                    caption, description = _0
                    self.__init__(caption, description, self.TYPE_HUMANIZED_MESSAGE)
            elif _1 == 3:
                caption, description, type = _0
                self._caption = caption
                self._description = description
                self.setType(type)
            else:
                raise ARGERROR(1, 3)

        def setType(self, type):
            _0 = type
            _1 = False
            while True:
                if _0 == self.TYPE_WARNING_MESSAGE:
                    _1 = True
                    self._delayMsec = 1500
                    self._styleName = 'warning'
                    break
                if (_1 is True) or (_0 == self.TYPE_ERROR_MESSAGE):
                    _1 = True
                    self._delayMsec = -1
                    self._styleName = 'error'
                    break
                if (_1 is True) or (_0 == self.TYPE_TRAY_NOTIFICATION):
                    _1 = True
                    self._delayMsec = 3000
                    self._position = self.POSITION_BOTTOM_RIGHT
                    self._styleName = 'tray'
                if (_1 is True) or (_0 == self.TYPE_HUMANIZED_MESSAGE):
                    _1 = True
                if True:
                    _1 = True
                    break
                break

        def getCaption(self):
            """Gets the caption part of the notification message.

            @return The message caption
            """
            return self._caption

        def setCaption(self, caption):
            """Sets the caption part of the notification message

            @param caption
                       The message caption
            """
            self._caption = caption

        def getMessage(self):
            """@deprecated Use {@link #getDescription()} instead.
            @return
            """
            return self._description

        def setMessage(self, description):
            """@deprecated Use {@link #setDescription(String)} instead.
            @param description
            """
            self._description = description

        def getDescription(self):
            """Gets the description part of the notification message.

            @return The message description.
            """
            return self._description

        def setDescription(self, description):
            """Sets the description part of the notification message.

            @param description
            """
            self._description = description

        def getPosition(self):
            """Gets the position of the notification message.

            @return The position
            """
            return self._position

        def setPosition(self, position):
            """Sets the position of the notification message.

            @param position
                       The desired notification position
            """
            self._position = position

        def getIcon(self):
            """Gets the icon part of the notification message.

            @return The message icon
            """
            return self._icon

        def setIcon(self, icon):
            """Sets the icon part of the notification message.

            @param icon
                       The desired message icon
            """
            self._icon = icon

        def getDelayMsec(self):
            """Gets the delay before the notification disappears.

            @return the delay in msec, -1 indicates the message has to be
                    clicked.
            """
            return self._delayMsec

        def setDelayMsec(self, delayMsec):
            """Sets the delay before the notification disappears.

            @param delayMsec
                       the desired delay in msec, -1 to require the user to click
                       the message
            """
            self._delayMsec = delayMsec

        def setStyleName(self, styleName):
            """Sets the style name for the notification message.

            @param styleName
                       The desired style name.
            """
            self._styleName = styleName

        def getStyleName(self):
            """Gets the style name for the notification message.

            @return
            """
            return self._styleName

    def executeJavaScript(self, script):
        """Executes JavaScript in this window.

        <p>
        This method allows one to inject javascript from the server to client. A
        client implementation is not required to implement this functionality,
        but currently all web-based clients do implement this.
        </p>

        <p>
        Executing javascript this way often leads to cross-browser compatibility
        issues and regressions that are hard to resolve. Use of this method
        should be avoided and instead it is recommended to create new widgets
        with GWT. For more info on creating own, reusable client-side widgets in
        Java, read the corresponding chapter in Book of Vaadin.
        </p>

        @param script
                   JavaScript snippet that will be executed.
        """
        if self.getParent() is not None:
            raise self.UnsupportedOperationException('Only application level windows can execute javascript.')
        if self._jsExecQueue is None:
            self._jsExecQueue = list()
        self._jsExecQueue.add(script)
        self.requestRepaint()

    def isClosable(self):
        """Returns the closable status of the sub window. If a sub window is
        closable it typically shows an X in the upper right corner. Clicking on
        the X sends a close event to the server. Setting closable to false will
        remove the X from the sub window and prevent the user from closing the
        window.

        Note! For historical reasons readonly controls the closability of the sub
        window and therefore readonly and closable affect each other. Setting
        readonly to true will set closable to false and vice versa.
        <p/>
        Closable only applies to sub windows, not to browser level windows.

        @return true if the sub window can be closed by the user.
        """
        return not self.isReadOnly()

    def setClosable(self, closable):
        """Sets the closable status for the sub window. If a sub window is closable
        it typically shows an X in the upper right corner. Clicking on the X
        sends a close event to the server. Setting closable to false will remove
        the X from the sub window and prevent the user from closing the window.

        Note! For historical reasons readonly controls the closability of the sub
        window and therefore readonly and closable affect each other. Setting
        readonly to true will set closable to false and vice versa.
        <p/>
        Closable only applies to sub windows, not to browser level windows.

        @param closable
                   determines if the sub window can be closed by the user.
        """
        self.setReadOnly(not closable)

    def isDraggable(self):
        """Indicates whether a sub window can be dragged or not. By default a sub
        window is draggable.
        <p/>
        Draggable only applies to sub windows, not to browser level windows.

        @param draggable
                   true if the sub window can be dragged by the user
        """
        return self._draggable

    def setDraggable(self, draggable):
        """Enables or disables that a sub window can be dragged (moved) by the user.
        By default a sub window is draggable.
        <p/>
        Draggable only applies to sub windows, not to browser level windows.

        @param draggable
                   true if the sub window can be dragged by the user
        """
        # Actions
        self._draggable = draggable
        self.requestRepaint()

    closeShortcut = None

    def setCloseShortcut(self, keyCode, *modifiers):
        """Makes is possible to close the window by pressing the given
        {@link KeyCode} and (optional) {@link ModifierKey}s.<br/>
        Note that this shortcut only reacts while the window has focus, closing
        itself - if you want to close a subwindow from a parent window, use
        {@link #addAction(com.vaadin.event.Action)} of the parent window instead.

        @param keyCode
                   the keycode for invoking the shortcut
        @param modifiers
                   the (optional) modifiers for invoking the shortcut, null for
                   none
        """
        if self.closeShortcut is not None:
            self.removeAction(self.closeShortcut)
        self.closeShortcut = self.CloseShortcut(self, keyCode, modifiers)
        self.addAction(self.closeShortcut)

    def removeCloseShortcut(self):
        """Removes the keyboard shortcut previously set with
        {@link #setCloseShortcut(int, int...)}.
        """
        if self.closeShortcut is not None:
            self.removeAction(self.closeShortcut)
            self.closeShortcut = None

    class CloseShortcut(ShortcutListener):
        """A {@link ShortcutListener} specifically made to define a keyboard
        shortcut that closes the window.

        <pre>
        <code>
         // within the window using helper
         subWindow.setCloseShortcut(KeyCode.ESCAPE, null);

         // or globally
         getWindow().addAction(new Window.CloseShortcut(subWindow, KeyCode.ESCAPE));
        </code>
        </pre>
        """
        window = None

        def __init__(self, *args):
            """Creates a keyboard shortcut for closing the given window using the
            shorthand notation defined in {@link ShortcutAction}.

            @param window
                       to be closed when the shortcut is invoked
            @param shorthandCaption
                       the caption with shortcut keycode and modifiers indicated
            ---
            Creates a keyboard shortcut for closing the given window using the
            given {@link KeyCode} and {@link ModifierKey}s.

            @param window
                       to be closed when the shortcut is invoked
            @param keyCode
                       KeyCode to react to
            @param modifiers
                       optional modifiers for shortcut
            ---
            Creates a keyboard shortcut for closing the given window using the
            given {@link KeyCode}.

            @param window
                       to be closed when the shortcut is invoked
            @param keyCode
                       KeyCode to react to
            """
            _0 = args
            _1 = len(args)
            if _1 == 2:
                if isinstance(_0[1], int):
                    window, keyCode = _0
                    self.__init__(window, keyCode, None)
                else:
                    window, shorthandCaption = _0
                    super(CloseShortcut, self)(shorthandCaption)
                    self.window = window
            elif _1 == 3:
                window, keyCode, modifiers = _0
                super(CloseShortcut, self)(None, keyCode, modifiers)
                self.window = window
            else:
                raise ARGERROR(2, 3)

        def handleAction(self, sender, target):
            self.window.close()

    def focus(self):
        """{@inheritDoc}

        If the window is a sub-window focusing will cause the sub-window to be
        brought on top of other sub-windows on gain keyboard focus.
        """
        if self.getParent() is not None:
            # When focusing a sub-window it basically means it should be
            # brought to the front. Instead of just moving the keyboard focus
            # we focus the window and bring it top-most.

            self._bringToFront()
        else:
            super(Window, self).focus()