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

from com.vaadin.data.Validator import (Validator,)


class NullValidator(Validator):
    """This validator is used for validating properties that do or do not allow null
    values. By default, nulls are not allowed.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    _onlyNullAllowed = None
    _errorMessage = None

    def __init__(self, errorMessage, onlyNullAllowed):
        """Creates a new NullValidator.

        @param errorMessage
                   the error message to display on invalidation.
        @param onlyNullAllowed
                   Are only nulls allowed?
        """
        self.setErrorMessage(errorMessage)
        self.setNullAllowed(onlyNullAllowed)

    def validate(self, value):
        """Validates the data given in value.

        @param value
                   the value to validate.
        @throws Validator.InvalidValueException
                    if the value was invalid.
        """
        if (
            (self._onlyNullAllowed and value is not None) or (not self._onlyNullAllowed and value is None)
        ):
            raise Validator.InvalidValueException(self._errorMessage)

    def isValid(self, value):
        """Tests if the given value is valid.

        @param value
                   the value to validate.
        @returns <code>true</code> for valid value, otherwise <code>false</code>.
        """
        return value is None if self._onlyNullAllowed else value is not None

    def isNullAllowed(self):
        """Returns <code>true</code> if nulls are allowed otherwise
        <code>false</code>.
        """
        return self._onlyNullAllowed

    def setNullAllowed(self, onlyNullAllowed):
        """Sets if nulls (and only nulls) are to be allowed.

        @param onlyNullAllowed
                   If true, only nulls are allowed. If false only non-nulls are
                   allowed. Do we allow nulls?
        """
        self._onlyNullAllowed = onlyNullAllowed

    def getErrorMessage(self):
        """Gets the error message that is displayed in case the value is invalid.

        @return the Error Message.
        """
        return self._errorMessage

    def setErrorMessage(self, errorMessage):
        """Sets the error message to be displayed on invalid value.

        @param errorMessage
                   the Error Message to set.
        """
        self._errorMessage = errorMessage