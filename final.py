import numpy as np
import cv2
import streamlit as st

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])

colors = [] # contains identified colors of the flag
centres = {} # contains centroids of each bounding rectangle for their respective colours
def check_color(x1,y1):
    color = ''
    if red_mask[y1,x1]==255:
        color = 'red'
    elif black_mask[y1,x1]==255:
        color = 'black'
    elif yellow_mask[y1,x1]==255:
        color='yellow'
    elif white_mask[y1,x1]==255:
        color='white'
    elif blue_mask[y1,x1]==255:
        color='blue'
    elif green_mask[y1,x1]==255:
        color='green'
    elif orange_mask[y1,x1]==255:
        color='orange'
    colors.append(color)
    centres[color] = [x1,y1]


def makeBox(img, mask):
    contours, _ = cv2.findContours(mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
   
    for _, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 100):
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y),
                                        (x + w, y + h),
                                        (0, 100, 255), 2)
            x1 = int(x + w/2)
            y1 = int(y + h/2)
            check_color(x1,y1)


if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img2 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #st.image(img)
    st.image(img2, caption = 'Original Image')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,threshold = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    red_lower = np.array([0,0,50], np.uint8)
    red_upper = np.array([50, 50, 255], np.uint8)
    red_mask = cv2.inRange(img, red_lower, red_upper)

    green_lower = np.array([0, 75, 0], np.uint8)
    green_upper = np.array([75, 255, 70], np.uint8)
    green_mask = cv2.inRange(img, green_lower, green_upper)

    yellow_lower = np.array([20, 52, 72], np.uint8)
    yellow_upper = np.array([36, 255, 255], np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    black_lower = np.array([0, 0, 0], np.uint8)
    black_upper = np.array([50, 50, 50], np.uint8)
    black_mask = cv2.inRange(img, black_lower, black_upper)

    white_lower = np.array([215, 215, 215], np.uint8)
    white_upper = np.array([255, 255, 255], np.uint8)
    white_mask = cv2.inRange(img, white_lower, white_upper)

    orange_lower = np.array([10, 80, 2], np.uint8)
    orange_upper = np.array([20, 255, 255], np.uint8)
    orange_mask = cv2.inRange(hsvFrame, orange_lower, orange_upper)

    st.image(white_mask, caption="white mask", use_column_width=True)
    st.image(red_mask, caption="red mask", use_column_width=True)
    st.image(blue_mask, caption="blue mask", use_column_width=True)
    st.image(yellow_mask, caption="yellow mask", use_column_width=True)
    st.image(green_mask, caption="green mask", use_column_width=True)
    st.image(black_mask, caption="black mask", use_column_width=True)
    st.image(orange_mask, caption="orange mask", use_column_width=True)

 
    makeBox(img, red_mask)
    makeBox(img, green_mask)
    makeBox(img, blue_mask)
    makeBox(img, yellow_mask)
    makeBox(img, white_mask)
    makeBox(img, black_mask)
    makeBox(img, orange_mask)

    germany = ['red', 'yellow', 'black'] #same colors for belgium
    france = ['red', 'blue', 'white'] #same colors for russia
    abu = ['red', 'white']
    ukraine = ['blue', 'yellow']
    peru = ['red','red', 'white']
    ireland = ['green', 'white', 'orange']
    print(centres)
    if colors == germany:
        print(centres)
        if centres['red'][0]>centres['yellow'][0]:
            st.markdown('''Flag : Belgium <br>
              Colours: Black, Yellow, Red<br>
             ''', True)
        elif centres['red'][1]<centres['yellow'][1]:
            st.markdown('''Flag : Germany <br>
              Colours: Black, Red, Yellow<br>
             ''', True)
    elif colors == france:
        if centres['blue'][1]<centres['red'][1]:
            st.markdown('''Flag : Russia <br>
            Colours: White, Blue, Red''', True)
        else: 
            st.markdown('''Flag : France <br>
            Colours: Blue, White, Red''', True)
    elif colors == abu:
        st.markdown('''Flag : Abu Dhabi <br>
        Colours: Red, White''', True)
    elif colors == peru:
         st.markdown('''Flag : Peru <br>
        Colours: Red, White''', True)
    elif colors == ireland:
        st.markdown('''Flag : Ireland <br>
        Colours: Green, White, Orange''', True)
    elif colors == ukraine:
         st.markdown('''Flag : Ukraine <br>
        Colours: Blue, Yellow''', True)   
         
    print(colors)
    st.write("Colors: ", colors)