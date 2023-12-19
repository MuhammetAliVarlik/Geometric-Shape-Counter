import eel
from geometricshapecounter import *
import base64
import numpy as np
import cv2
import logging

logging.basicConfig(filename='web/output_log.txt', filemode='w', level=logging.DEBUG)

eel.init("web")


@eel.expose
def initializeImage(data,eps,thresh,closed,withText,withColor,withLog):
    try:
        image_data = data.split(';base64,')[-1]  # Base64 verisini ayırma
        binary_data = base64.b64decode(image_data)  # Base64 verisini çözme
        np_data = np.frombuffer(binary_data, np.uint8)
        inp = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        gsc = GeometricShapeCounter()
        image,count,log,thresholdImage,grayImage=gsc.drawContours(inp, eps=float(eps),thresh=int(thresh),closed=closed,withText=withText,withColor=withColor,withLog=withLog)
        print(thresholdImage)
        retval, buffer = cv2.imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer.tobytes())
        retvalThresh, bufferThresh = cv2.imencode('.jpg', thresholdImage)
        jpg_as_text_thresh = base64.b64encode(bufferThresh.tobytes())
        retvalGray, buffer_Gray = cv2.imencode('.jpg', grayImage)
        jpg_as_text_gray = base64.b64encode(buffer_Gray.tobytes())
        print(jpg_as_text_thresh)
        logging.info(str(log),exc_info=True)
        return 'data:image/jpeg;base64,' + jpg_as_text.decode('utf-8'), count,'data:image/jpeg;base64,' + jpg_as_text_thresh.decode('utf-8'),'data:image/jpeg;base64,' + jpg_as_text_gray.decode('utf-8')
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)


@eel.expose
def getDefaults(key,property_name):
    gsc=GeometricShapeCounter()
    defaults=gsc.get_defaults()
    # Check if the key exists in the data
    if str(key) in defaults:
        shape = defaults[str(key)]
        for prop, value in shape.items():
            if prop == property_name:
                return value
    return None

@eel.expose
def updateDefaults(key,property_name,point, color, text, fontScale, thickness, fontColor,fillChoice,textChoice):
    gsc=GeometricShapeCounter()
    filePath="defaults.json"
    defaults=gsc.update_json_value(filePath, key, property_name,point, color, text, fontScale, thickness, fontColor,fillChoice,textChoice)
    return "done"

# Start the index.html file
eel.start("index.html")
