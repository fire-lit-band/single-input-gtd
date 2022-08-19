import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui,QtCore
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel,QKeySequence
from PyQt5.QtWidgets import QMainWindow, QTreeView, QApplication
from PyQt5 import QtWidgets
import pandas as pd
import numpy as np
from function import clockUI

class MainWindow(QMainWindow):
    class DemoTreeView(QWidget):
        class Item(QStandardItem):
            def __init__(self, text,key):
                super().__init__(text)
                self.original_text = text
                self.key=key

            def clone(self) -> 'DemoTreeView.Item':
                return MainWindow.DemoTreeView.Item(self.original_text)

            def say(self):
                print(self.original_text)

            def parent(self):
                if super().parent() is None:
                    return self.model().invisibleRootItem()
                else:
                    return super().parent()
        class View(QTreeView):
            def __init__(self, parent):
                super().__init__(parent)
                self.setSelectionMode(self.ExtendedSelection)
                self.setDragDropMode(self.InternalMove)
                self.clicked.connect(self.on_clicked_handle)


            def on_clicked_handle(self, index):
                item = self.model().itemFromIndex(index)
                item.say()

            def dropEvent(self, event: QtGui.QDropEvent) -> None:
                item_from: "list[DemoTreeView.Item]" = [self.model().itemFromIndex(index) for index in
                                                        self.selectedIndexes()]
                item_to: "DemoTreeView.Item" = self.model().itemFromIndex(self.indexAt(event.pos()))

                parent_from = [item.parent() for item in item_from]
                parent_to = item_to.parent() if item_to is not None else self.model().invisibleRootItem()

                if self.dropIndicatorPosition() == self.OnItem:
                    # for i in item_from:
                    for i in range(len(item_from)):
                        item = parent_from[i].takeRow(item_from[i].row())
                        item_to.appendRow(item)
                elif self.dropIndicatorPosition() == self.OnViewport:
                    for i in range(len(item_from)):
                        item = parent_from[i].takeRow(item_from[i].row())
                        self.model().appendRow(item)
                elif self.dropIndicatorPosition() == self.BelowItem:
                    for i in range(len(item_from)):
                        item = parent_from[i].takeRow(item_from[i].row())
                        parent_to.insertRow(item_to.row() + 1, item)
                elif self.dropIndicatorPosition() == self.AboveItem:
                    for i in range(len(item_from)):
                        item = parent_from[i].takeRow(item_from[i].row())
                        parent_to.insertRow(item_to.row(), item)
                    pass


        def __init__(self, parent=None):
            super().__init__(parent)
            self.initUi()

        def on_model_data_changed_handle(self, index):
            print("emit")
            data=self.model.invisibleRootItem().child(0,0).data(Qt.UserRole)
            print(data)
        def initUi(self):
            self.model = QStandardItemModel(self)
            self.model.setHorizontalHeaderLabels(['test'])
            df = pd.read_csv('data/todo.csv')
            df1 = df[np.isnan(df['father'])]
            df2 = df[np.logical_not(np.isnan(df['father']))]
            alldata = []
            for i in df1.index:
                child =self.Item(df.at[i, 'name'],df.at[i,'name'])
                #child.setText(0, df.at[i, 'name'])
                self.model.appendRow([child])
                alldata.append({'id': df.at[i, 'id'], 'self': child})

            for i in df2.index:
                for j in alldata:
                    if j['id'] == df.at[i, 'father']:
                        child = self.Item(df.at[i, 'name'],df.at[i,'name'])
                        #child.setText(0, df.at[i, 'name'])
                        j['self'].appendRow([child])
                        alldata.append({'id': df.at[i, 'id'], 'self': child})
                        break

            self.model.dataChanged.connect(self.on_model_data_changed_handle)
            self.treeView = self.View(self)

            self.treeView.setModel(self.model)
            self.treeView.selectionModel().selectionChanged.connect(self.on_view_selectionChanged)

            self.treeView.expandAll()



        def on_view_selectionChanged(self, selection: 'QItemSelection'):
            if len(selection.indexes())==0:
                return
            row = selection.indexes()[0].row()
            item = self.model.itemFromIndex(selection.indexes()[0])
            item.say()

    def __init__(self):
        super().__init__()
        self.setCentralWidget(QWidget(self))

        self.Init_UI()
    def Init_UI(self,parent=None):
        Newtree=MainWindow.DemoTreeView(self)
        QShortcut(QKeySequence(" "), self).activated.connect(self.clock)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(40, 30, 511, 31))
        self.lineEdit.setObjectName("lineEdit")
        v_box=QVBoxLayout()
        v_box.addWidget(Newtree.treeView)
        v_box.addWidget(self.lineEdit)
        self.centralWidget().setLayout(v_box)


    def clock(self):
        item = self.model().itemFromIndex(index)
        print(item.original_text)
        clockUI.main(item.original_text)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree =  MainWindow()
    tree.show()
    sys.exit(app.exec_())
