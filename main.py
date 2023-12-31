import eel
from geometricshapecounter import *
import base64
import numpy as np
import cv2
import logging
open('output_log.txt', 'w').close()
logging.basicConfig(filename='web/output_log.txt', filemode='w', level=logging.DEBUG)
eel.init("web")


@eel.expose
def initializeImage(data, eps, thresh, closed, withText, withColor, withLog):
    """
    Process input image data to identify geometric shapes and return processed images and count data.

    :param data: Base64-encoded image data
    :param eps: Approximation accuracy for contours
    :param thresh: Threshold value for contour identification
    :param closed: Flag for closed contours
    :param withText: Flag to include text in the image
    :param withColor: Flag to include color in the image
    :param withLog: Flag to log count information
    :return: Processed image, count of shapes, thresholded image, grayscale image as base64 strings
    """
    try:
        # Decode base64 image data and convert to OpenCV format
        image_data = data.split(';base64,')[-1]
        binary_data = base64.b64decode(image_data)
        np_data = np.frombuffer(binary_data, np.uint8)
        inp = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

        # Initialize GeometricShapeCounter
        gsc = GeometricShapeCounter()

        # Process the input image to detect shapes and generate outputs
        image, count, log, thresholdImage, grayImage = gsc.drawContours(
            inp,
            eps=float(eps),
            thresh=int(thresh),
            closed=closed,
            withText=withText,
            withColor=withColor,
            withLog=withLog
        )

        # Encode processed images back into base64
        retval, buffer = cv2.imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer.tobytes())

        retvalThresh, bufferThresh = cv2.imencode('.jpg', thresholdImage)
        jpg_as_text_thresh = base64.b64encode(bufferThresh.tobytes())

        retvalGray, buffer_Gray = cv2.imencode('.jpg', grayImage)
        jpg_as_text_gray = base64.b64encode(buffer_Gray.tobytes())

        # Log information and return processed images and count data as base64 strings
        logging.info(str(log), exc_info=True)

        return (
            'data:image/jpeg;base64,' + jpg_as_text.decode('utf-8'),  # Processed image
            count,  # Count of shapes
            'data:image/jpeg;base64,' + jpg_as_text_thresh.decode('utf-8'),  # Thresholded image
            'data:image/jpeg;base64,' + jpg_as_text_gray.decode('utf-8')  # Grayscale image
        )
    except Exception as e:
        # Error handling and logging for exceptions
        logging.error("Exception occurred", exc_info=True)
        return "error"




@eel.expose
def getDefaults(key, property_name):
    """
    Get default properties of a geometric shape.

    :param key: Key representing the shape
    :param property_name: Name of the property to retrieve
    :return: Value of the specified property for the given shape key or None if not found
    """
    try:
        gsc = GeometricShapeCounter()
        defaults = gsc.get_defaults()

        # Check if the key exists in the default data
        if str(key) in defaults:
            shape = defaults[str(key)]
            for prop, value in shape.items():
                # Find the specified property for the shape
                if prop == property_name:
                    return value
        return None  # Return None if property or key is not found
    except Exception as e:
        # Error handling and logging for exceptions
        logging.error("Exception occurred", exc_info=True)
        return "error"  # Return "error" in case of exceptions


@eel.expose
def updateDefaults(key, property_name, point, color, text, fontScale, thickness, fontColor, fillChoice, textChoice):
    """
    Update default properties of a geometric shape.

    :param key: Key representing the shape
    :param property_name: Name of the property to update
    :param point: Point related to the property
    :param color: Color related to the property
    :param text: Text related to the property
    :param fontScale: Font scale related to the property
    :param thickness: Thickness related to the property
    :param fontColor: Font color related to the property
    :param fillChoice: Fill choice related to the property
    :param textChoice: Text choice related to the property
    :return: "done" if the update is successful, otherwise "error"
    """
    try:
        gsc = GeometricShapeCounter()
        filePath = "defaults.json"

        # Update the JSON file with new property values for the specified shape key
        defaults = gsc.update_json_value(
            filePath, key, property_name, point, color, text, fontScale, thickness, fontColor, fillChoice, textChoice
        )

        return "done"  # Return "done" if the update is successful
    except Exception as e:
        # Error handling and logging for exceptions
        logging.error("Exception occurred", exc_info=True)
        return "error"  # Return "error" in case of exceptions


# Start the index.html file
eel.start("index.html")
