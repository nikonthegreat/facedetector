import requests
import threading
import dlib
import sys
import os

mutex = threading.Lock()
mutex_session = threading.Lock()

def detectFace(imageUrl):
    mutex.acquire()

    filename = imageUrl[imageUrl.rfind('/')+1:]

    print("downloading image", imageUrl, "file", filename)

    try:
        r = requests.get(imageUrl, timeout=10)
        if r.status_code != 200:
            mutex.release()
            return
    except requests.exceptions.RequestException:
        mutex.release()
        return

    with open(filename, 'wb') as f:
        f.write(r.content)

    detector = dlib.get_frontal_face_detector()
    image = dlib.load_rgb_image(filename)
    dets = detector(image, 1)
    facesCount = len(dets)
    # print("Number of faces detected", facesCount)
    # for i, d in enumerate(dets):
    #     print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
    #         i, d.left(), d.top(), d.right(), d.bottom()))

    os.remove(filename)
    mutex.release()
    return facesCount

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit(255)

    imageUrl = sys.argv[1]
    if not imageUrl:
        exit(255)

    facesCount = detectFace(imageUrl)
    print('faces count', facesCount)

    exit(facesCount)
