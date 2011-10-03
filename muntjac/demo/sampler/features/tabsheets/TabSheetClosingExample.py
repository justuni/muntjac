# -*- coding: utf-8 -*-
# from com.vaadin.ui.TabSheet.SelectedTabChangeEvent import (SelectedTabChangeEvent,)
# from com.vaadin.ui.TabSheet.Tab import (Tab,)


class TabSheetClosingExample(VerticalLayout, TabSheet.SelectedTabChangeListener, TabSheet.CloseHandler):
    _t = None

    def __init__(self):
        # Tab 1 content
        l1 = VerticalLayout()
        l1.setMargin(True)
        l1.addComponent(ALabel('There are no previously saved actions.'))
        # Tab 2 content
        l2 = VerticalLayout()
        l2.setMargin(True)
        l2.addComponent(ALabel('There are no saved notes.'))
        # Tab 3 content
        l3 = VerticalLayout()
        l3.setMargin(True)
        l3.addComponent(ALabel('There are currently no issues.'))
        # Tab 4 content
        l4 = VerticalLayout()
        l4.setMargin(True)
        l4.addComponent(ALabel('There are no comments.'))
        # Tab 5 content
        l5 = VerticalLayout()
        l5.setMargin(True)
        l5.addComponent(ALabel('There is no new feedback.'))
        self._t = TabSheet()
        self._t.setHeight('200px')
        self._t.setWidth('400px')
        saved = self._t.addTab(l1, 'Saved actions', None)
        saved.setClosable(True)
        notes = self._t.addTab(l2, 'Notes', None)
        notes.setClosable(True)
        issues = self._t.addTab(l3, 'Issues', None)
        issues.setClosable(True)
        comments = self._t.addTab(l4, 'Comments', None)
        comments.setClosable(True)
        feedback = self._t.addTab(l5, 'Feedback', None)
        feedback.setClosable(True)
        self._t.addListener(self)
        self._t.setCloseHandler(self)
        self.addComponent(self._t)

    def selectedTabChange(self, event):
        tabsheet = event.getTabSheet()
        tab = tabsheet.getTab(tabsheet.getSelectedTab())
        if tab is not None:
            self.getWindow().showNotification('Selected tab: ' + tab.getCaption())

    def onTabClose(self, tabsheet, tabContent):
        self.getWindow().showNotification('Closed tab: ' + tabsheet.getTab(tabContent).getCaption())
        tabsheet.removeComponent(tabContent)