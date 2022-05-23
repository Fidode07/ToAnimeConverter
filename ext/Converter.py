import os
from PIL import Image

import torch
from torchvision.transforms.functional import to_tensor, to_pil_image

from ext.model import Generator


torch.device("cuda")

torch.backends.cudnn.enabled = False
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True


class MyConverter:

    def load_image(self, image_path, x32=False):
        img = Image.open(image_path).convert("RGB")

        if x32:
            def to_32s(x):
                return 256 if x < 256 else x - x % 32
            w, h = img.size
            img = img.resize((to_32s(w), to_32s(h)))

        return img

    def convert_image(self, image_location, the_checkpoint, output_directory, device):
        print("Net Generator ...")
        net = Generator()
        net.load_state_dict(torch.load(the_checkpoint, map_location="cpu"))
        net.to(device).eval()
        print(f"model loaded: {the_checkpoint}")

        print("The Classic Dir Shit")
        os.makedirs(output_directory, exist_ok=True)

        print("Okay ... Look at the Extension!")
        if os.path.splitext(image_location)[-1].lower() in [".jpg", ".png", ".bmp", ".tiff", ".jpeg", ".webp"]:
            pass
        else:
            print("MEHHHHH")
            return "Wrong File Format!"

        print("Load Image ...")
        image = self.load_image(image_location, True)

        with torch.no_grad():
            image = to_tensor(image).unsqueeze(0) * 2 - 1
            out = net(image.to(device), False).cpu()
            out = out.squeeze(0).clip(-1, 1) * 0.5 + 0.5
            out = to_pil_image(out)

        print("We got here!")
        image_name: str = os.path.basename(image_location)
        out.save(os.path.join(output_directory, image_name))
        print(f"image saved: {output_directory, image_name}")


if __name__ == "__main__":
    print("This is the Wrong File, you have to run main.py!")
