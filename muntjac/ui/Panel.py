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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.Scrollable import (Scrollable,)
from com.vaadin.event.ActionManager import (ActionManager,)
from com.vaadin.event.Action import (Action, Notifier,)
from com.vaadin.terminal.gwt.client.ui.VPanel import (VPanel,)
from com.vaadin.ui.AbstractComponentContainer import (AbstractComponentContainer,)
from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
from com.vaadin.ui.ComponentContainer import (ComponentContainer,)
from com.vaadin.ui.VerticalLayout import (VerticalLayout,)
# from java.util.Iterator import (Iterator,)
# from java.util.Map import (Map,)


class Panel(AbstractComponentContainer, Scrollable, ComponentContainer, ComponentAttachListener, ComponentContainer, ComponentDetachListener, Action, Notifier, Focusable):
    """Panel - a simple single component container.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    _CLICK_EVENT = VPanel.CLICK_EVENT_IDENTIFIER
    # Removes extra decorations from the Panel.
    # 
    # @deprecated this style is no longer part of the core framework and this
    #             component, even though most built-in themes implement this
    #             style. Use the constant specified in the theme class file
    #             that you're using, if it provides one, e.g.
    #             {@link Reindeer#PANEL_LIGHT} or {@link Runo#PANEL_LIGHT} .

    STYLE_LIGHT = 'light'
    # Content of the panel.
    _content = None
    # Scroll X position.
    _scrollOffsetX = 0
    # Scroll Y position.
    _scrollOffsetY = 0
    # Scrolling mode.
    _scrollable = False
    # Keeps track of the Actions added to this component, and manages the
    # painting and handling as well.

    actionManager = None
    # By default the Panel is not in the normal document focus flow and can
    # only be focused by using the focus()-method. Change this to 0 if you want
    # to have the Panel in the normal focus flow.

    _tabIndex = -1

    def __init__(self, *args):
        """Creates a new empty panel. A VerticalLayout is used as content.
        ---
        Creates a new empty panel which contains the given content. The content
        cannot be null.

        @param content
                   the content for the panel.
        ---
        Creates a new empty panel with caption. Default layout is used.

        @param caption
                   the caption used in the panel.
        ---
        Creates a new empty panel with the given caption and content.

        @param caption
                   the caption of the panel.
        @param content
                   the content used in the panel.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__(None)
        elif _1 == 1:
            if isinstance(_0[0], ComponentContainer):
                content, = _0
                self.setContent(content)
                self.setWidth(100, self.UNITS_PERCENTAGE)
            else:
                caption, = _0
                self.__init__(caption, None)
        elif _1 == 2:
            caption, content = _0
            self.__init__(content)
            self.setCaption(caption)
        else:
            raise ARGERROR(0, 2)

    def getLayout(self):
        """Gets the current layout of the panel.

        @return the Current layout of the panel.
        @deprecated A Panel can now contain a ComponentContainer which is not
                    necessarily a Layout. Use {@link #getContent()} instead.
        """
        if isinstance(self._content, Layout):
            return self._content
        elif self._content is None:
            return None
        raise self.IllegalStateException('Panel does not contain a Layout. Use getContent() instead of getLayout().')

    def setLayout(self, newLayout):
        """Sets the layout of the panel.

        If given layout is null, a VerticalLayout with margins set is used as a
        default.

        Components from old layout are not moved to new layout by default
        (changed in 5.2.2). Use function in Layout interface manually.

        @param newLayout
                   the New layout of the panel.
        @deprecated A Panel can now contain a ComponentContainer which is not
                    necessarily a Layout. Use
                    {@link #setContent(ComponentContainer)} instead.
        """
        self.setContent(newLayout)

    def getContent(self):
        """Returns the content of the Panel.

        @return
        """
        return self._content

    def setContent(self, newContent):
        """Set the content of the Panel. If null is given as the new content then a
        layout is automatically created and set as the content.

        @param content
                   The new content
        """
        # If the content is null we create the default content
        if newContent is None:
            newContent = self.createDefaultContent()
        # if (newContent == null) {
        # throw new IllegalArgumentException("Content cannot be null");
        # }
        if newContent == self._content:
            # don't set the same content twice
            return
        # detach old content if present
        if self._content is not None:
            self._content.setParent(None)
            self._content.removeListener(self)
            self._content.removeListener(self)
        # Sets the panel to be parent for the content
        newContent.setParent(self)
        # Sets the new content
        self._content = newContent
        # Adds the event listeners for new content
        newContent.addListener(self)
        newContent.addListener(self)
        self._content = newContent

    def createDefaultContent(self):
        """Create a ComponentContainer which is added by default to the Panel if
        user does not specify any content.

        @return
        """
        # (non-Javadoc)
        # 
        # @see
        # com.vaadin.ui.AbstractComponent#paintContent(com.vaadin.terminal.PaintTarget
        # )

        layout = VerticalLayout()
        # Force margins by default
        layout.setMargin(True)
        return layout

    def paintContent(self, target):
        self._content.paint(target)
        target.addVariable(self, 'tabindex', self.getTabIndex())
        if self.isScrollable():
            target.addVariable(self, 'scrollLeft', self.getScrollLeft())
            target.addVariable(self, 'scrollTop', self.getScrollTop())
        if self.actionManager is not None:
            self.actionManager.paintActions(None, target)

    def requestRepaintAll(self):
        # Panel has odd structure, delegate to layout
        self.requestRepaint()
        if self.getContent() is not None:
            self.getContent().requestRepaintAll()

    def addComponent(self, c):
        """Adds the component into this container.

        @param c
                   the component to be added.
        @see com.vaadin.ui.AbstractComponentContainer#addComponent(com.vaadin.ui.Component)
        """
        self._content.addComponent(c)
        # No repaint request is made as we except the underlying container to
        # request repaints

    def removeComponent(self, c):
        """Removes the component from this container.

        @param c
                   The component to be removed.
        @see com.vaadin.ui.AbstractComponentContainer#removeComponent(com.vaadin.ui.Component)
        """
        self._content.removeComponent(c)
        # No repaint request is made as we except the underlying container to
        # request repaints

    def getComponentIterator(self):
        """Gets the component container iterator for going through all the
        components in the container.

        @return the Iterator of the components inside the container.
        @see com.vaadin.ui.ComponentContainer#getComponentIterator()
        """
        return self._content.getComponentIterator()

    def changeVariables(self, source, variables):
        """Called when one or more variables handled by the implementing class are
        changed.

        @see com.vaadin.terminal.VariableOwner#changeVariables(Object, Map)
        """
        # Scrolling functionality
        # (non-Javadoc)
        # 
        # @see com.vaadin.terminal.Scrollable#setScrollable(boolean)

        super(Panel, self).changeVariables(source, variables)
        if self._CLICK_EVENT in variables:
            self.fireClick(variables[self._CLICK_EVENT])
        # Get new size
        newWidth = variables['width']
        newHeight = variables['height']
        if newWidth is not None and newWidth.intValue() != self.getWidth():
            self.setWidth(newWidth.intValue(), self.UNITS_PIXELS)
        if newHeight is not None and newHeight.intValue() != self.getHeight():
            self.setHeight(newHeight.intValue(), self.UNITS_PIXELS)
        # Scrolling
        newScrollX = variables['scrollLeft']
        newScrollY = variables['scrollTop']
        if newScrollX is not None and newScrollX.intValue() != self.getScrollLeft():
            # set internally, not to fire request repaint
            self._scrollOffsetX = newScrollX.intValue()
        if newScrollY is not None and newScrollY.intValue() != self.getScrollTop():
            # set internally, not to fire request repaint
            self._scrollOffsetY = newScrollY.intValue()
        # Actions
        if self.actionManager is not None:
            self.actionManager.handleActions(variables, self)

    def getScrollLeft(self):
        return self._scrollOffsetX

    def getScrollOffsetX(self):
        """@deprecated use {@link #getScrollLeft()} instead"""
        # (non-Javadoc)
        # 
        # @see com.vaadin.terminal.Scrollable#setScrollable(boolean)

        return self.getScrollLeft()

    def getScrollTop(self):
        return self._scrollOffsetY

    def getScrollOffsetY(self):
        """@deprecated use {@link #getScrollTop()} instead"""
        # (non-Javadoc)
        # 
        # @see com.vaadin.terminal.Scrollable#setScrollable(boolean)

        return self.getScrollTop()

    def isScrollable(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.terminal.Scrollable#setScrollable(boolean)

        return self._scrollable

    def setScrollable(self, isScrollingEnabled):
        # (non-Javadoc)
        # 
        # @see com.vaadin.terminal.Scrollable#setScrollLeft(int)

        if self._scrollable != isScrollingEnabled:
            self._scrollable = isScrollingEnabled
            self.requestRepaint()

    def setScrollLeft(self, pixelsScrolled):
        if pixelsScrolled < 0:
            raise self.IllegalArgumentException('Scroll offset must be at least 0')
        if self._scrollOffsetX != pixelsScrolled:
            self._scrollOffsetX = pixelsScrolled
            self.requestRepaint()

    def setScrollOffsetX(self, pixels):
        """@deprecated use setScrollLeft() method instead"""
        # Documented in interface
        self.setScrollLeft(pixels)

    def setScrollTop(self, pixelsScrolledDown):
        if pixelsScrolledDown < 0:
            raise self.IllegalArgumentException('Scroll offset must be at least 0')
        if self._scrollOffsetY != pixelsScrolledDown:
            self._scrollOffsetY = pixelsScrolledDown
            self.requestRepaint()

    def setScrollOffsetY(self, pixels):
        """@deprecated use setScrollTop() method instead"""
        # Documented in superclass
        self.setScrollTop(pixels)

    def replaceComponent(self, oldComponent, newComponent):
        self._content.replaceComponent(oldComponent, newComponent)

    def componentAttachedToContainer(self, event):
        """A new component is attached to container.

        @see com.vaadin.ui.ComponentContainer.ComponentAttachListener#componentAttachedToContainer(com.vaadin.ui.ComponentContainer.ComponentAttachEvent)
        """
        if event.getContainer() == self._content:
            self.fireComponentAttachEvent(event.getAttachedComponent())

    def componentDetachedFromContainer(self, event):
        """A component has been detached from container.

        @see com.vaadin.ui.ComponentContainer.ComponentDetachListener#componentDetachedFromContainer(com.vaadin.ui.ComponentContainer.ComponentDetachEvent)
        """
        if event.getContainer() == self._content:
            self.fireComponentDetachEvent(event.getDetachedComponent())

    def attach(self):
        """Notifies the component that it is connected to an application.

        @see com.vaadin.ui.Component#attach()
        """
        # can't call parent here as this is Panels hierarchy is a hack
        self.requestRepaint()
        if self._content is not None:
            self._content.attach()

    def detach(self):
        """Notifies the component that it is detached from the application.

        @see com.vaadin.ui.Component#detach()
        """
        # can't call parent here as this is Panels hierarchy is a hack
        if self._content is not None:
            self._content.detach()

    def removeAllComponents(self):
        """Removes all components from this container.

        @see com.vaadin.ui.ComponentContainer#removeAllComponents()
        """
        # ACTIONS
        self._content.removeAllComponents()

    def getActionManager(self):
        if self.actionManager is None:
            self.actionManager = ActionManager(self)
        return self.actionManager

    def addAction(self, action):
        self.getActionManager().addAction(action)

    def removeAction(self, action):
        if self.actionManager is not None:
            self.actionManager.removeAction(action)

    def addActionHandler(self, actionHandler):
        self.getActionManager().addActionHandler(actionHandler)

    def removeActionHandler(self, actionHandler):
        if self.actionManager is not None:
            self.actionManager.removeActionHandler(actionHandler)

    def removeAllActionHandlers(self):
        """Removes all action handlers"""
        if self.actionManager is not None:
            self.actionManager.removeAllActionHandlers()

    def addListener(self, listener):
        """Add a click listener to the Panel. The listener is called whenever the
        user clicks inside the Panel. Also when the click targets a component
        inside the Panel, provided the targeted component does not prevent the
        click event from propagating.

        Use {@link #removeListener(ClickListener)} to remove the listener.

        @param listener
                   The listener to add
        """
        self.addListener(self._CLICK_EVENT, self.ClickEvent, listener, self.ClickListener.clickMethod)

    def removeListener(self, listener):
        """Remove a click listener from the Panel. The listener should earlier have
        been added using {@link #addListener(ClickListener)}.

        @param listener
                   The listener to remove
        """
        self.removeListener(self._CLICK_EVENT, self.ClickEvent, listener)

    def fireClick(self, parameters):
        """Fire a click event to all click listeners.

        @param object
                   The raw "value" of the variable change from the client side.
        """
        mouseDetails = MouseEventDetails.deSerialize(parameters['mouseDetails'])
        self.fireEvent(self.ClickEvent(self, mouseDetails))

    def getTabIndex(self):
        """{@inheritDoc}"""
        return self._tabIndex

    def setTabIndex(self, tabIndex):
        """{@inheritDoc}"""
        self._tabIndex = tabIndex
        self.requestRepaint()

    def focus(self):
        """Moves keyboard focus to the component. {@see Focusable#focus()}"""
        super(Panel, self).focus()