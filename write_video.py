import cv2
import os
from datetime import datetime

#class VideoWriter:
def write_video(camera_source, fps, seconds_to_record, path_to_saving_dir='.', saving_name=None):
    '''
    camera_source
        - an index of video device, check 0, 1, 2, 3
    fps
        - frame rate
    seconds_to_record
        - how much seconds of video you want to record
    path_to_saving_dir 
        - path to the target directory, where the video is saved
        if path_to_saving_dir does not exist, it will automatically be created
        default is the working directory
    saving_name
        - the name of the saving video
        default: None
        if saving_name is None then it is set to the current date and time in format DD.MM.YYY, HH-MM-SS
    '''
    if saving_name is not None:
        saving_name = saving_name + '.mp4'
    else:
        saving_name = datetime.now().strftime('%d.%m.%Y, %H-%M-%S') + '.mp4'

    cap = cv2.VideoCapture(camera_source)

    # file name is a current date and time
    path_to_saving_video = os.path.join(path_to_saving_dir, saving_name)

    while True:
        ret, frame = cap.read()

        if ret:
            h, w, ch = frame.shape
            break

    target_frame_num = seconds_to_record*fps
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv2.VideoWriter(path_to_saving_video, fourcc, fps, (w, h))

    for f in range(target_frame_num):
        ret, frame = cap.read()
        if ret:
            writer.write(frame)


    cap.release()
    writer.release()

if __name__ == '__main__':
    fps = 30
    seconds_to_record = 10
    camera_source = 0 # check also 1 or 2

    write_video(
        camera_source=0,
        fps=30,
        seconds_to_record=30
    )
    

