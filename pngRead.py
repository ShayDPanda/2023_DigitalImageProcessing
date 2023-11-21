import numpy
import math
import png as pypng
import time


def checkXRange(currentX, additionalX, maxX):
    if currentX + additionalX < 0:
        return 0

    # Top of image
    elif currentX + additionalX >= maxX:
        return maxX - 1

    else:
        return currentX + additionalX


def checkYRange(currentY, additionalY, maxY):
    if currentY + additionalY < 0:
        return 0

    # Top of image
    elif currentY + additionalY >= maxY:
        return maxY - 1

    else:
        return currentY + additionalY


class PNG_Obj:
    def __init__(self, newFile=""):
        #
        self.pixels = numpy.empty([0])

        # Dict: greyscale, alpha, planes, bitdepth, interlace, size, gamma, palette, colormap
        self.metaData = numpy.empty([0])
        self.imgFilePath = newFile

        if self.imgFilePath != "":
            self.load_image(self.imgFilePath)

    def setCopy(self, oldObj):
        # Copy Data
        self.load_image(oldObj.imgFilePath)

    def load_image(self, filePath: str):
        # Set file path

        # Set image data
        try:
            newImg = pypng.Reader(filePath).asDirect()
        except:
            print("Image not found")
            return

        self.imgFilePath = filePath
        self.metaData = dict(newImg[3])
        self.pixels = numpy.array(list(newImg[2]))

        if self.metaData["bitdepth"] == 8 and len(self.pixels[0]) > int(
            self.metaData["size"][0]
        ):
            self.resize8Bit()

        # Notes to self
        # pixels[0][0-2] = (0,0) (x,y)
        # pixels[0][3-5] = (1,0)
        # pixels[1][0-2] = (0,1)
        # width will be x3 for RGB

        # width, height
        # print(len(self.pixels[0]), len(self.pixels))

    def resize8Bit(self):
        imgY, imgX = self.getImgSize()
        newImg = numpy.zeros((imgY, imgX), dtype=numpy.uint8)

        for y in range(imgY):
            for x in range(imgX):
                newImg[y][x] = self.pixels[y][x * 3]

        self.pixels = newImg

    def getBitdepth(self):
        return int(self.metaData["bitdepth"])

    def getImgSize(self):
        y = int(self.metaData["size"][1])
        x = int(self.metaData["size"][0])

        return y, x

    def scaleUtil(self, newHeight, newWidth):
        # Empty array for new image
        newImg = numpy.zeros((newHeight, newWidth), dtype=numpy.uint8)

        # Scale size for new image
        oldY, oldX = self.getImgSize()

        yScale = float(oldY / newHeight)
        xScale = float(oldX / newWidth)

        # Set current metadata size
        self.metaData["size"] = (newWidth, newHeight)

        return newImg, oldY, oldX, yScale, xScale

    def nearestNeighbor(self, newHeight, newWidth):
        newImg, oldY, oldX, yScale, xScale = self.scaleUtil(newHeight, newWidth)

        for y in range(newHeight):
            for x in range(newWidth):
                calculatedX = round(x * xScale)
                calculatedY = round(y * yScale)

                # -1, because index numbers
                if calculatedX >= oldX:
                    calculatedX = oldX - 1

                if calculatedY >= oldY:
                    calculatedY = oldY - 1

                newImg[y][x] = self.pixels[calculatedY][calculatedX]

        self.pixels = newImg

    def linearInterp(self, newHeight, newWidth):
        newImg, oldY, oldX, yScale, xScale = self.scaleUtil(newHeight, newWidth)

        for y in range(newHeight):
            for x in range(newWidth):
                # Using X for the interpolation

                calculatedX = float(int(x)) * xScale
                leftX = math.floor(calculatedX)
                rightX = math.ceil(calculatedX)

                if abs(leftX - calculatedX) < abs(rightX - calculatedX):
                    calculatedX = leftX
                else:
                    calculatedX = rightX

                calculatedY = round(y * yScale)
                # -1, because index numbers
                if calculatedX >= oldX:
                    calculatedX = oldX - 1

                if calculatedY >= oldY:
                    calculatedY = oldY - 1

                newImg[y][x] = self.pixels[calculatedY][calculatedX]

        self.pixels = newImg

    def bilinearInterp(self, newHeight, newWidth):
        newImg, oldY, oldX, yScale, xScale = self.scaleUtil(newHeight, newWidth)

        for y in range(newHeight):
            for x in range(newWidth):
                calculatedX = float(int(x)) * xScale
                leftX = math.floor(calculatedX)
                rightX = math.ceil(calculatedX)

                if abs(leftX - calculatedX) < abs(rightX - calculatedX):
                    calculatedX = leftX
                else:
                    calculatedX = rightX

                calculatedY = float(int(y)) * yScale
                upY = math.floor(calculatedY)
                downY = math.ceil(calculatedY)

                if abs(upY - calculatedY) < abs(downY - calculatedY):
                    calculatedY = upY
                else:
                    calculatedY = downY

                # -1, because index numbers
                if calculatedX >= oldX:
                    calculatedX = oldX - 1

                if calculatedY >= oldY:
                    calculatedY = oldY - 1

                newImg[y][x] = self.pixels[calculatedY][calculatedX]

        self.pixels = newImg

    def bitMapping(self, newBits):
        if newBits >= int(self.metaData["bitdepth"]):
            print(
                "Bitdepth: No change made; Original:",
                self.metaData["bitdepth"],
                "New:",
                newBits,
            )
            return

        imgY, imgX = self.getImgSize()

        # bitChange = self.metaData["bitdepth"] - newBits
        bitChange = self.metaData["bitdepth"] - newBits  # Assumes 8 bit image for class

        # ONLY WORKS FOR BLACK AND WHITE
        for y in range(imgY):
            for x in range(imgX):
                self.pixels[y][x] = math.floor(self.pixels[y][x] / (2**bitChange)) * (
                    2**bitChange
                )

        self.metaData["bitdepth"] = newBits

    def histoLocal(self, maskSize):
        imgY, imgX = self.getImgSize()
        newImg = numpy.zeros((imgY, imgX), dtype=numpy.uint8)

        filterRange = (maskSize - 1) // 2
        filterRange = list(range(-filterRange, filterRange + 1))

        for y in range(imgY):
            for x in range(imgX):
                imgBits = dict()

                for filterY in filterRange:
                    currentY = checkYRange(y, filterY, imgY)

                    for filterX in filterRange:
                        currentX = checkXRange(x, filterX, imgX)

                        imgBits.setdefault(self.pixels[currentY][currentX], 0)
                        imgBits[self.pixels[currentY][currentX]] += 1

                for element in imgBits:
                    imgBits[element] /= maskSize * maskSize

                imgBits = dict(sorted(imgBits.items()))
                imgValues = numpy.zeros(len(imgBits))

                index = 0
                for element in imgBits:
                    if index == 0:
                        imgValues[0] = imgBits[element]
                    else:
                        imgValues[index] += imgValues[index - 1] + imgBits[element]

                    index += 1

                L = (2 ** self.getBitdepth()) - 1
                for thisX in range(len(imgValues)):
                    imgValues[thisX] *= L

                imgValues = numpy.rint(imgValues)
                index = 0
                for element in imgBits:
                    imgBits[element] = imgValues[index]
                    index += 1

                for filterY in filterRange:
                    currentY = checkYRange(y, filterY, imgY)

                    for filterX in filterRange:
                        currentX = checkXRange(x, filterX, imgX)

                        newImg[y][x] = int(imgBits[self.pixels[currentY][currentX]])

        self.pixels = newImg

    def histoGlobal(self):
        imgY, imgX = self.getImgSize()
        newImg = numpy.zeros((imgY, imgX), dtype=numpy.uint8)

        imgBits = dict()

        for y in range(imgY):
            for x in range(imgX):
                imgBits.setdefault(self.pixels[y][x], 0)
                imgBits[self.pixels[y][x]] += 1

        for element in imgBits:
            imgBits[element] /= imgY * imgX

        imgBits = dict(sorted(imgBits.items()))
        imgValues = numpy.zeros(len(imgBits))

        index = 0
        for element in imgBits:
            if index == 0:
                imgValues[0] = imgBits[element]
            else:
                imgValues[index] += imgValues[index - 1] + imgBits[element]

            index += 1

        L = (2 ** self.getBitdepth()) - 1
        for x in range(len(imgValues)):
            imgValues[x] *= L

        imgValues = numpy.rint(imgValues)
        index = 0
        for element in imgBits:
            imgBits[element] = imgValues[index]
            index += 1

        for y in range(imgY):
            for x in range(imgX):
                newImg[y][x] = int(imgBits[self.pixels[y][x]])

        self.pixels = newImg

    def filterSetup(self, filterSize):
        imgY, imgX = self.getImgSize()
        newImg = numpy.zeros((imgY, imgX), dtype=numpy.uint8)

        filterRange = (filterSize - 1) // 2
        filterRange = list(range(-filterRange, filterRange + 1))

        return imgY, imgX, newImg, filterRange

    def filterSmooth(self, filterSize):
        imgY, imgX, newImg, filterRange = self.filterSetup(filterSize)

        for y in range(imgY):
            for x in range(imgX):
                pixelSummation = 0

                for filterY in filterRange:
                    currentY = checkYRange(y, filterY, imgY)

                    for filterX in filterRange:
                        currentX = checkXRange(x, filterX, imgX)

                        pixelSummation += self.pixels[currentY][currentX]

                newImg[y][x] = pixelSummation / (filterSize**2)

        self.pixels = newImg

    def filterMedian(self, filterSize):
        imgY, imgX, newImg, filterRange = self.filterSetup(filterSize)

        for y in range(imgY):
            for x in range(imgX):
                pixelMedian = []

                for filterY in filterRange:
                    currentY = checkYRange(y, filterY, imgY)

                    for filterX in filterRange:
                        currentX = checkXRange(x, filterX, imgX)
                        pixelMedian.append(self.pixels[currentY][currentX])

                newImg[y][x] = int(numpy.median(pixelMedian))

        self.pixels = newImg

    def filterSharp(self):
        imgY, imgX, newImg, filterRange = self.filterSetup(3)

        # Laplacian
        firstFilter = numpy.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
        secondFilter = numpy.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])

        for y in range(imgY):
            for x in range(imgX):
                pixelSummation = 0
                thisRow = 0

                for filterY in filterRange:
                    thisCol = 0

                    currentY = checkYRange(y, filterY, imgY)

                    for filterX in filterRange:
                        currentX = checkXRange(x, filterX, imgX)

                        pixelSummation += (
                            firstFilter[thisRow][thisCol]
                            * self.pixels[currentY][currentX]
                        )

                        thisCol += 1

                    thisRow += 1

                if pixelSummation < 0:
                    newImg[y][x] = 255
                else:
                    newImg[y][x] = 0

                    # TODO
                newImg[y][x] = pixelSummation

        # for y in range(imgY):
        #     for x in range(imgX):
        #         newImg[y][x] = (newImg[y][x] * -1) + self.pixels[y][x]

        self.pixels = newImg

    def filterBoosting(self, A):  # didn't work
        pass

    def filterArithmetic(self, filterSize):
        imgY, imgX, newImg, filterRange = self.filterSetup(filterSize)

        # 1/mn * summation of pixels in neighborhood
        mn = filterSize**2

        for y in range(imgY):
            for x in range(imgX):
                summation = 0

                for filterY in filterRange:
                    currentY = checkYRange(y, filterY, imgY)

                    for filterX in filterRange:
                        currentX = checkXRange(x, filterX, imgX)

                        summation += self.pixels[currentY][currentX]

                newImg[y][x] = int(summation / mn)

        self.pixels = newImg

    def filterGeometric(self, filterSize):
        imgY, imgX, newImg, filterRange = self.filterSetup(filterSize)

        mn = filterSize**2

        for y in range(imgY):
            for x in range(imgX):
                piProduct = float(1)

                for filterY in filterRange:
                    currentY = checkYRange(y, filterY, imgY)

                    for filterX in filterRange:
                        currentX = checkXRange(x, filterX, imgX)
                        piProduct *= self.pixels[currentY][currentX]

                newImg[y][x] = math.floor(piProduct ** (1 / mn))

        self.pixels = newImg

    def filterHarmonic(self, filterSize):
        imgY, imgX, newImg, filterRange = self.filterSetup(filterSize)

        mn = filterSize**2

        for y in range(imgY):
            for x in range(imgX):
                summation = 0

                for filterY in filterRange:
                    currentY = checkYRange(y, filterY, imgY)

                    for filterX in filterRange:
                        currentX = checkXRange(x, filterX, imgX)

                        if self.pixels[currentY][currentX] != 0:
                            summation += 1 / self.pixels[currentY][currentX]

                if summation == 0:
                    newImg[y][x] = 0
                else:
                    newImg[y][x] = int(mn / summation)

        self.pixels = newImg

    def filterContraharmonic(self, filterSize):
        imgY, imgX, newImg, filterRange = self.filterSetup(filterSize)

        Q = 0

        for y in range(imgY):
            for x in range(imgX):
                numer = float(0)
                denom = float(0)

                for filterY in filterRange:
                    currentY = checkYRange(y, filterY, imgY)

                    for filterX in filterRange:
                        currentX = checkXRange(x, filterX, imgX)

                        numer += self.pixels[currentY][currentX] ** (Q + 1)
                        denom += self.pixels[currentY][currentX] ** Q

                newImg[y][x] = math.floor(numer / denom)

        self.pixels = newImg

    def filterMax(self, filterSize):
        imgY, imgX, newImg, filterRange = self.filterSetup(filterSize)

        for y in range(imgY):
            for x in range(imgX):
                currentMax = 0

                for filterY in filterRange:
                    currentY = checkYRange(y, filterY, imgY)

                    for filterX in filterRange:
                        currentX = checkXRange(x, filterX, imgX)

                        if self.pixels[currentY][currentX] > currentMax:
                            currentMax = self.pixels[currentY][currentX]

                newImg[y][x] = currentMax

        self.pixels = newImg

    def filterMin(self, filterSize):
        imgY, imgX, newImg, filterRange = self.filterSetup(filterSize)

        for y in range(imgY):
            for x in range(imgX):
                # 255 because it's the maximum color value
                currentMin = 255

                for filterY in filterRange:
                    currentY = checkYRange(y, filterY, imgY)

                    for filterX in filterRange:
                        currentX = checkXRange(x, filterX, imgX)

                        if self.pixels[currentY][currentX] < currentMin:
                            currentMin = self.pixels[currentY][currentX]

                newImg[y][x] = currentMin

        self.pixels = newImg

    def filterMidpoint(self, filterSize):
        imgY, imgX, newImg, filterRange = self.filterSetup(filterSize)

        for y in range(imgY):
            for x in range(imgX):
                currentMax = 0
                currentMin = 255

                for filterY in filterRange:
                    currentY = checkYRange(y, filterY, imgY)

                    for filterX in filterRange:
                        currentX = checkXRange(x, filterX, imgX)

                        currentValue = self.pixels[currentY][currentX]

                        if currentValue > currentMax:
                            currentMax = currentValue

                        if currentValue < currentMin:
                            currentMin = currentValue

                newImg[y][x] = int((currentMax + currentMin) / 2)

        self.pixels = newImg

    def filterAlphaTrimmed(self, filterSize):
        imgY, imgX, newImg, filterRange = self.filterSetup(filterSize)

        mn = filterSize**2
        alpha = 4
        for y in range(imgY):
            for x in range(imgX):
                items = []

                for filterY in filterRange:
                    currentY = checkYRange(y, filterY, imgY)

                    for filterX in filterRange:
                        currentX = checkXRange(x, filterX, imgX)

                        items.append(self.pixels[currentY][currentX])

                items.sort()

                for d in range(int(alpha / 2)):
                    items.pop(0)
                    items.pop(1)

                summation = 0
                for item in items:
                    summation += item

                newImg[y][x] = summation / (mn - alpha)

        self.pixels = newImg

    def removeBitPlane(self, bitPlane):
        imgY, imgX = self.getImgSize()

        lower = 2 ** (bitPlane - 1)
        upper = 2**bitPlane

        for y in range(imgY):
            for x in range(imgX):
                if lower <= self.pixels[y][x] < upper:
                    self.pixels[y][x] = 0

    def printPNG(self):
        try:
            self.imgFilePath = self.imgFilePath.replace(".png", "_Modified.png")
            pypng.from_array(self.pixels, "L").save(self.imgFilePath)
            print("Saved Image as", self.imgFilePath, "\n")
        except:
            print("FAILED TO PRINT.")
            print(self.pixels)

    # A function to just remind myself of how the input and output should look
    def greenSquare(self, newHeight, newWidth):
        for y in range(newHeight):
            for x in range(newWidth):
                self.pixels[y][(x * 3)] = 0  # R
                self.pixels[y][(x * 3) + 1] = 255  # G
                self.pixels[y][(x * 3) + 2] = 0  # B

                self.pixels[y][x] = 0  # Grey

    def hierarchicalFilling(self, upscale=4):
        imgY, imgX = self.getImgSize()
        newY = imgY * upscale
        newX = imgX * upscale
        newImg, oldY, oldX, yScale, xScale = self.scaleUtil(newY, newX)

        runtime = time.perf_counter()

        for y in range(oldY - 1):
            yOffset = y * 4
            # Left Col
            newImg[yOffset][0] = self.pixels[y][0]  # Upper Left pixel
            newImg[yOffset + 1][0] = self.pixels[y][0]
            newImg[yOffset + 2][0] = self.pixels[y][0]
            newImg[yOffset + 3][0] = self.pixels[y + 1][0]
            newImg[(y + 1) * 4][0] = self.pixels[y + 1][0]  # Lower left pixel

            for x in range(oldX - 1):
                xOffset = x * 4

                # Top of image
                if y == 0:
                    # Pixels between top corners
                    newImg[0][xOffset + 1] = self.pixels[0][x]
                    newImg[0][xOffset + 2] = self.pixels[0][x]
                    newImg[0][xOffset + 3] = self.pixels[0][x + 1]
                    newImg[0][(x + 1) * 4] = self.pixels[0][x + 1]  # Upper right pixel

                # Homogenous Square
                if (
                    self.pixels[y][x]
                    == self.pixels[y][x + 1]
                    == self.pixels[y + 1][x]
                    == self.pixels[y + 1][x + 1]
                ):
                    for countY in range(5):
                        newImg[yOffset + countY][
                            xOffset : (x + 1) * 4 + 1
                        ] = self.pixels[y][x]

                # Not Homogenous
                else:
                    # Lower right corner
                    newImg[(y + 1) * 4][(x + 1) * 4] = self.pixels[y + 1][x]

                    # Middle
                    # x x x x x
                    # x x x x x
                    # x x o x x
                    # x x x x x
                    # x x x x x

                    newImg[yOffset + 2][xOffset + 2] = numpy.sort(
                        [
                            self.pixels[y][x],
                            self.pixels[y][x + 1],
                            self.pixels[y + 1][x],
                            self.pixels[y + 1][x + 1],
                        ]
                    )[2]
                    # NOT MATHEMATICAL MEDIAN

                    # Corners
                    # x x x x x
                    # x o x o x
                    # x x x x x
                    # x o x o x
                    # x x x x x

                    # Upper Left
                    thisY = yOffset + 1
                    thisX = xOffset + 1
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 1][thisX - 1],
                            newImg[thisY + 1][thisX - 1],
                            newImg[thisY - 1][thisX + 1],
                            newImg[thisY + 1][thisX + 1],
                        ]
                    )[2]

                    # Lower Left
                    thisY += 2
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 1][thisX - 1],
                            newImg[thisY + 1][thisX - 1],
                            newImg[thisY - 1][thisX + 1],
                        ]
                    )[1]

                    # Lower Right
                    thisX += 2
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 1][thisX - 1],
                            newImg[thisY + 1][thisX + 1],
                        ]
                    )[0]

                    # Upper Right
                    thisY += -2
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 1][thisX - 1],
                            newImg[thisY + 1][thisX - 1],
                            newImg[thisY - 1][thisX + 1],
                        ]
                    )[1]

                    # Edge
                    # x x x x x
                    # x x x x x
                    # x x x x o
                    # x x x x x
                    # x x o x x

                    # Bottom Edge
                    thisY = yOffset + 4
                    thisX = xOffset + 2
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 2][thisX],
                            newImg[thisY][thisX - 2],
                            newImg[thisY][thisX + 2],
                        ]
                    )[1]

                    # Right Edge
                    thisY = yOffset + 2
                    thisX = xOffset + 4
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 2][thisX],
                            newImg[thisY + 2][thisX],
                            newImg[thisY][thisX - 2],
                        ]
                    )[1]

                    # Fill
                    # x x x x x
                    # x x o x o
                    # x o x o x
                    # x x o x o
                    # x o x o x

                    # First Row
                    thisY = yOffset + 1
                    thisX = xOffset + 2
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 1][thisX],
                            newImg[thisY + 1][thisX],
                            newImg[thisY][thisX - 1],
                            newImg[thisY][thisX + 1],
                        ]
                    )[2]

                    thisX += 2
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 1][thisX],
                            newImg[thisY + 1][thisX],
                            newImg[thisY][thisX - 1],
                        ]
                    )[1]

                    # Second Row
                    thisY += 1
                    thisX = xOffset + 1
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 1][thisX],
                            newImg[thisY + 1][thisX],
                            newImg[thisY][thisX - 1],
                            newImg[thisY][thisX + 1],
                        ]
                    )[2]

                    thisX += 2
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 1][thisX],
                            newImg[thisY + 1][thisX],
                            newImg[thisY][thisX - 1],
                            newImg[thisY][thisX + 1],
                        ]
                    )[2]

                    # Third Row
                    thisY += 1
                    thisX = xOffset + 2
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 1][thisX],
                            newImg[thisY + 1][thisX],
                            newImg[thisY][thisX - 1],
                            newImg[thisY][thisX + 1],
                        ]
                    )[2]

                    thisX += 2
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 1][thisX],
                            newImg[thisY + 1][thisX],
                            newImg[thisY][thisX - 1],
                        ]
                    )[1]

                    # Forth Row
                    thisY += 1
                    thisX = xOffset + 1
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 1][thisX],
                            newImg[thisY][thisX - 1],
                            newImg[thisY][thisX + 1],
                        ]
                    )[1]

                    thisX += 2
                    newImg[thisY][thisX] = numpy.sort(
                        [
                            newImg[thisY - 1][thisX],
                            newImg[thisY][thisX - 1],
                            newImg[thisY][thisX + 1],
                        ]
                    )[1]

        for y in range(newY - 4):
            newImg[y][-4:-1] = newImg[y][-5]

        for x in range(newX):
            newImg[-1][x] = newImg[-5][x]
            newImg[-2][x] = newImg[-5][x]
            newImg[-3][x] = newImg[-5][x]
            newImg[-4][x] = newImg[-5][x]

        runtime = time.perf_counter() - runtime
        print("Hierarchical Filling", runtime)
        self.pixels = newImg

        return runtime
