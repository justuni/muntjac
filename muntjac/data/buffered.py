# Copyright (C) 2010 IT Mill Ltd.
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

import sys

from muntjac.terminal.system_error import SystemErr
from muntjac.terminal.error_message import IErrorMessage
from muntjac.data.validatable import IValidatable


class IBuffered(object):
    """Defines the interface to commit and discard changes to an object,
    supporting read-through and write-through modes.

    <i>Read-through mode</i> means that the value read from the buffered object
    is constantly up to date with the data source. <i>Write-through</i> mode
    means that all changes to the object are immediately updated to the data
    source.

    Since these modes are independent, their combinations may result in some
    behaviour that may sound surprising.

    For example, if a <code>IBuffered</code> object is in read-through mode but
    not in write-through mode, the result is an object whose value is updated
    directly from the data source only if it's not locally modified. If the value
    is locally modified, retrieving the value from the object would result in a
    value that is different than the one stored in the data source, even though
    the object is in read-through mode.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def commit(self):
        """Updates all changes since the previous commit to the data source. The
        value stored in the object will always be updated into the data source
        when <code>commit</code> is called.

        @throws SourceException
                    if the operation fails because of an exception is thrown by
                    the data source. The cause is included in the exception.
        @throws InvalidValueException
                    if the operation fails because validation is enabled and the
                    values do not validate
        """
        raise NotImplementedError


    def discard(self):
        """Discards all changes since last commit. The object updates its value
        from the data source.

        @throws SourceException
                    if the operation fails because of an exception is thrown by
                    the data source. The cause is included in the exception.
        """
        raise NotImplementedError


    def isWriteThrough(self):
        """Tests if the object is in write-through mode. If the object is in
        write-through mode, all modifications to it will result in
        <code>commit</code> being called after the modification.

        @return <code>true</code> if the object is in write-through mode,
                <code>false</code> if it's not.
        """
        raise NotImplementedError


    def setWriteThrough(self, writeThrough):
        """Sets the object's write-through mode to the specified status. When
        switching the write-through mode on, the <code>commit</code> operation
        will be performed.

        @param writeThrough
                   Boolean value to indicate if the object should be in
                   write-through mode after the call.
        @throws SourceException
                    If the operation fails because of an exception is thrown by
                    the data source.
        @throws InvalidValueException
                    If the implicit commit operation fails because of a
                    validation error.
        """
        raise NotImplementedError


    def isReadThrough(self):
        """Tests if the object is in read-through mode. If the object is in
        read-through mode, retrieving its value will result in the value being
        first updated from the data source to the object.
        <p>
        The only exception to this rule is that when the object is not in
        write-through mode and it's buffer contains a modified value, the value
        retrieved from the object will be the locally modified value in the
        buffer which may differ from the value in the data source.
        </p>

        @return <code>true</code> if the object is in read-through mode,
                <code>false</code> if it's not.
        """
        raise NotImplementedError


    def setReadThrough(self, readThrough):
        """Sets the object's read-through mode to the specified status. When
        switching read-through mode on, the object's value is updated from the
        data source.

        @param readThrough
                   Boolean value to indicate if the object should be in
                   read-through mode after the call.

        @throws SourceException
                    If the operation fails because of an exception is thrown by
                    the data source. The cause is included in the exception.
        """
        raise NotImplementedError


    def isModified(self):
        """Tests if the value stored in the object has been modified since it was
        last updated from the data source.

        @return <code>true</code> if the value in the object has been modified
                since the last data source update, <code>false</code> if not.
        """
        raise NotImplementedError


class SourceException(RuntimeError, IErrorMessage):
    """An exception that signals that one or more exceptions occurred while a
    buffered object tried to access its data source or if there is a problem
    in processing a data source.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, source, cause=None):
        """Creates a source exception that does not include a cause.

        @param source
                   the source object implementing the IBuffered interface.
        ---
        Creates a source exception from a cause exception.

        @param source
                   the source object implementing the IBuffered interface.
        @param cause
                   the original cause for this exception.
        ---
        Creates a source exception from multiple causes.

        @param source
                   the source object implementing the IBuffered interface.
        @param causes
                   the original causes for this exception.
        """
        # Source class implementing the buffered interface
        self._source = source

        # Original cause of the source exception
        self._causes = list()

        if isinstance(cause, list):
            self._causes = cause
        elif cause is not None:
            self._causes = [cause]


    def getCause(self):
        """Gets the cause of the exception.

        @return The cause for the exception.
        @throws MoreThanOneCauseException
                    if there is more than one cause for the exception. This
                    is possible if the commit operation triggers more than
                    one error at the same time.
        """
        if len(self._causes) == 0:
            return None
        return self._causes[0]


    def getCauses(self):
        """Gets all the causes for this exception.

        @return throwables that caused this exception
        """
        return self._causes


    def getSource(self):
        """Gets a source of the exception.

        @return the IBuffered object which generated this exception.
        """
        return self._source


    def getErrorLevel(self):
        """Gets the error level of this buffered source exception. The level of
        the exception is maximum error level of all the contained causes.
        <p>
        The causes that do not specify error level default to
        <code>ERROR</code> level. Also source exception without any causes
        are of level <code>ERROR</code>.
        </p>

        @see com.vaadin.terminal.IErrorMessage#getErrorLevel()
        """
        level = -sys.maxint - 1

        for i in range(len(self._causes)):
            if isinstance(self._causes[i], IErrorMessage):
                causeLevel = self._causes[i].getErrorLevel()
            else:
                causeLevel = IErrorMessage.ERROR

            if causeLevel > level:
                level = causeLevel

        return IErrorMessage.ERROR if level == -sys.maxint - 1 else level


    def paint(self, target):
        target.startTag('error')
        level = self.getErrorLevel()

        if level > 0 and level <= IErrorMessage.INFORMATION:
            target.addAttribute('level', 'info')

        elif level <= IErrorMessage.WARNING:
            target.addAttribute('level', 'warning')

        elif level <= IErrorMessage.ERROR:
            target.addAttribute('level', 'error')

        elif level <= IErrorMessage.CRITICAL:
            target.addAttribute('level', 'critical')

        else:
            target.addAttribute('level', 'system')

        # Paint all the exceptions
        for i in range(len(self._causes)):
            if isinstance(self._causes[i], IErrorMessage):
                self._causes[i].paint(target)
            else:
                SystemErr(self._causes[i]).paint(target)

        target.endTag('error')


    def addListener(self, listener):
        raise NotImplementedError


    def removeListener(self, listener):
        raise NotImplementedError


    def requestRepaint(self):
        raise NotImplementedError


    def requestRepaintRequests(self):
        raise NotImplementedError


    def getDebugId(self):
        return None


    def setDebugId(self, idd):
        raise NotImplementedError, \
                'Setting testing id for this Paintable is not implemented'


class IBufferedValidatable(IBuffered, IValidatable):
    """This interface defines the combination of <code>IValidatable</code> and
    <code>IBuffered</code> interfaces. The combination of the interfaces defines
    if the invalid data is committed to datasource.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def isInvalidCommitted(self):
        """Tests if the invalid data is committed to datasource. The default is
        <code>false</code>.
        """
        raise NotImplementedError


    def setInvalidCommitted(self, isCommitted):
        """Sets if the invalid data should be committed to datasource. The
        default is <code>false</code>.
        """
        raise NotImplementedError