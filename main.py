from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
import math

def get_intersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1
    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    # non intersecting
    if d > r0 + r1:
        return [False, [0, 0], [0, 0]]
    # One circle within other
    if d < abs(r0 - r1):
        return [False, [0, 0], [0, 0]]
    # coincident circles
    if d == 0 and r0 == r1:
        return [False, [0, 0], [0, 0]]
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(r0 ** 2 - a ** 2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d
        return [True, [x3, y3], [x4, y4]]

def manipulatorNodesPositionFromPositionAndLengths(X, l):
    if (math.sqrt(X[0] * X[0] + X[1] * X[1]) > (l[0] + l[1] + l[2])):
        return []
    angles = [0, 0, 0]
    angles[0] = math.degrees(math.acos(X[0] / (3 * l[0])))
    pA = [l[0] * math.cos(math.radians(angles[0])), l[0] * math.sin(math.radians(angles[0]))]
    isFound, pB1, pB2 = get_intersections(pA[0], pA[1], l[1], X[0], X[1], l[2])
    if (isFound == False):
        return []
    pB = [0.0, 0.0]
    if (pB1[1] * pA[1] == 0):
        pB = pB1
    else:
        pB = pB2
    if (pB[0] - pA[0] != 0):
        angles[1] = math.degrees(math.atan2((pB[1] - pA[1]), (pB[0] - pA[0])))
    else:
        angles[1] = 90
    if (X[0] - pB[0]):
        angles[2] = math.degrees(math.atan2((X[1] - pB[1]), (X[0] - pB[0])))
    else:
        angles[2] = 90
    return [angles[0], angles[1] - angles[0], angles[2] - angles[1]]

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

class ManipulatorWindow(QWidget):
        "docs"
        def __init__(self):
            self.flagMoveIn = False
            self.logs = "Logs"
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
            self.setButtonAngles = QPushButton("Set")
            self.setButtonAngles.setMaximumWidth(50)
            anglesFormLayout.addRow(angleLabelName, angleLabelValue)
            self.angleBoxes = [QDoubleSpinBox(), QDoubleSpinBox(), QDoubleSpinBox()]
            self.angleLabels = [QLabel(self.nodeNames[0]), QLabel(self.nodeNames[1]), QLabel(self.nodeNames[2])]
            anglesFormLayout.addRow(self.angleLabels[0], self.angleBoxes[0])
            anglesFormLayout.addRow(self.angleLabels[1], self.angleBoxes[1])
            anglesFormLayout.addRow(self.angleLabels[2], self.angleBoxes[2])
            anglesFormLayout.addRow("", self.setButtonAngles)
            rightLayout.addLayout(anglesFormLayout)
            self.lengthBoxes = [QSpinBox(), QSpinBox(), QSpinBox()]
            lengthsFormLayout = QFormLayout()
            lengthLabelValue = QLabel("Length")
            lengthLabelName = QLabel("Name")
            self.setButtonLengths = QPushButton("Set")
            self.setButtonLengths.setMaximumWidth(50)
            self.lengthLabels = [QLabel(self.edgeNames[0]), QLabel(self.edgeNames[1]), QLabel(self.edgeNames[2])]
            lengthsFormLayout.addRow(lengthLabelName, lengthLabelValue)
            lengthsFormLayout.addRow(self.lengthLabels[0], self.lengthBoxes[0])
            lengthsFormLayout.addRow(self.lengthLabels[1], self.lengthBoxes[1])
            lengthsFormLayout.addRow(self.lengthLabels[2], self.lengthBoxes[2])
            lengthsFormLayout.addRow("", self.setButtonLengths)
            rightLayout.addLayout(lengthsFormLayout)
            self.manipulatorFrame = ManipulatorRender(self.edgeLengths, self.nodeAngles)
            self.manipulatorFrame.setObjectName("manipulator")
            self.manipulatorFrame.installEventFilter(self)
            leftLayout.addWidget(self.manipulatorFrame, 1)
            self.logLabel = QTextBrowser()
            self.logLabel.setText("Logs")
            self.logLabel.setMaximumHeight(50)
            self.logLabel.installEventFilter(self)
            leftLayout.addWidget(self.logLabel)
            mainLayout.addLayout(leftLayout, 10)
            mainLayout.addLayout(rightLayout, 3)
            self.setLayout(mainLayout)
            for ind in range(3):
                self.angleBoxes[ind].setRange(-180, 180)
                self.lengthBoxes[ind].setRange(10, 300)
            self.updateManipulatorData()
            self.setButtonAngles.clicked.connect(self.setAnglesFromForm)
            self.setButtonLengths.clicked.connect(self.setLengthsFromForm)
            self.logLabel.textChanged.connect(self.endOfLogs)

        def setManipulator(self, pos):
            self.manipulatorFrame.cursorPosition = [pos.x(), pos.y()]
            startCoordinates = self.manipulatorFrame.startCoordinates
            manipCursorPos = [pos.x() - startCoordinates[0],
                              self.manipulatorFrame.height() - (pos.y() + startCoordinates[1])]
            ang = (manipulatorNodesPositionFromPositionAndLengths(manipCursorPos, self.edgeLengths))
            if (len(ang) != 0):
                self.nodeAngles = ang
                self.manipulatorFrame.setAngles(ang)
                self.updateManipulatorData()
                self.logs = self.logs + '\n' + "set angles: " + str(ang[0]) + ' ' + str(
                    ang[1]) + ' ' + str(ang[2])
            else:
                self.logs = self.logs + '\n' + "cursor is out of manipulator zone"

        def eventFilter(self, obj, e) -> bool:
            if obj == self.manipulatorFrame:
                if e.type() == QEvent.MouseButtonPress:
                    self.setManipulator(e.pos())
                    self.flagMoveIn = True
                    return True

                if e.type() == QEvent.MouseButtonRelease:
                    self.flagMoveIn = False
                    return True

                if self.flagMoveIn == True and e.type() == QEvent.MouseMove:
                    self.setManipulator(e.pos())
                    return True

            if obj == self.logLabel and e.type() == QEvent.MouseButtonDblClick:
                self.logLabel.setText(self.logs)
                return True
            return False

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
            str1 = self.logs + '\n' + "angles: "
            for ind in range(3):
                str1 += str(self.nodeAngles[ind]) + ' '
            str1 += "lengths: "
            for ind in range(3):
                str1 += str(self.edgeLengths[ind]) + ' '
            self.logs = str1

        def setAnglesFromForm(self):
            for ind in range(3):
                self.nodeAngles[ind] = self.angleBoxes[ind].value()
            self.manipulatorFrame.setAngles(self.nodeAngles)
            str1 = self.logs + '\n' + "angles: "
            for ind in range(3):
                str1 += str(self.nodeAngles[ind]) + ' '
            self.logs = str1

        def setLengthsFromForm(self):
            for ind in range(3):
                self.edgeLengths[ind] = self.lengthBoxes[ind].value()
            self.manipulatorFrame.setLengths(self.edgeLengths)
            str1 = self.logs + '\n' + "lengths: "
            for ind in range(3):
                str1 += str(self.edgeLengths[ind]) + ' '
            self.logs = str1

        def endOfLogs(self):
            self.logLabel.moveCursor(QTextCursor.End)


app = QApplication([])
window = ManipulatorWindow()
window.show()
app.exec()