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
from com.vaadin.ui.AbstractOrderedLayout import (AbstractOrderedLayout,)


class OrderedLayout(AbstractOrderedLayout):
    """Ordered layout.

    <code>OrderedLayout</code> is a component container, which shows the
    subcomponents in the order of their addition in specified orientation.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    @deprecated Replaced by VerticalLayout/HorizontalLayout. For type checking
                please not that VerticalLayout/HorizontalLayout do not extend
                OrderedLayout but AbstractOrderedLayout (which also OrderedLayout
                extends).
    """
    # Predefined orientations
    # Components are to be laid out vertically.
    ORIENTATION_VERTICAL = 0
    # Components are to be laid out horizontally.
    ORIENTATION_HORIZONTAL = 1
    # Orientation of the layout.
    _orientation = None

    def __init__(self, *args):
        """Creates a new ordered layout. The order of the layout is
        <code>ORIENTATION_VERTICAL</code>.

        @deprecated Use VerticalLayout instead.
        ---
        Create a new ordered layout. The orientation of the layout is given as
        parameters.

        @param orientation
                   the Orientation of the layout.

        @deprecated Use VerticalLayout/HorizontalLayout instead.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.__init__(self.ORIENTATION_VERTICAL)
        elif _1 == 1:
            orientation, = _0
            self._orientation = orientation
            if orientation == self.ORIENTATION_VERTICAL:
                self.setWidth(100, self.UNITS_PERCENTAGE)
        else:
            raise ARGERROR(0, 1)

    def getOrientation(self):
        """Gets the orientation of the container.

        @return the Value of property orientation.
        """
        return self._orientation

    def setOrientation(self, *args):
        """Sets the orientation of this OrderedLayout. This method should only be
        used before initial paint.

        @param orientation
                   the New value of property orientation.
        @deprecated Use VerticalLayout/HorizontalLayout or define orientation in
                    constructor instead
        ---
        Internal method to change orientation of layout. This method should only
        be used before initial paint.

        @param orientation
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            orientation, = _0
            self.setOrientation(orientation, True)
        elif _1 == 2:
            orientation, needsRepaint = _0
            if (
                (orientation < self.ORIENTATION_VERTICAL) or (orientation > self.ORIENTATION_HORIZONTAL)
            ):
                raise self.IllegalArgumentException()
            self._orientation = orientation
            if needsRepaint:
                self.requestRepaint()
        else:
            raise ARGERROR(1, 2)

    # Checks the validity of the argument

    def paintContent(self, target):
        super(OrderedLayout, self).paintContent(target)
        # Adds the orientation attributes (the default is vertical)
        if self._orientation == self.ORIENTATION_HORIZONTAL:
            target.addAttribute('orientation', 'horizontal')