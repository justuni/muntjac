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

from muntjac.event.dd.acceptcriteria.accept_criterion import IAcceptCriterion


class ClientSideCriterion(IAcceptCriterion):
    """Parent class for criteria that can be completely validated on client side.
    All classes that provide criteria that can be completely validated on client
    side should extend this class.

    It is recommended that subclasses of ClientSideCriterion re-validate the
    condition on the server side in
    {@link IAcceptCriterion#accept(com.vaadin.event.dd.DragAndDropEvent)} after
    the client side validation has accepted a transfer.

    @since 6.3
    """

    def isClientSideVerifiable(self):
        return True


    def paint(self, target):
        target.startTag('-ac')
        target.addAttribute('name', self.getIdentifier())
        self.paintContent(target)
        target.endTag('-ac')


    def paintContent(self, target):
        pass


    def getIdentifier(self):
        return self.getClass().getCanonicalName()


    def paintResponse(self, target):
        # NOP, nothing to do as this is client side verified criterion
        pass