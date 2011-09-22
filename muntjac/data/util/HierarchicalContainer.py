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
from com.vaadin.data.Container import (Container, Hierarchical,)
from com.vaadin.data.util.IndexedContainer import (IndexedContainer,)
# from java.util.HashMap import (HashMap,)
# from java.util.Set import (Set,)


class HierarchicalContainer(IndexedContainer, Container, Hierarchical):
    """A specialized Container whose contents can be accessed like it was a
    tree-like structure.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Set of IDs of those contained Items that can't have children.
    _noChildrenAllowed = set()
    # Mapping from Item ID to parent Item ID.
    _parent = dict()
    # Mapping from Item ID to parent Item ID for items included in the filtered
    # container.

    _filteredParent = None
    # Mapping from Item ID to a list of child IDs.
    _children = dict()
    # Mapping from Item ID to a list of child IDs when filtered
    _filteredChildren = None
    # List that contains all root elements of the container.
    _roots = LinkedList()
    # List that contains all filtered root elements of the container.
    _filteredRoots = None
    # Determines how filtering of the container is done.
    _includeParentsWhenFiltering = True
    _contentChangedEventsDisabled = False
    _contentsChangedEventPending = None
    # Can the specified Item have any children? Don't add a JavaDoc comment
    # here, we use the default documentation from implemented interface.

    def areChildrenAllowed(self, itemId):
        # Gets the IDs of the children of the specified Item. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        if itemId in self._noChildrenAllowed:
            return False
        return self.containsId(itemId)

    def getChildren(self, itemId):
        # Gets the ID of the parent of the specified Item. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        if self._filteredChildren is not None:
            c = self._filteredChildren[itemId]
        else:
            c = self._children[itemId]
        if c is None:
            return None
        return Collections.unmodifiableCollection(c)

    def getParent(self, itemId):
        # Is the Item corresponding to the given ID a leaf node? Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.

        if self._filteredParent is not None:
            return self._filteredParent[itemId]
        return self._parent[itemId]

    def hasChildren(self, itemId):
        # Is the Item corresponding to the given ID a root node? Don't add a
        # JavaDoc comment here, we use the default documentation from implemented
        # interface.

        if self._filteredChildren is not None:
            return itemId in self._filteredChildren
        else:
            return itemId in self._children

    def isRoot(self, itemId):
        # If the container is filtered the itemId must be among filteredRoots
        # to be a root.
        # Gets the IDs of the root elements in the container. Don't add a JavaDoc
        # comment here, we use the default documentation from implemented
        # interface.

        if self._filteredRoots is not None:
            if not self._filteredRoots.contains(itemId):
                return False
        elif itemId in self._parent:
            return False
        # Container is not filtered
        return self.containsId(itemId)

    def rootItemIds(self):
        if self._filteredRoots is not None:
            return Collections.unmodifiableCollection(self._filteredRoots)
        else:
            return Collections.unmodifiableCollection(self._roots)

    def setChildrenAllowed(self, itemId, childrenAllowed):
        """<p>
        Sets the given Item's capability to have children. If the Item identified
        with the itemId already has children and the areChildrenAllowed is false
        this method fails and <code>false</code> is returned; the children must
        be first explicitly removed with
        {@link #setParent(Object itemId, Object newParentId)} or
        {@link com.vaadin.data.Container#removeItem(Object itemId)}.
        </p>

        @param itemId
                   the ID of the Item in the container whose child capability is
                   to be set.
        @param childrenAllowed
                   the boolean value specifying if the Item can have children or
                   not.
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        """
        # Checks that the item is in the container
        if not self.containsId(itemId):
            return False
        # Updates status
        if childrenAllowed:
            self._noChildrenAllowed.remove(itemId)
        else:
            self._noChildrenAllowed.add(itemId)
        return True

    def setParent(self, itemId, newParentId):
        """<p>
        Sets the parent of an Item. The new parent item must exist and be able to
        have children. (<code>canHaveChildren(newParentId) == true</code>). It is
        also possible to detach a node from the hierarchy (and thus make it root)
        by setting the parent <code>null</code>.
        </p>

        @param itemId
                   the ID of the item to be set as the child of the Item
                   identified with newParentId.
        @param newParentId
                   the ID of the Item that's to be the new parent of the Item
                   identified with itemId.
        @return <code>true</code> if the operation succeeded, <code>false</code>
                if not
        """
        # Checks that the item is in the container
        if not self.containsId(itemId):
            return False
        # Gets the old parent
        oldParentId = self._parent[itemId]
        # Checks if no change is necessary
        if (
            (newParentId is None and oldParentId is None) or (newParentId is not None and newParentId == oldParentId)
        ):
            return True
        # Making root?
        if newParentId is None:
            # The itemId should become a root so we need to
            # - Remove it from the old parent's children list
            # - Add it as a root
            # - Remove it from the item -> parent list (parent is null for
            # roots)
            # Removes from old parents children list
            l = self._children[oldParentId]
            if l is not None:
                l.remove(itemId)
                if l.isEmpty():
                    self._children.remove(oldParentId)
            # Add to be a root
            self._roots.add(itemId)
            # Updates parent
            self._parent.remove(itemId)
            if self.hasFilters():
                # Refilter the container if setParent is called when filters
                # are applied. Changing parent can change what is included in
                # the filtered version (if includeParentsWhenFiltering==true).
                self.doFilterContainer(self.hasFilters())
            self.fireItemSetChange()
            return True
        # We get here when the item should not become a root and we need to
        # - Verify the new parent exists and can have children
        # - Check that the new parent is not a child of the selected itemId
        # - Updated the item -> parent mapping to point to the new parent
        # - Remove the item from the roots list if it was a root
        # - Remove the item from the old parent's children list if it was not a
        # root
        # Checks that the new parent exists in container and can have
        # children
        if (
            (not self.containsId(newParentId)) or (newParentId in self._noChildrenAllowed)
        ):
            return False
        # Checks that setting parent doesn't result to a loop
        o = newParentId
        while o is not None and not (o == itemId):
            o = self._parent[o]
        if o is not None:
            return False
        # Updates parent
        self._parent.put(itemId, newParentId)
        pcl = self._children[newParentId]
        if pcl is None:
            # Create an empty list for holding children if one were not
            # previously created
            pcl = LinkedList()
            self._children.put(newParentId, pcl)
        pcl.add(itemId)
        # Removes from old parent or root
        if oldParentId is None:
            self._roots.remove(itemId)
        else:
            l = self._children[oldParentId]
            if l is not None:
                l.remove(itemId)
                if l.isEmpty():
                    self._children.remove(oldParentId)
        if self.hasFilters():
            # Refilter the container if setParent is called when filters
            # are applied. Changing parent can change what is included in
            # the filtered version (if includeParentsWhenFiltering==true).
            self.doFilterContainer(self.hasFilters())
        self.fireItemSetChange()
        return True

    def hasFilters(self):
        return self._filteredRoots is not None

    def moveAfterSibling(self, itemId, siblingId):
        """Moves a node (an Item) in the container immediately after a sibling node.
        The two nodes must have the same parent in the container.

        @param itemId
                   the identifier of the moved node (Item)
        @param siblingId
                   the identifier of the reference node (Item), after which the
                   other node will be located
        """
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.util.IndexedContainer#addItem()

        parent2 = self.getParent(itemId)
        if parent2 is None:
            childrenList = self._roots
        else:
            childrenList = self._children[parent2]
        if siblingId is None:
            childrenList.remove(itemId)
            childrenList.addFirst(itemId)
        else:
            oldIndex = childrenList.index(itemId)
            indexOfSibling = childrenList.index(siblingId)
            if indexOfSibling != -1 and oldIndex != -1:
                if oldIndex > indexOfSibling:
                    newIndex = indexOfSibling + 1
                else:
                    newIndex = indexOfSibling
                childrenList.remove(oldIndex)
                childrenList.add(newIndex, itemId)
            else:
                raise self.IllegalArgumentException('Given identifiers no not have the same parent.')
        self.fireItemSetChange()

    def addItem(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.disableContentsChangeEvents()
            itemId = super(HierarchicalContainer, self).addItem()
            if itemId is None:
                return None
            if not self._roots.contains(itemId):
                self._roots.add(itemId)
                if self._filteredRoots is not None:
                    if self.passesFilters(itemId):
                        self._filteredRoots.add(itemId)
            self.enableAndFireContentsChangeEvents()
            return itemId
        elif _1 == 1:
            itemId, = _0
            self.disableContentsChangeEvents()
            item = super(HierarchicalContainer, self).addItem(itemId)
            if item is None:
                return None
            self._roots.add(itemId)
            if self._filteredRoots is not None:
                if self.passesFilters(itemId):
                    self._filteredRoots.add(itemId)
            self.enableAndFireContentsChangeEvents()
            return item
        else:
            raise ARGERROR(0, 1)

    def fireItemSetChange(self, event):
        if self.contentsChangeEventsOn():
            super(HierarchicalContainer, self).fireItemSetChange(event)
        else:
            self._contentsChangedEventPending = True

    def contentsChangeEventsOn(self):
        return not self._contentChangedEventsDisabled

    def disableContentsChangeEvents(self):
        self._contentChangedEventsDisabled = True

    def enableAndFireContentsChangeEvents(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.util.IndexedContainer#addItem(java.lang.Object)

        self._contentChangedEventsDisabled = False
        if self._contentsChangedEventPending:
            self.fireItemSetChange()
        self._contentsChangedEventPending = False

    # (non-Javadoc)
    # 
    # @see com.vaadin.data.util.IndexedContainer#removeAllItems()

    def removeAllItems(self):
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.util.IndexedContainer#removeItem(java.lang.Object )

        self.disableContentsChangeEvents()
        success = super(HierarchicalContainer, self).removeAllItems()
        if success:
            self._roots.clear()
            self._parent.clear()
            self._children.clear()
            self._noChildrenAllowed.clear()
            if self._filteredRoots is not None:
                self._filteredRoots = None
            if self._filteredChildren is not None:
                self._filteredChildren = None
            if self._filteredParent is not None:
                self._filteredParent = None
        self.enableAndFireContentsChangeEvents()
        return success

    def removeItem(self, itemId):
        self.disableContentsChangeEvents()
        success = super(HierarchicalContainer, self).removeItem(itemId)
        if success:
            # Remove from roots if this was a root
            if self._roots.remove(itemId):
                # If filtering is enabled we might need to remove it from the
                # filtered list also
                if self._filteredRoots is not None:
                    self._filteredRoots.remove(itemId)
            # Clear the children list. Old children will now become root nodes
            childNodeIds = self._children.remove(itemId)
            if childNodeIds is not None:
                if self._filteredChildren is not None:
                    self._filteredChildren.remove(itemId)
                for childId in childNodeIds:
                    self.setParent(childId, None)
            # Parent of the item that we are removing will contain the item id
            # in its children list
            parentItemId = self._parent[itemId]
            if parentItemId is not None:
                c = self._children[parentItemId]
                if c is not None:
                    c.remove(itemId)
                    if c.isEmpty():
                        self._children.remove(parentItemId)
                    # Found in the children list so might also be in the
                    # filteredChildren list
                    if self._filteredChildren is not None:
                        f = self._filteredChildren[parentItemId]
                        if f is not None:
                            f.remove(itemId)
                            if f.isEmpty():
                                self._filteredChildren.remove(parentItemId)
            self._parent.remove(itemId)
            if self._filteredParent is not None:
                # Item id no longer has a parent as the item id is not in the
                # container.
                self._filteredParent.remove(itemId)
            self._noChildrenAllowed.remove(itemId)
        self.enableAndFireContentsChangeEvents()
        return success

    def removeItemRecursively(self, *args):
        """Removes the Item identified by given itemId and all its children.

        @see #removeItem(Object)
        @param itemId
                   the identifier of the Item to be removed
        @return true if the operation succeeded
        ---
        Removes the Item identified by given itemId and all its children from the
        given Container.

        @param container
                   the container where the item is to be removed
        @param itemId
                   the identifier of the Item to be removed
        @return true if the operation succeeded
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            itemId, = _0
            self.disableContentsChangeEvents()
            removeItemRecursively = removeItemRecursively(self, itemId)
            self.enableAndFireContentsChangeEvents()
            return removeItemRecursively
        elif _1 == 2:
            container, itemId = _0
            success = True
            children2 = container.getChildren(itemId)
            if children2 is not None:
                array = list(children2)
                _0 = True
                i = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        i += 1
                    if not (i < len(array)):
                        break
                    removeItemRecursively = removeItemRecursively(container, array[i])
                    if not removeItemRecursively:
                        success = False
            # remove the root of subtree if children where succesfully removed
            if success:
                success = container.removeItem(itemId)
            return success
        else:
            raise ARGERROR(1, 2)

    # (non-Javadoc)
    # 
    # @see com.vaadin.data.util.IndexedContainer#doSort()

    def doSort(self):
        super(HierarchicalContainer, self).doSort()
        Collections.sort(self._roots, self.getItemSorter())
        for childList in self._children.values():
            Collections.sort(childList, self.getItemSorter())

    def isIncludeParentsWhenFiltering(self):
        """Used to control how filtering works. @see
        {@link #setIncludeParentsWhenFiltering(boolean)} for more information.

        @return true if all parents for items that match the filter are included
                when filtering, false if only the matching items are included
        """
        return self._includeParentsWhenFiltering

    def setIncludeParentsWhenFiltering(self, includeParentsWhenFiltering):
        """Controls how the filtering of the container works. Set this to true to
        make filtering include parents for all matched items in addition to the
        items themselves. Setting this to false causes the filtering to only
        include the matching items and make items with excluded parents into root
        items.

        @param includeParentsWhenFiltering
                   true to include all parents for items that match the filter,
                   false to only include the matching items
        """
        # Overridden to provide filtering for root & children items.
        # 
        # (non-Javadoc)
        # 
        # @see com.vaadin.data.util.IndexedContainer#updateContainerFiltering()

        self._includeParentsWhenFiltering = includeParentsWhenFiltering
        if self._filteredRoots is not None:
            # Currently filtered so needs to be re-filtered
            self.doFilterContainer(True)

    def doFilterContainer(self, hasFilters):
        if not hasFilters:
            # All filters removed
            self._filteredRoots = None
            self._filteredChildren = None
            self._filteredParent = None
            return super(HierarchicalContainer, self).doFilterContainer(hasFilters)
        # Reset data structures
        self._filteredRoots = LinkedList()
        self._filteredChildren = dict()
        self._filteredParent = dict()
        if self._includeParentsWhenFiltering:
            # Filter so that parents for items that match the filter are also
            # included
            includedItems = set()
            for rootId in self._roots:
                if self.filterIncludingParents(rootId, includedItems):
                    self._filteredRoots.add(rootId)
                    self.addFilteredChildrenRecursively(rootId, includedItems)
            # includedItemIds now contains all the item ids that should be
            # included. Filter IndexedContainer based on this
            self._filterOverride = includedItems
            super(HierarchicalContainer, self).doFilterContainer(hasFilters)
            self._filterOverride = None
            return True
        else:
            # Filter by including all items that pass the filter and make items
            # with no parent new root items
            # Filter IndexedContainer first so getItemIds return the items that
            # match
            super(HierarchicalContainer, self).doFilterContainer(hasFilters)
            filteredItemIds = self.LinkedHashSet(self.getItemIds())
            for itemId in filteredItemIds:
                itemParent = self._parent[itemId]
                if (itemParent is None) or (not filteredItemIds.contains(itemParent)):
                    # Parent is not included or this was a root, in both cases
                    # this should be a filtered root
                    self._filteredRoots.add(itemId)
                else:
                    # Parent is included. Add this to the children list (create
                    # it first if necessary)
                    self.addFilteredChild(itemParent, itemId)
            return True

    def addFilteredChild(self, parentItemId, childItemId):
        """Adds the given childItemId as a filteredChildren for the parentItemId and
        sets it filteredParent.

        @param parentItemId
        @param childItemId
        """
        parentToChildrenList = self._filteredChildren[parentItemId]
        if parentToChildrenList is None:
            parentToChildrenList = LinkedList()
            self._filteredChildren.put(parentItemId, parentToChildrenList)
        self._filteredParent.put(childItemId, parentItemId)
        parentToChildrenList.add(childItemId)

    def addFilteredChildrenRecursively(self, parentItemId, includedItems):
        """Recursively adds all items in the includedItems list to the
        filteredChildren map in the same order as they are in the children map.
        Starts from parentItemId and recurses down as long as child items that
        should be included are found.

        @param parentItemId
                   The item id to start recurse from. Not added to a
                   filteredChildren list
        @param includedItems
                   Set containing the item ids for the items that should be
                   included in the filteredChildren map
        """
        childList = self._children[parentItemId]
        if childList is None:
            return
        for childItemId in childList:
            if childItemId in includedItems:
                self.addFilteredChild(parentItemId, childItemId)
                self.addFilteredChildrenRecursively(childItemId, includedItems)

    def filterIncludingParents(self, itemId, includedItems):
        """Scans the itemId and all its children for which items should be included
        when filtering. All items which passes the filters are included.
        Additionally all items that have a child node that should be included are
        also themselves included.

        @param itemId
        @param includedItems
        @return true if the itemId should be included in the filtered container.
        """
        toBeIncluded = self.passesFilters(itemId)
        childList = self._children[itemId]
        if childList is not None:
            for childItemId in self._children[itemId]:
                toBeIncluded |= self.filterIncludingParents(childItemId, includedItems)
        if toBeIncluded:
            includedItems.add(itemId)
        return toBeIncluded

    _filterOverride = None
    # (non-Javadoc)
    # 
    # @see
    # com.vaadin.data.util.IndexedContainer#passesFilters(java.lang.Object)

    def passesFilters(self, itemId):
        if self._filterOverride is not None:
            return itemId in self._filterOverride
        else:
            return super(HierarchicalContainer, self).passesFilters(itemId)