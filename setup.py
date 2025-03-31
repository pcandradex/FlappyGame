from cx_Freeze import setup, Executable
import os

path = "./assets"
asset_list = os.listdir(path)
asset_list_complete = [os.path.join(path, assets).replace("\\", "/") for assets in asset_list]
print(asset_list_complete)

executables = [Executable("main.py")]
files = {"include_files": asset_list_complete, "packages": ["pygame"]}


setup(
    name="Flappy Game",
    version="1.0",
    description="Flappy Game app",
    options={"build.exe": files},
    executables=executables
)