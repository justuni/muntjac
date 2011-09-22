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

from com.vaadin.data.Validator import (InvalidValueException, Validator,)


class AbstractValidator(Validator):
    """Abstract {@link com.vaadin.data.Validator Validator} implementation that
    provides a basic Validator implementation except the {@link #isValid(Object)}
    method. Sub-classes need to implement the {@link #isValid(Object)} method.
    <p>
    To include the value that failed validation in the exception message you can
    use "{0}" in the error message. This will be replaced with the failed value
    (converted to string using {@link #toString()}) or "null" if the value is
    null.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 5.4
    """
    # Error message that is included in an {@link InvalidValueException} if
    # such is thrown.

    _errorMessage = None

    def __init__(self, errorMessage):
        """Constructs a validator with the given error message.

        @param errorMessage
                   the message to be included in an {@link InvalidValueException}
                   (with "{0}" replaced by the value that failed validation).
        """
        self._errorMessage = errorMessage

    def validate(self, value):
        if not self.isValid(value):
            message = self._errorMessage.replace('{0}', String.valueOf.valueOf(value))
            raise InvalidValueException(message)

    def getErrorMessage(self):
        """Returns the message to be included in the exception in case the value
        does not validate.

        @return the error message provided in the constructor or using
                {@link #setErrorMessage(String)}.
        """
        return self._errorMessage

    def setErrorMessage(self, errorMessage):
        """Sets the message to be included in the exception in case the value does
        not validate. The exception message is typically shown to the end user.

        @param errorMessage
                   the error message. "{0}" is automatically replaced by the
                   value that did not validate.
        """
        self._errorMessage = errorMessage