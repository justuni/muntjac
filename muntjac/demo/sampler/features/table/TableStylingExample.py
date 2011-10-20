
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.ui import VerticalLayout, Table, Link, Button, button, Alignment
from muntjac.event.action import Action
from muntjac.event import action
from muntjac.ui.table import IColumnGenerator, ICellStyleGenerator
from muntjac.terminal.external_resource import ExternalResource
from muntjac.event.item_click_event import IItemClickListener, ItemClickEvent


class TableStylingExample(VerticalLayout):

    ACTION_RED = Action('red')
    ACTION_BLUE = Action('blue')
    ACTION_GREEN = Action('green')
    ACTION_NONE = Action('none')
    ACTIONS = [ACTION_RED, ACTION_GREEN, ACTION_BLUE, ACTION_NONE]

    def __init__(self):
        self.setSpacing(True)

        self._table = Table()
        self._markedRows = dict()
        self._markedCells = dict()

        self.addComponent(self._table)

        # set a style name, so we can style rows and cells
        self._table.setStyleName('contacts')

        # size
        self._table.setWidth('100%')
        self._table.setPageLength(7)

        # connect data source
        self._table.setContainerDataSource(ExampleUtil.getPersonContainer())

        # Generate the email-link from firstname & lastname
        class TableColumnGenerator(IColumnGenerator):

            def __init__(self, c):
                self._c = c

            def generateCell(self, source, itemId, columnId):
                item = self._c._table.getItem(itemId)
                fn = item.getItemProperty(ExampleUtil.PERSON_PROPERTY_FIRSTNAME).getValue()
                ln = item.getItemProperty(ExampleUtil.PERSON_PROPERTY_LASTNAME).getValue()
                email = fn.lower() + '.' + ln.lower() + '@example.com'
                # the Link -component:
                emailLink = Link(email, ExternalResource('mailto:' + email))
                return emailLink

        self._table.addGeneratedColumn('Email', TableColumnGenerator(self))

        # turn on column reordering and collapsing
        self._table.setColumnReorderingAllowed(True)
        self._table.setColumnCollapsingAllowed(True)

        # Actions (a.k.a context menu)
        class TableActionHandler(action.IHandler):

            def __init__(self, c):
                self._c = c

            def getActions(self, target, sender):
                return self._c.ACTIONS

            def handleAction(self, action, sender, target):
                self._c._markedRows.remove(target)
                if not (self._c.ACTION_NONE == action):
                    # we're using the cations caption as stylename as well:
                    self._c._markedRows[target] = action.getCaption()
                # this causes the CellStyleGenerator to return new styles,
                # but table can't automatically know, we must tell it:
                self._c._table.requestRepaint()

        self._table.addActionHandler( TableActionHandler(self) )

        # style generator
        class TableStyleGenerator(ICellStyleGenerator):

            def __init__(self, c):
                self._c = c

            def getStyle(self, itemId, propertyId):
                if propertyId is None:
                    # no propertyId, styling row
                    return self._c._markedRows[itemId]
                elif propertyId == 'Email':
                    # style the generated email column
                    return 'email'
                else:
                    cells = self._c._markedCells[itemId]
                    if cells is not None and propertyId in cells:
                        # marked cell
                        return 'marked'
                    else:
                        # no style
                        return None

        self._table.setCellStyleGenerator( TableStyleGenerator(self) )

        # toggle cell 'marked' styling when double-clicked
        class TableClickListener(IItemClickListener):

            def __init__(self, c):
                self._c = c

            def itemClick(self, event):
                if event.getButton() == ItemClickEvent.BUTTON_RIGHT:
                    # you can handle left/right/middle -mouseclick
                    pass
                if event.isDoubleClick():
                    itemId = event.getItemId()
                    propertyId = event.getPropertyId()
                    cells = self._c._markedCells[itemId]
                    if cells is None:
                        cells = set()
                        self._c._markedCells[itemId] = cells
                    if propertyId in cells:
                        # toggle marking off
                        cells.remove(propertyId)
                    else:
                        # toggle marking on
                        cells.add(propertyId)
                    # this causes the CellStyleGenerator to return new styles,
                    # but table can't automatically know, we must tell it:
                    self._c._table.requestRepaint()

        self._table.addListener( TableClickListener(self) )

        # Editing

        # we don't want to update container before pressing 'save':
        self._table.setWriteThrough(False)

        # edit button
        editButton = Button('Edit')
        self.addComponent(editButton)

        class EditListener(button.IClickListener):

            def __init__(self, c):
                self._c = c

            def buttonClick(self, event):
                self._c._table.setEditable(not self._c._table.isEditable())
                self.editButton.setCaption('Save' if self._c._table.isEditable() else 'Edit')

        editButton.addListener( EditListener(self) )

        self.setComponentAlignment(editButton, Alignment.TOP_RIGHT)

