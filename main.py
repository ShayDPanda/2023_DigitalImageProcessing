import sys
from pngRead import PNG_Obj
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from MainWindow import Ui_MainWindow

LENADEFAULT = "LenaImages/LenaImage.png"


def errMsg(message):
    print("Error Found:", message)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.origImgObj = PNG_Obj(LENADEFAULT)  # SHOULD START AS USER INPUT
        self.newImgObj = PNG_Obj()

        # Button functions
        self.buttonLena.clicked.connect(self.openLena)
        self.buttonOpen.clicked.connect(self.openImage)
        self.buttonSave.clicked.connect(self.saveImage)
        self.buttonEditNew.clicked.connect(self.editNew)

        self.buttonConfirm.clicked.connect(self.modifyImage)

    # Getters and Setters
    def openLena(self):
        self.origImgObj = PNG_Obj(LENADEFAULT)
        self.openImage()

    def openImage(self):
        newPix = QPixmap(self.origImgObj.imgFilePath)  # SHOULD START AS USER INPUT
        self.origImage.setPixmap(newPix)

    def saveImage(self):
        self.newImgObj.printPNG()

    def editNew(self):
        self.origImgObj.setCopy(self.newImgObj)
        newPix = QPixmap(self.newImage.pixmap())
        self.origImage.setPixmap(newPix)

    # CONFIRM BUTTON
    def modifyImage(self):
        self.newImgObj.setCopy(self.origImgObj)

        # RESIZING
        change = True
        change = self.modifyImage_Resize()

        # VARYING BIT LEVELS
        newBits = self.inputBits.currentIndex()
        if not change and newBits != 0:
            self.newImgObj.bitMapping(newBits)
            change = True

        # HISTOGRAM EQUALIZING
        if not change:
            change = self.modifyImage_HistogramEQ()

        # FILTERING
        if not change:
            change = self.modifyImage_Filter()

        # If there was a change, print
        if change:
            self.newImgObj.printPNG()
            newPix = QPixmap(self.newImgObj.imgFilePath)
            self.newImage.setPixmap(newPix)

        # Print the original
        else:
            newPix = QPixmap(self.origImgObj.imgFilePath)
            self.newImage.setPixmap(newPix)

    def modifyImage_Resize(self):
        # Combo Boxes
        selectedAlgo = self.inputAlgo.currentIndex()

        # Line Edits
        newX = self.input_x.text()
        newY = self.input_y.text()

        if newX == "" or newY == "":
            newX = 0
            newY = 0
        else:
            newX = int(newX)  # Maybe check if it is an int first?
            newY = int(newY)

        if selectedAlgo == 0 and newX == 0 and newY == 0:
            return False

        elif selectedAlgo == 0 and (newX > 0 and newY > 0):
            errMsg("Resize Skipped, No Algorithm Chosen")
            return False

        elif selectedAlgo != 0 and (newX <= 0 or newY <= 0):
            errMsg("Resize Skipped, Invalid Size")
            return False

        elif selectedAlgo == 1:
            self.newImgObj.nearestNeighbor(newY, newX)

        elif selectedAlgo == 2:
            self.newImgObj.linearInterp(newY, newX)

        elif selectedAlgo == 3:
            self.newImgObj.bilinearInterp(newY, newX)

        else:
            errMsg("Resize Skipped, Invalid Algorithm")
            return False

        return True

    def modifyImage_HistogramEQ(self):
        histoAlgo = self.inputHistoEq.currentIndex()

        if histoAlgo == 0:
            return False

        # Local
        elif histoAlgo == 1:
            maskSize = int(input("Mask Size (x^2): "))

            while maskSize % 2 == 0 or maskSize < 0:
                print("\nInvalid Mask Size ( must be odd )")
                maskSize = int(input("Mask Size (x^2): "))

            self.newImgObj.histoLocal(maskSize)

        # Global
        elif histoAlgo == 2:
            self.newImgObj.histoGlobal()

        else:
            errMsg("Histogram Equalize Skipped, Invalid Selection")
            return False

        return True

    def modifyImage_Filter(self):
        # Get from UI
        filterAlgo = self.inputFilter.currentIndex()
        filterSize = self.input_filterSize.text()

        if filterSize == "":
            filterSize = 3
        else:
            filterSize = int(filterSize)

        if filterAlgo <= 0:
            print("Filter skipped, Invalid Filter Size")
            return False

        # Smooth
        elif filterAlgo == 1:
            self.newImgObj.filterSmooth(filterSize)

        # Median
        elif filterAlgo == 2:
            self.newImgObj.filterMedian(filterSize)

        # Sharpening Laplacian
        elif filterAlgo == 3:
            self.newImgObj.filterSharp()

        # High boosting
        elif filterAlgo == 4:
            # Needs A
            pass

        else:
            errMsg("Spatial Filter Skipped, Invalid Selection")
            return False

        return True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
