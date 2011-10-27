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

from muntjac.test.server.component.AbstractListenerMethodsTest import \
    AbstractListenerMethodsTest

from muntjac.ui.tree import \
    Tree, ExpandEvent, IExpandListener, CollapseEvent, ICollapseListener

from muntjac.event.item_click_event import ItemClickEvent, IItemClickListener


class TreeListeners(AbstractListenerMethodsTest):

    def testExpandListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Tree, ExpandEvent, IExpandListener)


    def testItemClickListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Tree, ItemClickEvent, IItemClickListener)


    def testCollapseListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Tree, CollapseEvent, ICollapseListener)