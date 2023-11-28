"""
Application to classify shapes
"""
import cv2
import json
from ErrorHandler import ErrorCatcher,CatchException


class GeometricShapeCounter:
    def __init__(self, file):
        __metaclass__ = ErrorCatcher
        self.__count = {"triangle": 0, "rectangle": 0, "pentagon": 0, "hexagon": 0, "circle": 0}
        # turn bgr image to gray
        self.original = self.__imRead(file)
        # get defaults values
        self.defaults = self.__get_defaults()

    @staticmethod

    def __get_defaults():
        f = open('defaults.json')
        defaultValues = json.load(f)
        return defaultValues

    @staticmethod
    def update_json_value(json_file_path, key, name,point,color,text,fontScale,thickness,fontColor):
        new_value = {
            "name": name,
            "point": point,
            "color": color,
            "text": text,
            "fontScale": fontScale,
            "thickness": thickness,
            "fontColor": fontColor
        }
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        if key in data:
            data[key] = new_value
        else:
            print(f"Error: Key '{key}' not found in the JSON file.")

        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        return data

    @staticmethod
    def __imRead(file):
        img = cv2.imread(file)
        return img

    @staticmethod
    def imShow(img, windowName="Trial"):
        cv2.imshow(windowName, img)
        cv2.waitKey(0)

    def __im2Gray(self, img):
        self.__img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return self.__img_gray

    @staticmethod
    def __threshold(img, thresh, maxVal):
        # threshold for getting better results
        ret, threshImg = cv2.threshold(img, thresh, maxVal, cv2.THRESH_BINARY)
        return ret, threshImg

    @staticmethod
    def __hex_to_bgr(hex_color):
        """
        Convert a hexadecimal color code to BGR format.

        Parameters:
        - hex_color (str): Hexadecimal color code (e.g., "#1E90FF").

        Returns:
        - tuple: BGR color representation as a tuple.
        """
        print(tuple(int(hex_color[i:i + 2], 16) for i in (5, 3, 1)))
        return tuple(int(hex_color[i:i + 2], 16) for i in (5, 3, 1))

    @staticmethod
    def __bgr_to_hex(bgr_color):
        """
        Convert a BGR color representation to hexadecimal format.

        Parameters:
        - bgr_color (tuple): BGR color representation as a tuple.

        Returns:
        - str: Hexadecimal color code.
        """
        return "#{:02X}{:02X}{:02X}".format(*bgr_color[::-1])

    def __findContours(self, img, thresh, maxVal):
        _, img = self.__threshold(self.__im2Gray(img), thresh=thresh, maxVal=maxVal)
        # findContours finds the shell of shapes and classifies them hierarchically
        contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def __findHierarchy(self, img, thresh, maxVal):
        _, img = self.__threshold(self.__im2Gray(img), thresh=thresh, maxVal=maxVal)
        # findContours finds the shell of shapes and classifies them hierarchically
        _, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return hierarchy

    def printCount(self):
        return self.__count

    def __countShapes(self, shape):
        self.__count[shape] += 1

    @staticmethod
    def __fillPollyWithText(img, text, approx, x, y, fontScale, thickness, fontColor, color, withText=True,
                            withColor=True):
        if withColor:
            cv2.fillPoly(img, [approx], color)
        if withText:
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, fontScale, fontColor, thickness)

    @staticmethod
    def __drawCircle(img, text, x, y, fontScale, thickness, fontColor, cnt, color, withText=True, withColor=True):
        ((x1, y1), radius) = cv2.minEnclosingCircle(cnt)
        M = cv2.moments(cnt)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 5:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            if withColor:
                cv2.circle(img, (int(x1), int(y1)), int(radius), color, -1)
                cv2.circle(img, (int(center[0]), int(center[1])), int(radius), (255, 0, 0), -1)
        if withText:
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, fontScale, fontColor, thickness)

    def drawContours(self, img, eps=0.031, thresh=170, maxVal=255, closed=True, withText=True, withColor=True,
                     withLog=True):
        contours = self.__findContours(img, thresh=thresh, maxVal=maxVal)
        for cnt in contours:
            epsilon = eps * cv2.arcLength(cnt, closed)
            # use approxPolyDb to simplify poly lines (RDP based)
            approx = cv2.approxPolyDP(cnt, epsilon, closed)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            # classify and paint
            if 6 < len(approx):
                default = self.defaults.get("{}".format(7))
                self.__drawCircle(img, text=default["text"], x=x, y=y, fontScale=default["fontScale"],
                                  thickness=default["thickness"], fontColor=self.__hex_to_bgr(default["fontColor"]),
                                  cnt=cnt, color=self.__hex_to_bgr(default["color"]), withText=withText,
                                  withColor=withColor)
                self.__countShapes(default["name"])
            elif len(approx) > 2:
                default = self.defaults.get("{}".format(len(approx)))
                self.__fillPollyWithText(img=img, text=default["text"], approx=approx, x=x, y=y,
                                         fontScale=default["fontScale"], thickness=default["thickness"],
                                         fontColor=self.__hex_to_bgr(default["fontColor"]),
                                         color=self.__hex_to_bgr(default["color"]), withText=withText,
                                         withColor=withColor)
                self.__countShapes(default["name"])
        if withLog:
            print(self.printCount())
        return img


#fileName = "shapes.png
fileName = "shapes.png"
gsc = GeometricShapeCounter(fileName)
gsc.imShow(gsc.drawContours(gsc.original, withText=False, withColor=True))