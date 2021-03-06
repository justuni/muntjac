# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from unittest import TestCase

from muntjac.data.container import IFilter
from muntjac.data.property import IProperty, ReadOnlyException
from muntjac.data.util.object_property import ObjectProperty
from muntjac.data.util.propertyset_item import PropertysetItem


class AbstractFilterTest(TestCase):

    PROPERTY1 = 'property1'
    PROPERTY2 = 'property2'


class TestItem(PropertysetItem):

    def __init__(self, value1, value2):
        super(TestItem, self).__init__()

        self.addItemProperty(AbstractFilterTest.PROPERTY1,
                ObjectProperty(value1))
        self.addItemProperty(AbstractFilterTest.PROPERTY2,
                ObjectProperty(value2))


class NullProperty(IProperty):

    def getValue(self):
        return None


    def setValue(self, newValue):
        raise ReadOnlyException()


    def getType(self):
        return str


    def isReadOnly(self):
        return True


    def setReadOnly(self, newStatus):
        pass  # do nothing


    def __str__(self):
        return ""


class SameItemFilter(IFilter):

    def __init__(self, item, propertyId=''):
        self._item = item
        self._propertyId = propertyId


    def passesFilter(self, itemId, item):
        return self._item == item


    def appliesToProperty(self, propertyId):
        if self._propertyId is not None:
            return self._propertyId == propertyId
        else:
            return True


    def __eq__(self, obj):
        if (obj is None) or (self.__class__ != obj.__class__):
            return False

        other = obj

        if self._propertyId is None:
            return self._item == other.item and other.propertyId is None
        else:
            return self._propertyId == other.propertyId


    def __hash__(self):
        return hash(self._item)
