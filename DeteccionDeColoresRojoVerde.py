import threading
import serial
import cv2
import numpy as np
arduino = serial.Serial('/dev/ttyACM0', 9600)
class Camera(object):
    """
    Base Camera object
    """

    def __init__(self):
        self._cam = None
        self._frame = None
        self._frame_width = None
        self._frame_height = None
        self._ret = False

        self.auto_undistortion = False
        self._camera_matrix = None
        self._distortion_coefficients = None

        self._is_running = False

    def _init_camera(self):
        """
        This is the first for creating our camera
        We should override this!
        """

        pass

    def start_camera(self):
        """
        Start the running of the camera, without this we can't capture frames
        Camera runs on a separate thread so we can reach a higher FPS
        """

        self._init_camera()
        self._is_running = True
        threading.Thread(target=self._update_camera, args=()).start()

    def _read_from_camera(self):
        """
        This method is responsible for grabbing frames from the camera
        We should override this!
        """

        if self._cam is None:
            raise Exception("Camera is not started!")

    def _update_camera(self):
        """
        Grabs the frames from the camera
        """

        while True:
            if self._is_running:
                self._ret, self._frame = self._read_from_camera()
            else:
                break

    def get_frame_width_and_height(self):
        """
        Returns the width and height of the grabbed images
        :return (int int): width and height
        """

        return self._frame_width, self._frame_height

    def read(self):
        """
        With this you can grab the last frame from the camera
        :return (boolean, np.array): return value and frame
        """
        return self._ret, self._frame

    def release_camera(self):
        """
        Stop the camera
        """

        self._is_running = False

    def is_running(self):
        return self._is_running

    def set_calibration_matrices(self, camera_matrix, distortion_coefficients):
        self._camera_matrix = camera_matrix
        self._distortion_coefficients = distortion_coefficients

    def activate_auto_undistortion(self):
        self.auto_undistortion = True

    def deactivate_auto_undistortion(self):
        self.auto_undistortion = False

    def _undistort_image(self, image):
        if self._camera_matrix is None or self._distortion_coefficients is None:
            import warnings
            warnings.warn("Undistortion has no effect because <camera_matrix>/<distortion_coefficients> is None!")
            return image

        h, w = image.shape[:2]
        new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(self._camera_matrix,
                                                               self._distortion_coefficients, (w, h),
                                                               1,
                                                               (w, h))
        undistorted = cv2.undistort(image, self._camera_matrix, self._distortion_coefficients, None,
                                    new_camera_matrix)
        return undistorted


class WebCamera(Camera):
    """
    Simple Webcamera
    """

    def __init__(self, video_src=0):
        """
        :param video_src (int): camera source code (it should be 0 or 1, or the filename)
        """

        super().__init__()
        self._video_src = video_src

    def _init_camera(self):
        super()._init_camera()
        self._cam = cv2.VideoCapture(self._video_src)
        self._ret, self._frame = self._cam.read()
        if not self._ret:
            raise Exception("No camera feed")
        self._frame_height, self._frame_width, c = self._frame.shape
        return self._ret

    def _read_from_camera(self):
        super()._read_from_camera()
        self._ret, self._frame = self._cam.read()
        if self._ret:
            if self.auto_undistortion:
                self._frame = self._undistort_image(self._frame)
            return True, self._frame
        else:
            return False, None

    def release_camera(self):
        super().release_camera()
        self._cam.release()

# Example usage:
if __name__ == "__main__":
    webcam = WebCamera(video_src=0)
    webcam.start_camera()
    while True:
        ret, imageFrame = webcam.read()
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

        red_lower = np.array([170, 70, 30], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

        green_lower = np.array([70, 70, 30], np.uint8)
        green_upper = np.array([100, 255, 255], np.uint8)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

        kernel = np.ones((5, 5), "uint8")
        
        red_mask = cv2.dilate(red_mask, kernel)
        res_red = cv2.bitwise_and(imageFrame, imageFrame, mask = red_mask)
        
        green_mask = cv2.dilate(green_mask, kernel)
        res_green = cv2.bitwise_and(imageFrame, imageFrame, mask = green_mask)

        contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                M = cv2.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if(area > 20000):
                    x, y, w, h = cv2.boundingRect(contour)
                    imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(imageFrame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))    
                    cv2.circle(imageFrame, (cX, cY), 7, (255, 255, 255), -1)
                    if (cX > 150):
                        comando = "rojo"
                        arduino.write(comando.encode())
                    else:
                        comando = "siga"
                        arduino.write(comando.encode())

        contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                M = cv2.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if(area > 20000):
                    x, y, w, h = cv2.boundingRect(contour)
                    imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.circle(imageFrame, (cX, cY), 7, (255, 255, 255), -1)
                    cv2.putText(imageFrame, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
                    if (cX < 490):
                        comando = "verde"
                        arduino.write(comando.encode())
                    else:
                        comando = "siga"
                        arduino.write(comando.encode())
        cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    webcam.release_camera()
