import cv2

# loading the pretrained haarcascade face detect
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# start the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit(1)

def getDeltaLoc(prev_loc_x = 0, prev_loc_y = 0):
    """
    return (delta_x, delta_y), (center_x, center_y)
    """
    global cap
    global face_cascade

    # capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive the frame")
        return
    
    # detect faces in the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # find the largest face
    if len(faces) > 0:
        largest_face = max(faces, key=lambda face: face[2] * face[3])
        x, y, w, h = largest_face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        center_x = x + w // 2
        center_y = y + h // 2
        cv2.circle(frame, (center_x, center_y), radius=2, color=(0, 255, 0), thickness=-1)
        
        # calculate differences
        delta_x = center_x - prev_loc_x
        delta_y = center_y - prev_loc_y

        if prev_loc_x == 0 and prev_loc_y == 0:
            return (0,0), (center_x, center_y)
        else:
            return (delta_x, delta_y), (center_x, center_y)
        
    else:
        return (0,0), (0,0)
    
def getDirectionChange(change : tuple, current = [0,0]):
    """
    return [-1,0] for left
    return [0,-1] for up
    return [1,0] for right
    return [0,1] for down
    return None for no change
    """
    delta_x = change[0]
    delta_y = change[1]
    maximum = max(abs(delta_x),abs(delta_y))
    threshold = 30
    if abs(maximum) >= threshold:
        if maximum == abs(delta_x):
            return [1,0] if delta_x < 0 else [-1,0]
        elif maximum == abs(delta_y):
            return [0,-1] if delta_y < 0 else [0,1]
    else:
        return current

# Testing
if __name__ == "__main__":
    from time import sleep
    change, location = getDeltaLoc()
    while True:
        change, location = getDeltaLoc(location[0], location[1])
        print("Change: ", change)
        direction = getDirectionChange(change)
        direction_str : str
        match (direction):
            case [-1,0]:
                direction_str = "left"
            case [0,-1]:
                direction_str = "up"
            case [1,0]:
                direction_str = "right"
            case [0,1]:
                direction_str = "down"
            case [0,0]:
                direction_str = "none"
        print("Direction: ", direction_str)
        sleep(0.5)