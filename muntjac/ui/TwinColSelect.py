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
from com.vaadin.ui.AbstractSelect import (AbstractSelect,)
from com.vaadin.terminal.gwt.client.ui.VTwinColSelect import (VTwinColSelect,)
# from java.util.Collection import (Collection,)


class TwinColSelect(AbstractSelect):
    """Multiselect component with two lists: left side for available items and right
    side for selected items.
    """
    _columns = 0
    _rows = 0
    _leftColumnCaption = None
    _rightColumnCaption = None

    def __init__(self, *args):
        """None
        ---
        @param caption
        ---
        @param caption
        @param dataSource
        ---
        @param caption
        @param options
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            super(TwinColSelect, self)()
            self.setMultiSelect(True)
        elif _1 == 1:
            caption, = _0
            super(TwinColSelect, self)(caption)
            self.setMultiSelect(True)
        elif _1 == 2:
            if isinstance(_0[1], Collection):
                caption, options = _0
                super(TwinColSelect, self)(caption, options)
                self.setMultiSelect(True)
            else:
                caption, dataSource = _0
                super(TwinColSelect, self)(caption, dataSource)
                self.setMultiSelect(True)
        else:
            raise ARGERROR(0, 2)

    def setColumns(self, columns):
        """Sets the number of columns in the editor. If the number of columns is set
        0, the actual number of displayed columns is determined implicitly by the
        adapter.
        <p>
        The number of columns overrides the value set by setWidth. Only if
        columns are set to 0 (default) the width set using
        {@link #setWidth(float, int)} or {@link #setWidth(String)} is used.

        @param columns
                   the number of columns to set.
        """
        if columns < 0:
            columns = 0
        if self._columns != columns:
            self._columns = columns
            self.requestRepaint()

    def getColumns(self):
        return self._columns

    def getRows(self):
        return self._rows

    def setRows(self, rows):
        """Sets the number of rows in the editor. If the number of rows is set to 0,
        the actual number of displayed rows is determined implicitly by the
        adapter.
        <p>
        If a height if set (using {@link #setHeight(String)} or
        {@link #setHeight(float, int)}) it overrides the number of rows. Leave
        the height undefined to use this method. This is the opposite of how
        {@link #setColumns(int)} work.


        @param rows
                   the number of rows to set.
        """
        if rows < 0:
            rows = 0
        if self._rows != rows:
            self._rows = rows
            self.requestRepaint()

    def paintContent(self, target):
        target.addAttribute('type', 'twincol')
        # Adds the number of columns
        if self._columns != 0:
            target.addAttribute('cols', self._columns)
        # Adds the number of rows
        if self._rows != 0:
            target.addAttribute('rows', self._rows)
        # Right and left column captions and/or icons (if set)
        lc = self.getLeftColumnCaption()
        rc = self.getRightColumnCaption()
        if lc is not None:
            target.addAttribute(VTwinColSelect.ATTRIBUTE_LEFT_CAPTION, lc)
        if rc is not None:
            target.addAttribute(VTwinColSelect.ATTRIBUTE_RIGHT_CAPTION, rc)
        super(TwinColSelect, self).paintContent(target)

    def setRightColumnCaption(self, rightColumnCaption):
        """Sets the text shown above the right column.

        @param caption
                   The text to show
        """
        self._rightColumnCaption = rightColumnCaption
        self.requestRepaint()

    def getRightColumnCaption(self):
        """Returns the text shown above the right column.

        @return The text shown or null if not set.
        """
        return self._rightColumnCaption

    def setLeftColumnCaption(self, leftColumnCaption):
        """Sets the text shown above the left column.

        @param caption
                   The text to show
        """
        self._leftColumnCaption = leftColumnCaption
        self.requestRepaint()

    def getLeftColumnCaption(self):
        """Returns the text shown above the left column.

        @return The text shown or null if not set.
        """
        return self._leftColumnCaption