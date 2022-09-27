from PyQt5.QtWidgets import *




app = QApplication([])
window = QWidget()
window.setMinimumSize(700, 500)
window.setStyleSheet("QFrame#manipulator { background : rgb(220, 220, 220); border: 1px solid black;}")

nodeNames = ["A", "B", "C"]
nodeAngles = {0, 0, 0}
edgeNames = ["x1", "x2", "x3"]
edgeLengths = {30, 30, 30}

mainLayout = QHBoxLayout()
leftLayout = QVBoxLayout()
rightLayout = QHBoxLayout()


anglesFormLayout = QFormLayout()
angleLabelValue = QLabel("Angle")
angleLabelName = QLabel("Name")
anglesFormLayout.addRow(angleLabelName, angleLabelValue)
angleBox1 = QSpinBox()
angleBox1.setValue(20)
angleBox1.setEnabled(False)
angleBox2 = QSpinBox()
angleBox2.setValue(20)
angleBox2.setEnabled(False)
angleBox3 = QSpinBox()
angleBox3.setValue(20)
angleBox3.setEnabled(False)
anglesFormLayout.addRow(nodeNames[0], angleBox1)
anglesFormLayout.addRow(nodeNames[1], angleBox2)
anglesFormLayout.addRow(nodeNames[2], angleBox3)
rightLayout.addLayout(anglesFormLayout)

lengthsFormLayout = QFormLayout()
lengthLabelValue = QLabel("Length")
lengthLabelName = QLabel("Name")

lengthBox1 = QSpinBox()
lengthBox1.setValue(20)
lengthBox1.setEnabled(False)
lengthBox2 = QSpinBox()
lengthBox2.setValue(20)
lengthBox2.setEnabled(False)
lengthBox3 = QSpinBox()
lengthBox3.setValue(20)
lengthBox3.setEnabled(False)
lengthsFormLayout.addRow(lengthLabelName, lengthLabelValue)
lengthsFormLayout.addRow(edgeNames[0], lengthBox1)
lengthsFormLayout.addRow(edgeNames[1], lengthBox2)
lengthsFormLayout.addRow(edgeNames[2], lengthBox3)
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

window.setLayout(mainLayout)
window.show()
app.exec()