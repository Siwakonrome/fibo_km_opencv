
import cv2
import os

def display(value):
    pass


def main():
    cv2.namedWindow("Output")
    cv2.createTrackbar("value","Output",128,255,display)
    while True :
        this_location = os.path.dirname(os.path.abspath(__file__))
        gray_img = cv2.imread("{path}/image/nectec.jpg".format(path=this_location),0)
        thresh_value = cv2.getTrackbarPos("value","Output")
        thresh, result = cv2.threshold(gray_img,thresh_value,255,cv2.THRESH_BINARY)
        if cv2.waitKey(1) == 27:
            break
        cv2.imshow("Output",result)
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()