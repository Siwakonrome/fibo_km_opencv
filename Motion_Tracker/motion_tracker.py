import cv2 
import os


def main():
    this_location = os.path.dirname(os.path.abspath(__file__))
    cap = cv2.VideoCapture("{path}/video/Walking.mp4".format(path=this_location))
    check , frame1 = cap.read()
    check , frame2 = cap.read()
    while True:
        if check == True:
            motiondiff= cv2.absdiff(frame1,frame2)
            gray=cv2.cvtColor(motiondiff,cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),0)
            thresh,result = cv2.threshold(blur,15,255,cv2.THRESH_BINARY)
            dilation = cv2.dilate(result,None,iterations=3)
            contours,hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                M = cv2.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                (x,y,w,h) = cv2.boundingRect(contour)
                if cv2.contourArea(contour)<2500:
                    continue
                cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.circle(frame1, (cX, cY), 5, (0, 0, 255), -1)
                cv2.putText(frame1, str((cX, cY)) , (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow("Output",frame1)
            frame1=frame2
            check,frame2 = cap.read()
            if cv2.waitKey(1) == 27:
                break
        else :
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()