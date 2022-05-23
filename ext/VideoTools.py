import glob

import cv2
import os


global FrameTempFolder
FrameTempFolder: str = "FrameTEMP"


def split_into_frames(video_location: str):
    if not os.path.isdir(FrameTempFolder):
        os.mkdir(FrameTempFolder)

    vidcap = cv2.VideoCapture(video_location)
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(FrameTempFolder+"/%d.jpg" % count, image)
        success, image = vidcap.read()
        count += 1


def get_video_fps(video_location: str):
    print("WE WAS CALLED")
    video = cv2.VideoCapture(video_location)

    (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')

    if int(major_ver) < 3:
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    else:
        fps = video.get(cv2.CAP_PROP_FPS)

    video.release()
    return fps


def images_to_video(file_name: str, fps, x, y):
    print("Here we was called!")
    try:
        images = []
        file_amount = 0
        for image in glob.glob("FrameTEMP/*"):
            file_amount += 1

        i = 0
        while i != file_amount:
            images.append(f"{i}.jpg")
            i += 1

        print(len(images))

        img_array = []
        si = 0
        for filename in images:
            print("FrameTEMP/"+filename)
            img = cv2.imread("FrameTEMP/"+filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)
            print(si)
            si += 1

        print("Now the ... Out")
        print(f"Safe with: output/{file_name}.mp4")
        out = cv2.VideoWriter(f'output/{file_name}.mp4', cv2.VideoWriter_fourcc(*'MP4V'), fps, (x, y))

        print("Build the Shit!")

        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        return 0
    except Exception as e:
        print(e)
        print("Look ... An Error ... Above this Message!")
        return 1


def get_video_size(video_location: str):
    vcap = cv2.VideoCapture(video_location)

    if vcap.isOpened():
        width = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return [width, height]

