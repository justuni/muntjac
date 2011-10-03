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

from muntjac.ui.component_container import IComponentContainer

from muntjac.terminal.gwt.client.ui.v_margin_info import VMarginInfo
from muntjac.terminal.gwt.client.ui.alignment_info import Bits


class ILayout(IComponentContainer):
    """Extension to the {@link IComponentContainer} interface which adds the
    layouting control to the elements in the container. This is required by
    the various layout components to enable them to place other components in
    specific locations in the UI.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def setMargin(self, *args):
        """Enable layout margins. Affects all four sides of the layout. This
        will tell the client-side implementation to leave extra space around
        the layout. The client-side implementation decides the actual amount,
        and it can vary between themes.

        @param enabled
        ---
        Enable specific layout margins. This will tell the client-side
        implementation to leave extra space around the layout in specified
        edges, clockwise from top (top, right, bottom, left). The client-side
        implementation decides the actual amount, and it can vary between
        themes.

        @param top
        @param right
        @param bottom
        @param left
        """
        raise NotImplementedError


class IAlignmentHandler(object):
    """IAlignmentHandler is most commonly an advanced {@link ILayout} that
    can align its components.
    """

    # Contained component should be aligned horizontally to the left.
    #
    # @deprecated Use of {@link Alignment} class and its constants
    ALIGNMENT_LEFT = Bits.ALIGNMENT_LEFT

    # Contained component should be aligned horizontally to the right.
    #
    # @deprecated Use of {@link Alignment} class and its constants
    ALIGNMENT_RIGHT = Bits.ALIGNMENT_RIGHT

    # Contained component should be aligned vertically to the top.
    #
    # @deprecated Use of {@link Alignment} class and its constants
    ALIGNMENT_TOP = Bits.ALIGNMENT_TOP

    # Contained component should be aligned vertically to the bottom.
    #
    # @deprecated Use of {@link Alignment} class and its constants
    ALIGNMENT_BOTTOM = Bits.ALIGNMENT_BOTTOM

    # Contained component should be horizontally aligned to center.
    #
    # @deprecated Use of {@link Alignment} class and its constants
    ALIGNMENT_HORIZONTAL_CENTER = Bits.ALIGNMENT_HORIZONTAL_CENTER

    # Contained component should be vertically aligned to center.
    #
    # @deprecated Use of {@link Alignment} class and its constants
    ALIGNMENT_VERTICAL_CENTER = Bits.ALIGNMENT_VERTICAL_CENTER


    def setComponentAlignment(self, *args):
        """Set alignment for one contained component in this layout. Alignment
        is calculated as a bit mask of the two passed values.

        @deprecated Use {@link #setComponentAlignment(Component, Alignment)}
                    instead

        @param childComponent
                   the component to align within it's layout cell.
        @param horizontalAlignment
                   the horizontal alignment for the child component (left,
                   center, right). Use ALIGNMENT constants.
        @param verticalAlignment
                   the vertical alignment for the child component (top,
                   center, bottom). Use ALIGNMENT constants.
        ---
        Set alignment for one contained component in this layout. Use
        predefined alignments from Alignment class.

        Example: <code>
             layout.setComponentAlignment(myComponent, Alignment.TOP_RIGHT);
        </code>

        @param childComponent
                   the component to align within it's layout cell.
        @param alignment
                   the Alignment value to be set
        """
        raise NotImplementedError


    def getComponentAlignment(self, childComponent):
        """Returns the current Alignment of given component.

        @param childComponent
        @return the {@link Alignment}
        """
        raise NotImplementedError


class ISpacingHandler(object):
    """This type of layout supports automatic addition of space between its
    components.
    """

    def setSpacing(self, enabled):
        """Enable spacing between child components within this layout.

        <strong>NOTE:</strong> This will only affect the space between
        components, not the space around all the components in the layout
        (i.e. do not confuse this with the cellspacing attribute of a HTML
        Table). Use {@link #setMargin(boolean)} to add space around the
        layout.

        See the reference manual for more information about CSS rules for
        defining the amount of spacing to use.

        @param enabled
                   true if spacing should be turned on, false if it should be
                   turned off
        """
        raise NotImplementedError


    def isSpacingEnabled(self):
        """@return true if spacing between child components within this layout
                is enabled, false otherwise
        @deprecated Use {@link #isSpacing()} instead.
        """
        raise NotImplementedError


    def isSpacing(self):
        """@return true if spacing between child components within this layout
                is enabled, false otherwise
        """
        raise NotImplementedError


class IMarginHandler(object):
    """This type of layout supports automatic addition of margins (space around
    its components).
    """

    def setMargin(self, marginInfo):
        """Enable margins for this layout.

        <strong>NOTE:</strong> This will only affect the space around the
        components in the layout, not space between the components in the
        layout. Use {@link #setSpacing(boolean)} to add space between the
        components in the layout.

        See the reference manual for more information about CSS rules for
        defining the size of the margin.

        @param marginInfo
                   MarginInfo object containing the new margins.
        """
        raise NotImplementedError


    def getMargin(self):
        """@return MarginInfo containing the currently enabled margins."""
        raise NotImplementedError


class MarginInfo(VMarginInfo):

    def __init__(self, *args):
        pass