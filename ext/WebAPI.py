from ext import Converter
import pathlib
from tkinter import messagebox
from ext import VideoTools
import os
import glob
from tkinter import Tk
from tkinter.filedialog import askopenfilename


class Api:

    def __init__(self) -> None:
        self.result = None
        self.MyConv = Converter.MyConverter()
        print("Api was called.")

    def open_new_file_dialog(self, file_types):
        root = Tk()
        root.attributes('-alpha', 0.01)

        root.attributes('-topmost', True)
        root.withdraw()
        result = askopenfilename(title="Choose Image",
                                 filetypes=file_types)
        root.destroy()
        return result

    def convert_image(self, the_model_name):
        result = self.open_new_file_dialog([('Image Files', ('.png', '.jpg', ".bmp", ".tiff", ".jpeg", ".webp"))])
        print(result)
        if result[0] == "" or result[0] == " " or result[0] is None:
            print("He canceled")
            return

        if os.path.isfile(result):
            print("Ok ...")
            self.MyConv.convert_image(image_location=result, the_checkpoint="ext/weights/"+the_model_name, output_directory="output", device="cpu")
            ourPath = str(pathlib.Path(__file__).parent.absolute())
            size = len(ourPath)
            ourPath = ourPath.replace(ourPath[size - 4:], "")
            response = {'message': 'Succefully Generated. Look at: '+ourPath+'/output'}
            return response
        else:
            print("File doesnt exists!")
            messagebox.showerror("ERROR - 404", "The selected File, does not exists!")

    def convert_video(self, the_model_name):
        self.result = self.open_new_file_dialog([('Video Files', '.mp4')])
        print(self.result)
        if self.result[0] == "" or self.result[0] == " " or self.result[0] is None:
            print("He canceled")
            return

        if os.path.isfile(self.result):
            print("(Video) Ok ...")
            VideoTools.split_into_frames(self.result)
            print("Scann FPS ...")
            video_fps = VideoTools.get_video_fps(self.result)
            print("FOUND!")
            print(video_fps)

            file_amount = 0
            for image in glob.glob("FrameTEMP/*"):
                file_amount += 1

            vSize = VideoTools.get_video_size(self.result)

            print(f"Video Width: {str(vSize[0])}")
            print(f"Video Height: {str(vSize[1])}")

            i = 0
            while i != file_amount:
                print(" ")
                print(f"Convert Frame ({i}.jpg) [{i}] ...")
                self.MyConv.convert_image(image_location=f"FrameTEMP/{i}.jpg", the_checkpoint="ext/weights/"+the_model_name, output_directory="FrameTEMP", device="cpu")
                print(" ")
                i += 1

            print("LOOP FINISHED")
            filenm = pathlib.Path(self.result).stem
            print("Now go to Generate ...")
            video_result = VideoTools.images_to_video(str(filenm), int(video_fps), int(vSize[0]), int(vSize[1]))

            for file in glob.glob("FrameTEMP/*.*"):
                os.remove(file)

            if video_result == 0:
                ourPath = str(pathlib.Path(__file__).parent.absolute())
                size = len(ourPath)
                ourPath = ourPath.replace(ourPath[size - 4:], "")
                response = {"message": f"Your video was generated successfully. Look in {ourPath}/output"}
            else:
                response = {"message": "Sorry, there must have been a mistake. Check out the output to find out more."}

            return response
