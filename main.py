import webview
from ext.WebAPI import Api


global GUIWindow
GUIWindow = None


if __name__ == '__main__':
    print("\n\n")
    print("Programmed by Fido_de07")
    print("Discord: Fido_de02#9227")
    print("NOTE: The GAN wasnt made by me!")
    print("\n")

    api = Api()
    GUIWindow = webview.create_window("ToAnimeConverter - Programmed by Fido_de07 (Discord: Fido_de02#9227)", "src/app.html", width=900, height=500, js_api=api)
    webview.start(gui="gtk")
