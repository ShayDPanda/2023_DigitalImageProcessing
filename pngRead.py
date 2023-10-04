import numpy
import math
import png as pypng


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

        self.metaData = dict(newImg[3])
        self.pixels = numpy.array(list(newImg[2]))

        self.imgFilePath = filePath

        # Notes to self
        # pixels[0][0-2] = (0,0) (x,y)
        # pixels[0][3-5] = (1,0)
        # pixels[1][0-2] = (0,1)
        # width * 3, height
        # print(len(self.pixels[0]), len(self.pixels))

    def getBitdepth(self):
        return int(self.metaData["bitdepth"])

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

                newImg[y][(x * 3)] = self.pixels[calculatedY][(calculatedX * 3)]
                newImg[y][(x * 3) + 1] = self.pixels[calculatedY][(calculatedX * 3) + 1]
                newImg[y][(x * 3) + 2] = self.pixels[calculatedY][(calculatedX * 3) + 2]

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

                newImg[y][(x * 3)] = self.pixels[calculatedY][(calculatedX * 3)]
                newImg[y][(x * 3) + 1] = self.pixels[calculatedY][(calculatedX * 3) + 1]
                newImg[y][(x * 3) + 2] = self.pixels[calculatedY][(calculatedX * 3) + 2]

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

                newImg[y][(x * 3)] = self.pixels[calculatedY][(calculatedX * 3)]
                newImg[y][(x * 3) + 1] = self.pixels[calculatedY][(calculatedX * 3) + 1]
                newImg[y][(x * 3) + 2] = self.pixels[calculatedY][(calculatedX * 3) + 2]

        self.pixels = newImg

    def scaleUtil(self, newHeight, newWidth):
        # Empty array for new image
        newImg = numpy.zeros((newHeight, newWidth * 3), dtype=numpy.uint8)

        # Scale size for new image
        oldY = int(self.metaData["size"][1])
        oldX = int(self.metaData["size"][0])

        yScale = float(oldY / newHeight)
        xScale = float(oldX / newWidth)

        # Set current metadata size
        self.metaData["size"] = (newWidth, newHeight)

        return newImg, oldY, oldX, yScale, xScale

    def bitMapping(self, newBits):
        if newBits >= int(self.metaData["bitdepth"]):
            print(
                "Bitdepth: No change made; Original:",
                self.metaData["bitdepth"],
                "New:",
                newBits,
            )
            return

        self.metaData["bitdepth"] = newBits

        imgY = int(self.metaData["size"][1])
        imgX = int(self.metaData["size"][0])

        bitChange = self.metaData["bitdepth"] - newBits

        # ONLY WORKS FOR BLACK AND WHITE
        for y in range(imgY):
            for x in range(imgX):
                thisPixel = self.pixels[y][x * 3]
                thisPixel = math.floor(thisPixel / (2**bitChange)) * (2**bitChange)
                self.pixels[y][x * 3] = thisPixel
                self.pixels[y][(x * 3) + 1] = thisPixel
                self.pixels[y][(x * 3) + 2] = thisPixel

    def histoLocal(self, maskSize):

        maskRange =  (maskSize - 1) % 2
        imgY = int(self.metaData["size"][1])
        imgX = int(self.metaData["size"][0])

        for y in range(imgY):
            for x in range(imgX):

                pass

        pass        # TODO

    def histoGlobal(self):
        pass        # TODO

    def printPNG(self):
        try:
            self.imgFilePath = self.imgFilePath.replace(".png", "_Modified.png")
            pypng.from_array(self.pixels, "RGB").save(self.imgFilePath)
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
