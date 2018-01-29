from pyperlib import colordetect
from unittest import TestCase
from PIL import Image, ImageDraw


class TestColor(TestCase):
    """Test that the color interface works correctly."""

    colors = [
        (0, 0, 0),
        (10, 10, 10),
        (0, 255, 255),
        (255, 0, 255),
        (255, 255, 0),
        (255, 255, 255),
        (11, 11, 11)
    ]
    colors_made = False

    def __init__(self, *args, **kwargs):
        """Initialize the testcase."""
        super().__init__(*args, **kwargs)
        self.mkcolors()

    def mkcolors(self):
        """Create colors from a list of tuples."""
        if not self.colors_made:
            self.colors = [colordetect.Color(*rgb) for rgb in self.colors]
            self.colors_made = True

    def test_round(self):
        """Test that color rounding works."""
        c1 = self.colors[0]
        c2 = self.colors[1]
        c3 = self.colors[5]

        self.assertNotEqual(c1, c2)
        c4 = colordetect.Color(11, 11, 11, rnd=5)
        self.assertEqual(c4, c2)
        c5 = colordetect.Color(13, 13, 13, rnd=5)
        self.assertNotEqual(c5, c2)

    def do_dist_test(self, i, j, dist):
        """Test that the distance between two colors is dist."""
        c1 = self.colors[i]
        c2 = self.colors[j]
        self.assertEqual(c1.distance(c2), dist)

    def test_dist(self):
        """Test distance calculation between colors."""
        self.do_dist_test(0, 2, 130050)
        self.do_dist_test(2, 3, 130050)
        self.do_dist_test(3, 4, 130050)
        self.do_dist_test(4, 5, 65025)

    def test_similar(self):
        """Test the Color.similar method."""
        c1 = self.colors[0]
        c2 = self.colors[1]
        c3 = self.colors[6]

        self.assertTrue(c1.similar(c2))
        self.assertFalse(c1.similar(c3))

    def test_mean(self):
        """Test color mean calculation."""
        mean1 = colordetect.Color.mean(self.colors[2:5])
        mean2 = colordetect.Color(170, 170, 170)
        self.assertEqual(mean1, mean2)

    def do_unique_test(self, colors, count):
        """Assert that running unique on colors works."""
        uniq = colordetect.Color.unique(colors)
        self.assertEqual(len(uniq), count)

        min_dist = colordetect.Color.approx_dist
        for c1 in uniq:
            for c2 in uniq:
                if c1 is not c2:
                    self.assertTrue(c1.distance(c2) > min_dist)

    def test_unique(self):
        """Test that unique filters similar colors."""
        cs1 = self.colors[:2] + [self.colors[6]]
        self.do_unique_test(cs1, 1)

        cs2 = self.colors[:6]
        self.do_unique_test(cs2, 5)


class TestDetector(TestCase):
    """Test detecting colors from an image."""

    transparent = (0, 0, 0, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    orange = (255, 95, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    grey = (10, 10, 10)

    draw_coords = [
        [0, 0, 5, 5],
        [0, 5, 5, 10],
        [5, 0, 10, 5],
        [5, 5, 10, 10]
    ]

    def do_img_test(self, background, colors, output):
        """Create an image and detect the colors in it."""
        assert len(colors) <= 4

        img = Image.new("RGBA", (10, 10), background)

        draw = ImageDraw.Draw(img)
        for i, c in enumerate(colors):
            draw.ellipse(self.draw_coords[i], fill=c)

        detector = colordetect.Detector(img)
        uniques = detector.run()
        expected = [colordetect.Color(*rgb) for rgb in output]
        self.assertEqual(len(expected), len(uniques))
        for e in expected:
            match = False
            found_u = None
            for u in uniques:
                if e.similar(u):
                    match = True
                    found_u = u
            self.assertTrue(match)
            uniques.remove(found_u)

    def do_test_set(self, *args):
        """Repeat an img test many times to check for inconsistency."""
        for _ in range(10):
            self.do_img_test(*args)

    def test_detect(self):
        """Make and detect many images."""
        in1 = [self.orange]
        out1 = [self.orange, self.white]
        self.do_test_set(self.transparent, in1, out1)

        in2 = [self.orange, self.grey]
        out2 = [self.black, self.orange]
        self.do_test_set(self.black, in2, out2)

        in3 = [self.orange, self.blue, self.black, self.grey]
        out3 = [self.orange, self.black, self.blue]
        self.do_test_set(self.green, in3, out3)
