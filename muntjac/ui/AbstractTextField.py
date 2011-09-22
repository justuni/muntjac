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

from muntjac.ui.AbstractField import AbstractField
from muntjac.terminal.gwt.client.ui.VTextField import VTextField

from muntjac.event.FieldEvents import BlurEvent
from muntjac.event.FieldEvents import BlurListener
from muntjac.event.FieldEvents import BlurNotifier
from muntjac.event.FieldEvents import FocusEvent
from muntjac.event.FieldEvents import FocusListener
from muntjac.event.FieldEvents import FocusNotifier
from muntjac.event.FieldEvents import TextChangeEvent
from muntjac.event.FieldEvents import TextChangeListener
from muntjac.event.FieldEvents import TextChangeNotifier


class TextChangeEventMode(object):
    """Different modes how the TextField can trigger {@link TextChangeEvent}s."""

    # An event is triggered on each text content change, most commonly key
    # press events.
    EAGER = 'EAGER'

    # Each text change event in the UI causes the event to be communicated
    # to the application after a timeout. The length of the timeout can be
    # controlled with {@link TextField#setInputEventTimeout(int)}. Only the
    # last input event is reported to the server side if several text
    # change events happen during the timeout.
    # <p>
    # In case of a {@link ValueChangeEvent} the schedule is not kept
    # strictly. Before a {@link ValueChangeEvent} a {@link TextChangeEvent}
    # is triggered if the text content has changed since the previous
    # TextChangeEvent regardless of the schedule.
    TIMEOUT = 'TIMEOUT'

    # An event is triggered when there is a pause of text modifications.
    # The length of the pause can be modified with
    # {@link TextField#setInputEventTimeout(int)}. Like with the
    # {@link #TIMEOUT} mode, an event is forced before
    # {@link ValueChangeEvent}s, even if the user did not keep a pause
    # while entering the text.
    # <p>
    # This is the default mode.
    LAZY = 'LAZY'

    _values = [EAGER, TIMEOUT, LAZY]

    @classmethod
    def values(cls):
        return cls._values[:]


class AbstractTextField(AbstractField, BlurNotifier, FocusNotifier, TextChangeNotifier):

    def __init__(self):
        super(AbstractTextField, self).__init__()

        # Value formatter used to format the string contents.
        self._format = None

        # Null representation.
        self._nullRepresentation = 'null'

        # Is setting to null from non-null value allowed by setting with null
        # representation .
        self._nullSettingAllowed = False

        # Maximum character count in text field.
        self._maxLength = -1

        # Number of visible columns in the TextField.
        self._columns = 0

        # The prompt to display in an empty field. Null when disabled.
        self._inputPrompt = None

        # The text content when the last messages to the server was sent.
        self._lastKnownTextContent = None

        # The position of the cursor when the last message to the server was sent.
        self._lastKnownCursorPosition = None

        # Flag indicating that a text change event is pending to be triggered.
        # Cleared by {@link #setInternalValue(Object)} and when the event is fired.
        self._textChangeEventPending = None

        self._textChangeEventMode = TextChangeEventMode.LAZY

        self._DEFAULT_TEXTCHANGE_TIMEOUT = 400

        self._textChangeEventTimeout = self._DEFAULT_TEXTCHANGE_TIMEOUT

        # Temporarily holds the new selection position. Cleared on paint.
        self._selectionPosition = -1

        # Temporarily holds the new selection length.
        self._selectionLength = None

        # Flag used to determine whether we are currently handling a state change
        # triggered by a user. Used to properly fire text change event before value
        # change event triggered by the client side.
        self._changingVariables = None


    def paintContent(self, target):
        super(AbstractTextField, self).paintContent(target)

        if self.getMaxLength() >= 0:
            target.addAttribute('maxLength', self.getMaxLength())

        # Adds the number of column and rows
        columns = self.getColumns()
        if columns != 0:
            target.addAttribute('cols', str(columns))

        if self.getInputPrompt() is not None:
            target.addAttribute('prompt', self.getInputPrompt())

        # Adds the content as variable
        value = self.getFormattedValue()
        if value is None:
            value = self.getNullRepresentation()
        if value is None:
            raise ValueError, 'Null values are not allowed if the null-representation is null'

        target.addVariable(self, 'text', value)

        if self._selectionPosition != -1:
            target.addAttribute('selpos', self._selectionPosition)
            target.addAttribute('sellen', self._selectionLength)
            self._selectionPosition = -1

        if self.hasListeners(TextChangeEvent):
            target.addAttribute(VTextField.ATTR_TEXTCHANGE_EVENTMODE, str(self.getTextChangeEventMode()))
            target.addAttribute(VTextField.ATTR_TEXTCHANGE_TIMEOUT, self.getTextChangeTimeout())


    def getFormattedValue(self):
        """Gets the formatted string value. Sets the field value by using the
        assigned Format.

        @return the Formatted value.
        @see #setFormat(Format)
        @see Format
        @deprecated
        """
        raise DeprecationWarning

        v = self.getValue()
        if v is None:
            return None
        return str(v)


    def getValue(self):
        v = super(AbstractTextField, self).getValue()
        if (self._format is None) or (v is None):
            return v
        try:
            raise DeprecationWarning
            return self._format.format(v)
        except ValueError:
            return v


    def changeVariables(self, source, variables):
        self._changingVariables = True

        try:
            super(AbstractTextField, self).changeVariables(source, variables)

            if VTextField.VAR_CURSOR in variables:
                obj = variables.get( VTextField.VAR_CURSOR )
                self._lastKnownCursorPosition = int(obj)

            if VTextField.VAR_CUR_TEXT in variables:
                # NOTE, we might want to develop this further so that on a
                # value change event the whole text content don't need to be
                # sent from the client to server. Just "commit" the value from
                # currentText to the value.
                self.handleInputEventTextChange(variables)

            # Sets the text
            if 'text' in variables and not self.isReadOnly():

                # Only do the setting if the string representation of the value
                # has been updated
                newValue = variables.get('text')

                # server side check for max length
                if self.getMaxLength() != -1 and len(newValue) > self.getMaxLength():
                    newValue = newValue[:self.getMaxLength()]

                oldValue = self.getFormattedValue()

                if newValue is not None \
                        and (oldValue is None) \
                        or self.isNullSettingAllowed() \
                        and newValue == self.getNullRepresentation():
                    newValue = None

                if newValue != oldValue \
                        and (newValue is None) \
                        or (not (newValue == oldValue)):
                    wasModified = self.isModified()
                    self.setValue(newValue, True)

                    # If the modified status changes, or if we have a
                    # formatter, repaint is needed after all.
                    if (self._format is not None) or (wasModified != self.isModified()):
                        self.requestRepaint()

            self.firePendingTextChangeEvent()

            if FocusEvent.EVENT_ID in variables:
                self.fireEvent(FocusEvent(self))

            if BlurEvent.EVENT_ID in variables:
                self.fireEvent(BlurEvent(self))
        finally:
            self._changingVariables = False


    def getType(self):
        return basestring


    def getNullRepresentation(self):
        """Gets the null-string representation.

        <p>
        The null-valued strings are represented on the user interface by
        replacing the null value with this string. If the null representation is
        set null (not 'null' string), painting null value throws exception.
        </p>

        <p>
        The default value is string 'null'.
        </p>

        @return the String Textual representation for null strings.
        @see TextField#isNullSettingAllowed()
        """
        return self._nullRepresentation


    def isNullSettingAllowed(self):
        """Is setting nulls with null-string representation allowed.

        <p>
        If this property is true, writing null-representation string to text
        field always sets the field value to real null. If this property is
        false, null setting is not made, but the null values are maintained.
        Maintenance of null-values is made by only converting the textfield
        contents to real null, if the text field matches the null-string
        representation and the current value of the field is null.
        </p>

        <p>
        By default this setting is false
        </p>

        @return boolean Should the null-string represenation be always converted
                to null-values.
        @see TextField#getNullRepresentation()
        """
        return self._nullSettingAllowed


    def setNullRepresentation(self, nullRepresentation):
        """Sets the null-string representation.

        <p>
        The null-valued strings are represented on the user interface by
        replacing the null value with this string. If the null representation is
        set null (not 'null' string), painting null value throws exception.
        </p>

        <p>
        The default value is string 'null'
        </p>

        @param nullRepresentation
                   Textual representation for null strings.
        @see TextField#setNullSettingAllowed(boolean)
        """
        self._nullRepresentation = nullRepresentation
        self.requestRepaint()


    def setNullSettingAllowed(self, nullSettingAllowed):
        """Sets the null conversion mode.

        <p>
        If this property is true, writing null-representation string to text
        field always sets the field value to real null. If this property is
        false, null setting is not made, but the null values are maintained.
        Maintenance of null-values is made by only converting the textfield
        contents to real null, if the text field matches the null-string
        representation and the current value of the field is null.
        </p>

        <p>
        By default this setting is false.
        </p>

        @param nullSettingAllowed
                   Should the null-string representation always be converted to
                   null-values.
        @see TextField#getNullRepresentation()
        """
        self._nullSettingAllowed = nullSettingAllowed
        self.requestRepaint()


    def getFormat(self):
        """Gets the value formatter of TextField.

        @return the Format used to format the value.
        @deprecated replaced by {@link com.vaadin.data.util.PropertyFormatter}
        """
        return self._format


    def setFormat(self, fmt):
        """Gets the value formatter of TextField.

        @param format
                   the Format used to format the value. Null disables the
                   formatting.
        @deprecated replaced by {@link com.vaadin.data.util.PropertyFormatter}
        """
        self._format = fmt
        self.requestRepaint()


    def isEmpty(self):
        return super(AbstractTextField, self).isEmpty() or (len(str(self)) == 0)


    def getMaxLength(self):
        """Returns the maximum number of characters in the field. Value -1 is
        considered unlimited. Terminal may however have some technical limits.

        @return the maxLength
        """
        return self._maxLength


    def setMaxLength(self, maxLength):
        """Sets the maximum number of characters in the field. Value -1 is
        considered unlimited. Terminal may however have some technical limits.

        @param maxLength
                   the maxLength to set
        """
        self._maxLength = maxLength
        self.requestRepaint()


    def getColumns(self):
        """Gets the number of columns in the editor. If the number of columns is set
        0, the actual number of displayed columns is determined implicitly by the
        adapter.

        @return the number of columns in the editor.
        """
        return self._columns


    def setColumns(self, columns):
        """Sets the number of columns in the editor. If the number of columns is set
        0, the actual number of displayed columns is determined implicitly by the
        adapter.

        @param columns
                   the number of columns to set.
        """
        if columns < 0:
            columns = 0
        self._columns = columns
        self.requestRepaint()


    def getInputPrompt(self):
        """Gets the current input prompt.

        @see #setInputPrompt(String)
        @return the current input prompt, or null if not enabled
        """
        return self._inputPrompt


    def setInputPrompt(self, inputPrompt):
        """Sets the input prompt - a textual prompt that is displayed when the field
        would otherwise be empty, to prompt the user for input.

        @param inputPrompt
        """
        # ** Text Change Events **
        self._inputPrompt = inputPrompt
        self.requestRepaint()


    def firePendingTextChangeEvent(self):
        if self._textChangeEventPending:
            self._textChangeEventPending = False
            self.fireEvent( TextChangeEventImpl(self) )


    def setInternalValue(self, newValue):
        if self._changingVariables and not self._textChangeEventPending:
            # Fire a "simulated" text change event before value change event if
            # change is coming from the client side.
            #
            # Iff there is both value change and textChangeEvent in same
            # variable burst, it is a text field in non immediate mode and the
            # text change event "flushed" queued value change event. In this
            # case textChangeEventPending flag is already on and text change
            # event will be fired after the value change event.
            if newValue is None and self._lastKnownTextContent is not None \
                    and not (self._lastKnownTextContent == self.getNullRepresentation()):
                # Value was changed from something to null representation
                self._lastKnownTextContent = self.getNullRepresentation()
                self._textChangeEventPending = True
            elif newValue is not None \
                    and not (str(newValue) == self._lastKnownTextContent):
                # Value was changed to something else than null representation
                self._lastKnownTextContent = str(newValue)
                self._textChangeEventPending = True

            self.firePendingTextChangeEvent()

        super(AbstractTextField, self).setInternalValue(newValue)


    def handleInputEventTextChange(self, variables):
        # TODO we could vastly optimize the communication of values by using
        # some sort of diffs instead of always sending the whole text content.
        # Also on value change events we could use the mechanism.
        obj = variables[VTextField.VAR_CUR_TEXT]
        self._lastKnownTextContent = obj
        self._textChangeEventPending = True


    def setTextChangeEventMode(self, inputEventMode):
        """Sets the mode how the TextField triggers {@link TextChangeEvent}s.

        @param inputEventMode
                   the new mode

        @see TextChangeEventMode
        """
        self._textChangeEventMode = inputEventMode
        self.requestRepaint()


    def getTextChangeEventMode(self):
        """@return the mode used to trigger {@link TextChangeEvent}s."""
        return self._textChangeEventMode


    def addListener(self, listener):
        if isinstance(listener, BlurListener):
            self.addListener(BlurEvent.EVENT_ID, BlurEvent, listener,
                             BlurListener.blurMethod)

        elif isinstance(listener, FocusListener):
            self.addListener(FocusEvent.EVENT_ID, FocusEvent, listener,
                             FocusListener.focusMethod)

        else:
            self.addListener(TextChangeListener.EVENT_ID, TextChangeEvent,
                             listener, TextChangeListener.EVENT_METHOD)


    def removeListener(self, listener):
        if isinstance(listener, BlurListener):
            self.removeListener(BlurEvent.EVENT_ID, BlurEvent, listener)

        elif isinstance(listener, FocusListener):
            self.removeListener(FocusEvent.EVENT_ID, FocusEvent, listener)

        else:
            self.removeListener(TextChangeListener.EVENT_ID, TextChangeEvent,
                                listener)


    def setTextChangeTimeout(self, timeout):
        """The text change timeout modifies how often text change events are
        communicated to the application when {@link #getTextChangeEventMode()} is
        {@link TextChangeEventMode#LAZY} or {@link TextChangeEventMode#TIMEOUT}.


        @see #getTextChangeEventMode()

        @param timeout
                   the timeout in milliseconds
        """
        self._textChangeEventTimeout = timeout
        self.requestRepaint()


    def getTextChangeTimeout(self):
        """Gets the timeout used to fire {@link TextChangeEvent}s when the
        {@link #getTextChangeEventMode()} is {@link TextChangeEventMode#LAZY} or
        {@link TextChangeEventMode#TIMEOUT}.

        @return the timeout value in milliseconds
        """
        return self._textChangeEventTimeout


    def getCurrentTextContent(self):
        """Gets the current (or the last known) text content in the field.
        <p>
        Note the text returned by this method is not necessary the same that is
        returned by the {@link #getValue()} method. The value is updated when the
        terminal fires a value change event via e.g. blurring the field or by
        pressing enter. The value returned by this method is updated also on
        {@link TextChangeEvent}s. Due to this high dependency to the terminal
        implementation this method is (at least at this point) not published.

        @return the text which is currently displayed in the field.
        """
        if self._lastKnownTextContent is not None:
            return self._lastKnownTextContent
        else:
            text = self.getValue()
            if text is None:
                return self.getNullRepresentation()
            return str(text)


    def selectAll(self):
        """Selects all text in the field.

        @since 6.4
        """
        text = '' if self.getValue() is None else str(self.getValue())
        self.setSelectionRange(0, len(text))


    def setSelectionRange(self, pos, length):
        """Sets the range of text to be selected.

        As a side effect the field will become focused.

        @since 6.4

        @param pos
                   the position of the first character to be selected
        @param length
                   the number of characters to be selected
        """
        self._selectionPosition = pos
        self._selectionLength = length
        self.focus()
        self.requestRepaint()


    def setCursorPosition(self, pos):
        """Sets the cursor position in the field. As a side effect the field will
        become focused.

        @since 6.4

        @param pos
                   the position for the cursor
        """
        self.setSelectionRange(pos, 0)
        self._lastKnownCursorPosition = pos


    def getCursorPosition(self):
        """Returns the last known cursor position of the field.

        <p>
        Note that due to the client server nature or the GWT terminal, Vaadin
        cannot provide the exact value of the cursor position in most situations.
        The value is updated only when the client side terminal communicates to
        TextField, like on {@link ValueChangeEvent}s and {@link TextChangeEvent}
        s. This may change later if a deep push integration is built to Vaadin.

        @return the cursor position
        """
        return self._lastKnownCursorPosition


class TextChangeEventImpl(TextChangeEvent):

    def __init__(self, tf):
        super(TextChangeEventImpl, self)(tf)
        self._curText = tf.getCurrentTextContent()
        self._cursorPosition = tf.getCursorPosition()


    def getComponent(self):
        return super(TextChangeEventImpl, self).getComponent()


    def getText(self):
        return self._curText


    def getCursorPosition(self):
        return self._cursorPosition