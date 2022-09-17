import cv2
import matplotlib.pyplot as plt
import os




def main():
    this_location = os.path.dirname(os.path.abspath(__file__))
    img = cv2.imread("{path}/image/nectec.jpg".format(path=this_location))
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    thresh_value = [50,100,130,200,230]
    plt.subplot(231,xticks=[],yticks=[])
    plt.title("Original")
    plt.imshow(gray_img,cmap="gray")
    for i in range(len(thresh_value)):
        thresh,result = cv2.threshold(gray_img,thresh_value[i],255,cv2.THRESH_BINARY)
        plt.subplot(232+i)
        plt.title("%d"%thresh_value[i])
        plt.imshow(result,cmap="gray")
        plt.xticks([]),plt.yticks([])
    plt.show()



if __name__ == "__main__":
    main()