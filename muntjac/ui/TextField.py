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
from com.vaadin.ui.AbstractTextField import (AbstractTextField,)


class TextField(AbstractTextField):
    """<p>
    A text editor component that can be bound to any bindable Property. The text
    editor supports both multiline and single line modes, default is one-line
    mode.
    </p>

    <p>
    Since <code>TextField</code> extends <code>AbstractField</code> it implements
    the {@link com.vaadin.data.Buffered} interface. A <code>TextField</code> is
    in write-through mode by default, so
    {@link com.vaadin.ui.AbstractField#setWriteThrough(boolean)} must be called
    to enable buffering.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Tells if input is used to enter sensitive information that is not echoed
    # to display. Typically passwords.

    _secret = False
    # Number of visible rows in a multiline TextField. Value 0 implies a
    # single-line text-editor.

    _rows = 0
    # Tells if word-wrapping should be used in multiline mode.
    _wordwrap = True

    def __init__(self, *args):
        """Constructs an empty <code>TextField</code> with no caption.
        ---
        Constructs an empty <code>TextField</code> with given caption.

        @param caption
                   the caption <code>String</code> for the editor.
        ---
        Constructs a new <code>TextField</code> that's bound to the specified
        <code>Property</code> and has no caption.

        @param dataSource
                   the Property to be edited with this editor.
        ---
        Constructs a new <code>TextField</code> that's bound to the specified
        <code>Property</code> and has the given caption <code>String</code>.

        @param caption
                   the caption <code>String</code> for the editor.
        @param dataSource
                   the Property to be edited with this editor.
        ---
        Constructs a new <code>TextField</code> with the given caption and
        initial text contents. The editor constructed this way will not be bound
        to a Property unless
        {@link com.vaadin.data.Property.Viewer#setPropertyDataSource(Property)}
        is called to bind it.

        @param caption
                   the caption <code>String</code> for the editor.
        @param text
                   the initial text content of the editor.
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.setValue('')
        elif _1 == 1:
            if isinstance(_0[0], Property):
                dataSource, = _0
                self.setPropertyDataSource(dataSource)
            else:
                caption, = _0
                self.__init__()
                self.setCaption(caption)
        elif _1 == 2:
            if isinstance(_0[1], Property):
                caption, dataSource = _0
                self.__init__(dataSource)
                self.setCaption(caption)
            else:
                caption, value = _0
                self.setValue(value)
                self.setCaption(caption)
        else:
            raise ARGERROR(0, 2)

    def isSecret(self):
        """Gets the secret property. If a field is used to enter secret information
        the information is not echoed to display.

        @return <code>true</code> if the field is used to enter secret
                information, <code>false</code> otherwise.

        @deprecated Starting from 6.5 use {@link PasswordField} instead for
                    secret text input.
        """
        return self._secret

    def setSecret(self, secret):
        """Sets the secret property on and off. If a field is used to enter secret
        information the information is not echoed to display.

        @param secret
                   the value specifying if the field is used to enter secret
                   information.
        @deprecated Starting from 6.5 use {@link PasswordField} instead for
                    secret text input.
        """
        if self._secret != secret:
            self._secret = secret
            self.requestRepaint()

    def paintContent(self, target):
        if self.isSecret():
            target.addAttribute('secret', True)
        rows = self.getRows()
        if rows != 0:
            target.addAttribute('rows', rows)
            target.addAttribute('multiline', True)
            if not self.isWordwrap():
                # Wordwrap is only painted if turned off to minimize
                # communications
                target.addAttribute('wordwrap', False)
        super(TextField, self).paintContent(target)

    def getRows(self):
        """Gets the number of rows in the editor. If the number of rows is set to 0,
        the actual number of displayed rows is determined implicitly by the
        adapter.

        @return number of explicitly set rows.
        @deprecated Starting from 6.5 use {@link TextArea} for a multi-line text
                    input.
        """
        return self._rows

    def setRows(self, rows):
        """Sets the number of rows in the editor.

        @param rows
                   the number of rows for this editor.

        @deprecated Starting from 6.5 use {@link TextArea} for a multi-line text
                    input.
        """
        if rows < 0:
            rows = 0
        if self._rows != rows:
            self._rows = rows
            self.requestRepaint()

    def isWordwrap(self):
        """Tests if the editor is in word-wrap mode.

        @return <code>true</code> if the component is in the word-wrap mode,
                <code>false</code> if not.
        @deprecated Starting from 6.5 use {@link TextArea} for a multi-line text
                    input.
        """
        return self._wordwrap

    def setWordwrap(self, wordwrap):
        """Sets the editor's word-wrap mode on or off.

        @param wordwrap
                   the boolean value specifying if the editor should be in
                   word-wrap mode after the call or not.

        @deprecated Starting from 6.5 use {@link TextArea} for a multi-line text
                    input.
        """
        if self._wordwrap != wordwrap:
            self._wordwrap = wordwrap
            self.requestRepaint()

    def setHeight(self, *args):
        """Sets the height of the {@link TextField} instance.

        <p>
        Setting height for {@link TextField} also has a side-effect that puts
        {@link TextField} into multiline mode (aka "textarea"). Multiline mode
        can also be achieved by calling {@link #setRows(int)}. The height value
        overrides the number of rows set by {@link #setRows(int)}.
        <p>
        If you want to set height of single line {@link TextField}, call
        {@link #setRows(int)} with value 0 after setting the height. Setting rows
        to 0 resets the side-effect.
        <p>
        Starting from 6.5 you should use {@link TextArea} instead of
        {@link TextField} for multiline text input.


        @see com.vaadin.ui.AbstractComponent#setHeight(float, int)
        ---
        Sets the height of the {@link TextField} instance.

        <p>
        Setting height for {@link TextField} also has a side-effect that puts
        {@link TextField} into multiline mode (aka "textarea"). Multiline mode
        can also be achieved by calling {@link #setRows(int)}. The height value
        overrides the number of rows set by {@link #setRows(int)}.
        <p>
        If you want to set height of single line {@link TextField}, call
        {@link #setRows(int)} with value 0 after setting the height. Setting rows
        to 0 resets the side-effect.

        @see com.vaadin.ui.AbstractComponent#setHeight(java.lang.String)
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            height, = _0
            super(TextField, self).setHeight(height)
        elif _1 == 2:
            height, unit = _0
            super(TextField, self).setHeight(height, unit)
            if height > 1 and self.getClass() == TextField:
                # In html based terminals we most commonly want to make component
                # to be textarea if height is defined. Setting row field above 0
                # will render component as textarea.

                self.setRows(2)
        else:
            raise ARGERROR(1, 2)

    # will call setHeight(float, int) the actually does the magic. Method
    # is overridden just to document side-effects.