from PyQt5.QtWidgets import *

class ManipulatorWindow(QWidget):
        "docs"
        def __init__(self):
            super(ManipulatorWindow, self).__init__()
            self.nodeAngles = [0, 0, 0]
            self.nodeNames = ["A", "B", "C"]
            self.edgeLengths = [30, 30, 30]
            self.edgeNames = ["x1", "x2", "x3"]
            self.setMinimumSize(700, 500)
            self.setStyleSheet("QFrame#manipulator { background : rgb(220, 220, 220); border: 1px solid black;}")
            mainLayout = QHBoxLayout()
            leftLayout = QVBoxLayout()
            rightLayout = QHBoxLayout()
            anglesFormLayout = QFormLayout()
            angleLabelValue = QLabel("Angle")
            angleLabelName = QLabel("Name")
            anglesFormLayout.addRow(angleLabelName, angleLabelValue)
            self.angleBoxes = [QSpinBox(), QSpinBox(), QSpinBox()]
            self.angleLabels = [QLabel(self.nodeNames[0]), QLabel(self.nodeNames[1]), QLabel(self.nodeNames[2])]
            anglesFormLayout.addRow(self.angleLabels[0], self.angleBoxes[0])
            anglesFormLayout.addRow(self.angleLabels[1], self.angleBoxes[1])
            anglesFormLayout.addRow(self.angleLabels[2], self.angleBoxes[2])
            rightLayout.addLayout(anglesFormLayout)
            self.lengthBoxes = [QSpinBox(), QSpinBox(), QSpinBox()]
            for ind in range(3):
                self.angleBoxes[ind].setEnabled(False)
                self.lengthBoxes[ind].setEnabled(False)
            lengthsFormLayout = QFormLayout()
            lengthLabelValue = QLabel("Length")
            lengthLabelName = QLabel("Name")
            self.lengthLabels = [QLabel(self.edgeNames[0]), QLabel(self.edgeNames[1]), QLabel(self.edgeNames[2])]
            lengthsFormLayout.addRow(lengthLabelName, lengthLabelValue)
            lengthsFormLayout.addRow(self.lengthLabels[0], self.lengthBoxes[0])
            lengthsFormLayout.addRow(self.lengthLabels[1], self.lengthBoxes[1])
            lengthsFormLayout.addRow(self.lengthLabels[2], self.lengthBoxes[2])
            rightLayout.addLayout(lengthsFormLayout)
            manipulatorFrame = QFrame()
            manipulatorFrame.setObjectName("manipulator")
            leftLayout.addWidget(manipulatorFrame, 1)
            logLabel = QTextBrowser()
            logLabel.setText("Logs")
            logLabel.setEnabled(False)
            logLabel.setMaximumHeight(50)
            leftLayout.addWidget(logLabel)
            mainLayout.addLayout(leftLayout, 10)
            mainLayout.addLayout(rightLayout, 3)
            self.setLayout(mainLayout)
            return

        def updateManipulatorData(self):
            for ind in range(3):
                self.angleBoxes[ind].setValue(self.edgeLengths[ind])
                self.lengthBoxes[ind].setValue(self.edgeLengths[ind])
                self.angleLabels[ind].setText(self.nodeNames[ind])
                self.lengthLabels[ind].setText(self.edgeNames[ind])
            return



app = QApplication([])
window = ManipulatorWindow()

window.show()
app.exec()