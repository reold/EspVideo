import cv2


class ImageProcessor:
    def __init__(self):
        pass

    def process_image(base_image):

        gray_image = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)

        blured_imaged = cv2.GaussianBlur(gray_image, (9, 9), cv2.BORDER_DEFAULT)

        canny_image = cv2.Canny(
            blured_imaged,
            1,
            20,
            100,
        )

        return canny_image
