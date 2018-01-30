from pyperlib import colordetect, helper
from PIL import Image, ImageOps
from pathlib import Path


class DesignerFactory(helper.NameFactory):
    """Create designers from names."""

    suffix = "Designer"
    pool = globals()


class BaseDesigner:
    """Create wallet designs from a template and logo."""

    wallet = None
    paths = []

    def __init__(self, path):
        """Create a designer with a path."""
        self.path = path

        self.images = []
        prefix_path = path + "/templates/" + self.wallet + "/"
        for name in self.paths:
            img = self.get_img(prefix_path + name)
            self.images.append(img)

        self.save_path = path + "/wallets/" + self.wallet + "/"

    def iter_logos(self):
        """Iterate through the logos and their names."""
        for p in Path(self.path + "/logos").iterdir():
            yield str(p), p.name

    def get_img(self, name):
        """Return the Image file at name."""
        img = Image.open(name)
        img = img.convert("RGBA")
        return img

    def detect_colors(self, img):
        """Use colordetect to find colors in the image."""
        detector = colordetect.Detector(img)
        return detector.run()

    def colorize(self, img, colors):
        """Colorize the image with colors."""
        img = img.convert("L")

        c1 = colors[0].rgb
        c2 = colors[1].rgb
        img = ImageOps.colorize(img, c2, c1)
        return img.convert("RGBA")

    def run_one(self, logo, name):
        """Create a wallet from a logo."""
        raise NotImplementedError("This designer has no run_one function.")

    def run(self):
        """Run the designer on all logos."""
        for logo, name in self.iter_logos():
            self.run_one(logo, name)


class SixfoldDesigner(BaseDesigner):
    """Create sixfold wallet designs from a logo."""

    wallet = "sixfold"
    paths = ["gradient.png", "overlay.png", "design.png"]

    def run_one(self, logo, name):
        """Create a sixfold wallet design."""
        img = self.get_img(logo)
        colors = self.detect_colors(img)

        gradient, overlay, design = self.images

        gradient = self.colorize(gradient, colors)

        background = Image.blend(gradient, overlay, 0.5)
        design = Image.alpha_composite(background, design)
        design.save(self.save_path + name)
