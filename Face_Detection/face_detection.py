import cv2 
import os




def main():
    cap = cv2.VideoCapture(0)
    this_location = os.path.dirname(os.path.abspath(__file__))
    face_cascade = cv2.CascadeClassifier("{path}/Detect/haarcascade_frontalface_default.xml".format(path=this_location))
    while True:
        check , frame = cap.read()
        if check == True :
            gray_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            face_detect = face_cascade.detectMultiScale(gray_img,1.2,5)
            for (x,y,w,h) in face_detect:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),thickness=5)
            cv2.imshow("Output",frame)
            if cv2.waitKey(1) == 27:
                break
        else :
            break
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()