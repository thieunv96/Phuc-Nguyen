import cv2
import numpy as np 
import glob



def processing(img, name = "NoName.jpg", debug = False):
    h , w, _ = img.shape
    k = int(min(w, h) / 10)
    k = k if k % 2 != 0 else k + 1
    img_pros = img[ int(h/10):int(h/2), int(w/2):w]
    img_pros = cv2.bilateralFilter(img_pros, 9, 49, 49)
    img_pros = cv2.medianBlur(img_pros, 9)
    img_gray = cv2.cvtColor(img_pros, cv2.COLOR_BGR2GRAY)
    sobelx64f = cv2.Sobel(img_gray,cv2.CV_64F,1,0,ksize=1)
    abs_sobel64f = np.absolute(sobelx64f)
    img_sobel = np.uint8(abs_sobel64f)
    _, img_threshold = cv2.threshold(img_sobel, 0, 255, cv2.THRESH_OTSU)
    _, contours, _ = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        xb, yb, wb, hb = cv2.boundingRect(cnt)
        if(hb > 200):
            cv2.drawContours(img_threshold, [cnt], 0, (0), -1)
    kernel = np.ones((1,k),np.uint64)
    result = cv2.morphologyEx(img_threshold, cv2.MORPH_CLOSE, kernel)
    k = int(k/2) if int(k/2) % 2 != 0 else int(k/2) + 1
    kernel = np.ones((1,k),np.uint8)
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
    _, contours, _ = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        xb, yb, wb, hb = cv2.boundingRect(cnt)
        if(hb > 30):
        # if(wb > w/4):
            cv2.rectangle(img_pros, (xb, yb), (xb+wb, yb+hb), (0,255,0), 3)
    img[int(h/10):int(h/2), int(w/2):w] = img_pros
    # img_blured = cv2.medianBlur(img_pros, 83)
    # img_sub = cv2.absdiff(img_pros, img_blured)
    # kernel = np.ones((k,k),np.uint8)
    # img_dilated = cv2.dilate(img_pros, kernel)
    # img_eroded = cv2.erode(img_pros, kernel)
    # img_abs = cv2.absdiff(img_dilated, img_eroded)
    # img_gray = cv2.cvtColor(img_abs, cv2.COLOR_BGR2GRAY)
    # _, img_threshold = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU)
    # # img_threshold = cv2.morphologyEx(img_threshold, cv2.MORPH_OPEN, kernel)
    # _, contours, _ = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # for cnt in contours:
    #     xb, yb, wb, hb = cv2.boundingRect(cnt)
    #     if(hb > 300):
    #         cv2.drawContours(img_threshold, [cnt], 0, (0), -1)
    cv2.imwrite(name, img)


def test():
    files = glob.glob("../images/*.jpg")
    for f in files:
        img = cv2.imread(f, 1)
        name = f.split("\\")[-1]
        processing(img, name = name)

if __name__ == "__main__":
    test()
