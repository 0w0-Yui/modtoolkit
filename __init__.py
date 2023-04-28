bl_info = {
    "name": "Yui's Modding Toolkit",
    "description": "Useful toolkit for modding",
    "author": "0w0-Yui <yui@lioat.cn>",
    "version": (0, 2, 0),
    "blender": (2, 83, 0),
    "location": "View 3D > Toolshelf",
    "doc_url": "https://github.com/0w0-Yui/modtoolkit",
    "tracker_url": "https://github.com/0w0-Yui/modtoolkit/issues",
    "category": "Object",
}

from . import modtoolkit


def register():
    modtoolkit.register()


def unregister():
    modtoolkit.unregister()


if __name__ == "__main__":
    modtoolkit.register()
