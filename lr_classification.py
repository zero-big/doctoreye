import cv2
import numpy as np

def lr_classifi(image_path):
    image = cv2.imread(image_path)
    # Get the dimensions of the original image
    height, width, _ = image.shape
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Perform edge detection using Canny
    edges = cv2.Canny(blurred, 50, 150)
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Initialize variables to store the brightest point and its brightness
    brightest_point = None
    max_brightness = 0
    # Loop over the contours
    for contour in contours:
        # Approximate the contour to reduce the number of points
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        # Check if the contour is approximately circular
        if len(approx) >= 8:
            # Compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(contour)
            # Crop the circular region
            mask = np.zeros_like(gray)
            cv2.drawContours(mask, [contour], 0, 255, -1)
            masked_gray = np.where(mask == 255, gray, 0)
            # Find the brightest point within the circular region
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(masked_gray)
            # Update the brightest point and its brightness if necessary
            if maxVal > max_brightness:
                brightest_point = maxLoc
                max_brightness = maxVal
# If no circular contours were found, skip further processing
    if brightest_point is None:
        position = "불명"
    else:
        # Draw a circle around the brightest point
        cv2.circle(image, brightest_point, 5, (255, 0, 0), 2)
        # Calculate the center of the original image
        center_x = width // 2
        # Determine if the blue dot is to the left or right of the center
        if brightest_point[0] < center_x:
            position = "좌안"
        elif brightest_point[0] > center_x:
            position = "우안"
        else:
            position = "불명"


        # Display the result
        # cv2.imshow('Result', image)
        # print(f"The blue dot is to the {position} of the center of the original image.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return position