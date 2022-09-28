from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import math

class ManipulatorRender(QFrame):
    "docs"
    def __init__(self, initialEdgeLengths, initialAngles):
        super().__init__()
        self.edgeLengths = initialEdgeLengths
        self.angles = initialAngles
        self.startCoordinates = [150, 50]
        self.nodeRadius = 30
        self.nodeColor = QColor(233, 218, 16)
        self.edgeColor = QColor(40, 40, 40)
        self.edgeWidth = 9
        self.boxLineWidth = 5
        self.boxEdgeLength = 40
        self.boxPenColor = QColor(0, 0, 0)
        self.boxBrushColor = QColor(83, 47, 0)
        self.cursorColor = QColor(255, 0, 0)
        self.cursorRadius = 5
        self.cursorPosition = [-1, -1]

    def paintEvent(self, e):
        super().paintEvent(e)
        brush = QBrush(QColor(100, 200, 100))
        painter = QPainter(self)
        painter.setBrush(brush)
        painter.drawRect(0, self.height() - 49, self.width() - 1, 48)
        nodePen = QPen(QColor(0, 0, 0))
        nodeBrush = QBrush(self.nodeColor)
        edgePen = QPen(self.edgeColor)
        edgePen.setWidth(self.edgeWidth)
        lastPosition = self.startCoordinates
        currentAngle = 0
        for t in range(3):
            currentAngle = currentAngle + self.angles[t]
            currentPosition = [lastPosition[0] + self.edgeLengths[t] * math.cos(math.radians(currentAngle)),
                               lastPosition[1] + self.edgeLengths[t] * math.sin(math.radians(currentAngle))]
            painter.setPen(edgePen)
            painter.drawLine(lastPosition[0], self.height() - lastPosition[1], currentPosition[0],  self.height() - currentPosition[1])
            painter.setBrush(nodeBrush)
            painter.setPen(nodePen)
            painter.drawEllipse(lastPosition[0] - self.nodeRadius / 2, self.height() - lastPosition[1] - self.nodeRadius / 2 + 1, self.nodeRadius, self.nodeRadius)
            lastPosition = currentPosition
            if t == 2:
                l = lastPosition[0] - self.boxEdgeLength / 2
                r = lastPosition[0] + self.boxEdgeLength / 2
                t = lastPosition[1] + self.boxEdgeLength / 2
                b = lastPosition[1] - self.boxEdgeLength / 2
                boxPen = QPen(self.boxPenColor)
                boxPen.setWidth(self.boxLineWidth)
                boxBrush = QBrush(self.boxBrushColor)
                painter.setPen(boxPen)
                painter.setBrush(boxBrush)
                painter.drawRect(l, self.height() - t, self.boxEdgeLength, self.boxEdgeLength)
                painter.drawLine(l + self.boxLineWidth / 2, self.height() - t + self.boxLineWidth / 2, r - self.boxLineWidth / 2, self.height() - b - self.boxLineWidth / 2)
                painter.drawLine(r - self.boxLineWidth / 2, self.height() - t + self.boxLineWidth / 2, l + self.boxLineWidth / 2, self.height() - b - self.boxLineWidth / 2)

            cursorPen = QPen(QColor(0, 0, 0))
            cursorPen.setWidth(1)
            cursorBrush = QBrush(self.cursorColor)
            painter.setBrush(cursorBrush)
            painter.setPen(cursorPen)
            painter.drawEllipse(self.cursorPosition[0] - self.cursorRadius / 2, self.cursorPosition[1] - self.cursorRadius / 2, self.cursorRadius, self.cursorRadius)

    def setAngles(self, angles):
        self.angles = angles
        self.update()

    def setLengths(self, lengths):
        self.edgeLengths = lengths
        self.update()

    def mousePressEvent(self, e):
        self.cursorPosition[0] = e.pos().x()
        self.cursorPosition[1] = e.pos().y()
        self.update()
        print(e.pos())
        super().mousePressEvent(e) #better use eventFilter than that

class ManipulatorWindow(QWidget):
        "docs"
        def __init__(self):
            super(ManipulatorWindow, self).__init__()
            self.nodeAngles = [60, -30, -45]
            self.nodeNames = ["A", "B", "C"]
            self.edgeLengths = [100, 100, 100]
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
            self.angleBoxes = [QDoubleSpinBox(), QDoubleSpinBox(), QDoubleSpinBox()]
            self.angleLabels = [QLabel(self.nodeNames[0]), QLabel(self.nodeNames[1]), QLabel(self.nodeNames[2])]
            anglesFormLayout.addRow(self.angleLabels[0], self.angleBoxes[0])
            anglesFormLayout.addRow(self.angleLabels[1], self.angleBoxes[1])
            anglesFormLayout.addRow(self.angleLabels[2], self.angleBoxes[2])
            rightLayout.addLayout(anglesFormLayout)
            self.lengthBoxes = [QSpinBox(), QSpinBox(), QSpinBox()]
            lengthsFormLayout = QFormLayout()
            lengthLabelValue = QLabel("Length")
            lengthLabelName = QLabel("Name")
            self.lengthLabels = [QLabel(self.edgeNames[0]), QLabel(self.edgeNames[1]), QLabel(self.edgeNames[2])]
            lengthsFormLayout.addRow(lengthLabelName, lengthLabelValue)
            lengthsFormLayout.addRow(self.lengthLabels[0], self.lengthBoxes[0])
            lengthsFormLayout.addRow(self.lengthLabels[1], self.lengthBoxes[1])
            lengthsFormLayout.addRow(self.lengthLabels[2], self.lengthBoxes[2])
            rightLayout.addLayout(lengthsFormLayout)
            self.manipulatorFrame = ManipulatorRender(self.edgeLengths, self.nodeAngles)
            self.manipulatorFrame.setObjectName("manipulator")
            leftLayout.addWidget(self.manipulatorFrame, 1)
            self.logLabel = QTextBrowser()
            self.logLabel.setText("Logs")
            self.logLabel.setMaximumHeight(50)
            leftLayout.addWidget(self.logLabel)
            mainLayout.addLayout(leftLayout, 10)
            mainLayout.addLayout(rightLayout, 3)
            self.setLayout(mainLayout)
            for ind in range(3):
                self.angleBoxes[ind].setRange(-180, 180)
                self.lengthBoxes[ind].setRange(10, 300)
            self.updateManipulatorData()

            for ind in range(3):
                self.angleBoxes[ind].valueChanged.connect(self.readManipulatorData)
                self.lengthBoxes[ind].valueChanged.connect(self.readManipulatorData)

        def mousePressEvent(self, e):
            pass


        def updateManipulatorData(self):
            for ind in range(3):
                self.angleBoxes[ind].setValue(self.nodeAngles[ind])
                self.lengthBoxes[ind].setValue(self.edgeLengths[ind])
                self.angleLabels[ind].setText(self.nodeNames[ind])
                self.lengthLabels[ind].setText(self.edgeNames[ind])

        def readManipulatorData(self):
            for ind in range(3):
                self.nodeAngles[ind] = self.angleBoxes[ind].value()
                self.edgeLengths[ind] = self.lengthBoxes[ind].value()
            self.manipulatorFrame.setAngles(self.nodeAngles)
            self.manipulatorFrame.setLengths(self.edgeLengths)
            str1 = self.logLabel.toPlainText() + '\n' + "angles: "
            for ind in range(3):
                str1 += str(self.nodeAngles[ind]) + ' '
            str1 += "lengths: "
            for ind in range(3):
                str1 += str(self.edgeLengths[ind]) + ' '

            self.logLabel.setText(str1)



app = QApplication([])
window = ManipulatorWindow()
window.show()
app.exec()