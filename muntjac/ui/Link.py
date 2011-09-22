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
from com.vaadin.ui.AbstractComponent import (AbstractComponent,)
from com.vaadin.ui.Window import (Window,)


class Link(AbstractComponent):
    """Link is used to create external or internal URL links.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Target window border type constant: No window border
    TARGET_BORDER_NONE = Window.BORDER_NONE
    # Target window border type constant: Minimal window border
    TARGET_BORDER_MINIMAL = Window.BORDER_MINIMAL
    # Target window border type constant: Default window border
    TARGET_BORDER_DEFAULT = Window.BORDER_DEFAULT
    _resource = None
    _targetName = None
    _targetBorder = TARGET_BORDER_DEFAULT
    _targetWidth = -1
    _targetHeight = -1

    def __init__(self, *args):
        """Creates a new link.
        ---
        Creates a new instance of Link.

        @param caption
        @param resource
        ---
        Creates a new instance of Link that opens a new window.


        @param caption
                   the Link text.
        @param targetName
                   the name of the target window where the link opens to. Empty
                   name of null implies that the target is opened to the window
                   containing the link.
        @param width
                   the Width of the target window.
        @param height
                   the Height of the target window.
        @param border
                   the Border style of the target window.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            pass # astStmt: [Stmt([]), None]
        elif _1 == 2:
            caption, resource = _0
            self.setCaption(caption)
            self._resource = resource
        elif _1 == 6:
            caption, resource, targetName, width, height, border = _0
            self.setCaption(caption)
            self._resource = resource
            self.setTargetName(targetName)
            self.setTargetWidth(width)
            self.setTargetHeight(height)
            self.setTargetBorder(border)
        else:
            raise ARGERROR(0, 6)

    def paintContent(self, target):
        """Paints the content of this component.

        @param target
                   the Paint Event.
        @throws PaintException
                    if the paint operation failed.
        """
        if self._resource is not None:
            target.addAttribute('src', self._resource)
        else:
            return
        # Target window name
        name = self.getTargetName()
        if name is not None and len(name) > 0:
            target.addAttribute('name', name)
        # Target window size
        if self.getTargetWidth() >= 0:
            target.addAttribute('targetWidth', self.getTargetWidth())
        if self.getTargetHeight() >= 0:
            target.addAttribute('targetHeight', self.getTargetHeight())
        # Target window border
        _0 = self.getTargetBorder()
        _1 = False
        while True:
            if _0 == self.TARGET_BORDER_MINIMAL:
                _1 = True
                target.addAttribute('border', 'minimal')
                break
            if (_1 is True) or (_0 == self.TARGET_BORDER_NONE):
                _1 = True
                target.addAttribute('border', 'none')
                break
            break

    def getTargetBorder(self):
        """Returns the target window border.

        @return the target window border.
        """
        return self._targetBorder

    def getTargetHeight(self):
        """Returns the target window height or -1 if not set.

        @return the target window height.
        """
        return -1 if self._targetHeight < 0 else self._targetHeight

    def getTargetName(self):
        """Returns the target window name. Empty name of null implies that the
        target is opened to the window containing the link.

        @return the target window name.
        """
        return self._targetName

    def getTargetWidth(self):
        """Returns the target window width or -1 if not set.

        @return the target window width.
        """
        return -1 if self._targetWidth < 0 else self._targetWidth

    def setTargetBorder(self, targetBorder):
        """Sets the border of the target window.

        @param targetBorder
                   the targetBorder to set.
        """
        if (
            ((targetBorder == self.TARGET_BORDER_DEFAULT) or (targetBorder == self.TARGET_BORDER_MINIMAL)) or (targetBorder == self.TARGET_BORDER_NONE)
        ):
            self._targetBorder = targetBorder
            self.requestRepaint()

    def setTargetHeight(self, targetHeight):
        """Sets the target window height.

        @param targetHeight
                   the targetHeight to set.
        """
        self._targetHeight = targetHeight
        self.requestRepaint()

    def setTargetName(self, targetName):
        """Sets the target window name.

        @param targetName
                   the targetName to set.
        """
        self._targetName = targetName
        self.requestRepaint()

    def setTargetWidth(self, targetWidth):
        """Sets the target window width.

        @param targetWidth
                   the targetWidth to set.
        """
        self._targetWidth = targetWidth
        self.requestRepaint()

    def getResource(self):
        """Returns the resource this link opens.

        @return the Resource.
        """
        return self._resource

    def setResource(self, resource):
        """Sets the resource this link opens.

        @param resource
                   the resource to set.
        """
        self._resource = resource
        self.requestRepaint()