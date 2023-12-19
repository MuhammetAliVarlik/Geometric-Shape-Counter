"""
Application to classify shapes
"""
import cv2
import json


class GeometricShapeCounter:
    def __init__(self):
        """
        :param file(str): file name of input file
        """
        # temp variable to keep number of shapes
        self.__count = {"triangle": 0, "rectangle": 0, "pentagon": 0, "hexagon": 0, "circle": 0}
        # get defaults values
        self.defaults = self.get_defaults()

    @staticmethod
    def get_defaults():
        """
        Get defaults.json file (it keeps settings of the GeometricShapeCounter class)

        :return: defaultValues: default settings (json array)

        """
        # open defaults.json
        f = open('defaults.json')
        defaultValues = json.load(f)
        # return defaultValues ==> Settings of the class
        return defaultValues

    @staticmethod
    def update_json_value(json_file_path, key, name, point, color, text, fontScale, thickness, fontColor,fillChoice,textChoice):
        """
        Function to update settings of app (defaults.json)

        :param json_file_path: path of the json settings file
        :param key: the key we're looking for
        :param name: name parameter in the json file (ex. triangle)
        :param point: point parameter in the json file (ex. 3)
        :param color: color parameter in the json file in HEX format (fill color) (ex. "#C80001")
        :param text: text parameter in the json file (the text which appears in the app) (ex. Triangle)
        :param fontScale: fontScale parameter in the json file (range [0-1]) (ex. 0.5)
        :param thickness: thickness parameter in the json file (ex. 1)
        :param fontColor: fontColor parameter in the json file in HEX format (ex. "#FFFFFF")
        :return: data: updated json file

        """
        # new values from user
        new_value = {
            "name": name,
            "point": point,
            "color": color,
            "text": text,
            "fontScale": fontScale,
            "thickness": thickness,
            "fontColor": fontColor,
            "fillChoice": fillChoice,
            "textChoice": textChoice
        }
        # read the JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # update JSON array data
        if key in data:
            data[key] = new_value
        else:
            print(f"Error: Key '{key}' not found in the JSON file.")

        # write updated JSON data to file
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        return data

    @staticmethod
    def imRead(file):
        """
        :param file:
        :return:
        """
        img = cv2.imread(file)
        return img

    @staticmethod
    def imShow(img, windowName="Trial"):
        """

        :param img:
        :param windowName:
        :return:
        """
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
        grayImg=self.__im2Gray(img)
        _, img = self.__threshold(grayImg, thresh=thresh, maxVal=maxVal)
        # findContours finds the shell of shapes and classifies them hierarchically
        contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours,img,grayImg

    def __findHierarchy(self, img, thresh, maxVal):
        _, img = self.__threshold(self.__im2Gray(img), thresh=thresh, maxVal=maxVal)
        # findContours finds the shell of shapes and classifies them hierarchically
        _, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return hierarchy

    def printCount(self,withLog):
        if withLog:
            return self.__count

    def __countShapes(self, shape):
        self.__count[shape] += 1

    @staticmethod
    def __fillPolyWithText(img, text, approx, x, y, fontScale, thickness, fontColor, color,fillChoice,textChoice, withText=True,
                           withColor=True):
        m = cv2.moments(approx)
        cx = int(m["m10"] / m["m00"])
        cy = int(m["m01"] / m["m00"])

        if withColor:
            if bool(fillChoice):
                cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
                cv2.fillPoly(img, [approx], color)
                cv2.circle(img, (cx, cy), 1, (0, 0, 255), 3)
        if withText:
            if bool(textChoice):
                cv2.putText(img, "AL:"+str(round(cv2.arcLength(approx, True),2)), (x, y+15), cv2.FONT_HERSHEY_SIMPLEX, fontScale, fontColor, thickness)
                cv2.putText(img, "A:" + str(round(cv2.contourArea(approx),2)), (x, y + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, fontScale, fontColor, thickness)
                cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, fontScale, fontColor, thickness)

    @staticmethod
    def __drawCircle(img, text, x, y, fontScale, thickness, fontColor, cnt, color,fillChoice,textChoice,withText=True, withColor=True):
        ((x1, y1), radius) = cv2.minEnclosingCircle(cnt)
        M = cv2.moments(cnt)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 5:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            if withColor:
                if bool(fillChoice):
                    cv2.circle(img, (int(center[0]), int(center[1])), int(radius), color, -1)
                    cv2.circle(img, (int(center[0]), int(center[1])), 3, (0, 0, 255), -1)
        if withText:
            if bool(textChoice):
                cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, fontScale, fontColor, thickness)

    def drawContours(self, img, eps=0.031, thresh=170, maxVal=255, closed=True, withText=True, withColor=True,
                     withLog=True):

        contours,thresholdImage,grayImage = self.__findContours(img, thresh=thresh, maxVal=maxVal)
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
                                  cnt=cnt, color=self.__hex_to_bgr(default["color"]),fillChoice=default["fillChoice"],textChoice=default["textChoice"],withText=withText,
                                  withColor=withColor)
                self.__countShapes(default["name"])
            elif len(approx) > 2:
                default = self.defaults.get("{}".format(len(approx)))
                self.__fillPolyWithText(img=img, text=default["text"], approx=approx, x=x, y=y,
                                        fontScale=default["fontScale"], thickness=default["thickness"],
                                        fontColor=self.__hex_to_bgr(default["fontColor"]),
                                        color=self.__hex_to_bgr(default["color"]),fillChoice=default["fillChoice"],textChoice=default["textChoice"],withText=withText,
                                        withColor=withColor)
                self.__countShapes(default["name"])
        if withLog:
            print(self.printCount(withLog=withLog))
        return img, self.__count,self.printCount(withLog=withLog),thresholdImage,grayImage


"""fileName = "shapes.png"
# fileName = ""
gsc = GeometricShapeCounter(fileName)

gsc.imShow(gsc.drawContours(gsc.original, withText=False, withColor=True))"""
