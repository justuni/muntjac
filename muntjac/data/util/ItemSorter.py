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

# from java.io.Serializable import (Serializable,)


class ItemSorter(Comparator, Cloneable, Serializable):
    """An item comparator which is compatible with the {@link Sortable} interface.
    The <code>ItemSorter</code> interface can be used in <code>Sortable</code>
    implementations to provide a custom sorting method.
    """

    def setSortProperties(self, container, propertyId, ascending):
        """Sets the parameters for an upcoming sort operation. The parameters
        determine what container to sort and how the <code>ItemSorter</code>
        sorts the container.

        @param container
                   The container that will be sorted. The container must contain
                   the propertyIds given in the <code>propertyId</code>
                   parameter.
        @param propertyId
                   The property ids used for sorting. The property ids must exist
                   in the container and should only be used if they are also
                   sortable, i.e include in the collection returned by
                   <code>container.getSortableContainerPropertyIds()</code>. See
                   {@link Sortable#sort(Object[], boolean[])} for more
                   information.
        @param ascending
                   Sorting order flags for each property id. See
                   {@link Sortable#sort(Object[], boolean[])} for more
                   information.
        """
        pass

    def compare(self, itemId1, itemId2):
        """Compares its two arguments for order. Returns a negative integer, zero,
        or a positive integer as the first argument is less than, equal to, or
        greater than the second.
        <p>
        The parameters for the <code>ItemSorter</code> <code>compare()</code>
        method must always be item ids which exist in the container set using
        {@link #setSortProperties(Sortable, Object[], boolean[])}.

        @see Comparator#compare(Object, Object)
        """
        pass