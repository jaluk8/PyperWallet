import PIL
import random
import copy


class Color:
    """Store a pixel's color and interact with other colors."""

    approx_dist = 300  # The distance between to similar colors.

    def __init__(self, r, g, b, a=0, rnd=1):
        """Initialize the color with rgb."""
        self.r = round(r / rnd) * rnd
        self.g = round(g / rnd) * rnd
        self.b = round(b / rnd) * rnd
        self.a = round(a / rnd) * rnd

    def distance(self, other):
        """Calculate the 'distance' to another color."""
        dr = other.r - self.r
        dg = other.g - self.g
        db = other.b - self.b
        return dr**2 + dg**2 + db**2

    def similar(self, other):
        """Return whether a color is similar to another."""
        return self.distance(other) <= self.approx_dist

    @staticmethod
    def mean(colors):
        """Return the mean color from a list of colors."""
        amount = float(len(colors))
        if amount == 0:
            return None

        r_mean = sum([c.r for c in colors]) / amount
        g_mean = sum([c.g for c in colors]) / amount
        b_mean = sum([c.b for c in colors]) / amount

        return Color(r_mean, g_mean, b_mean)

    @classmethod
    def unique(cls, colors):
        """Merge similar colors together in a set."""
        colors = list(colors)
        similars = True
        while similars:
            similars = False
            closest_dist = cls.approx_dist
            close_i = None
            close_j = None

            for i, c1 in enumerate(colors):
                for j, c2 in enumerate(colors):
                    if i != j:
                        dist = c1.distance(c2)
                        if dist <= closest_dist:
                            close_i = i
                            close_j = j
                            closest_dist = dist
                            similars = True

            if similars:
                c1 = colors.pop(close_i)
                if close_j > close_i:
                    close_j -= 1
                c2 = colors.pop(close_j)
                avg = Color.mean([c1, c2])
                colors.append(avg)

        return colors

    def __repr__(self):
        """Return the color's repr string."""
        return "Color({0}, {1}, {2})".format(self.r, self.g, self.b)

    def __hash__(self):
        """Hash the color."""
        return hash(self.r) + hash(self.g) + hash(self.b)

    def __eq__(self, other):
        """Return whether a color equals another."""
        return self.r == other.r and self.g == other.g and self.b == other.b


class Cluster:
    """A k-means cluster, a collection of colors."""

    def __init__(self, center):
        """Initialize the cluster with no colors and a center."""
        self.colors = []
        self.center = center

    def recenter(self):
        """Recreate the center as the mean of all colors."""
        mean = Color.mean(self.colors)
        if mean is not None:
            self.center = mean


class KMeans:
    """A k-means controller. It runs k-means."""

    def __init__(self, colors, count):
        """Initialize the list of clusters by creating centers."""
        assert count > 0
        self.colors = colors
        self.count = count
        self.clusters = []

        color_set = list(set(colors))
        for _ in range(count):
            center = random.choice(color_set)
            cluster = Cluster(center)
            self.clusters.append(cluster)

    def iteration(self):
        """Perform one iteration of k-means."""
        for cl in self.clusters:
            cl.colors = []
        for co in self.colors:
            closest = None
            dist = float('inf')
            for cl in self.clusters:
                d = cl.center.distance(co)
                if d < dist:
                    dist = d
                    closest = cl
            closest.colors.append(co)
        for cl in self.clusters:
            cl.recenter()

    def centers(self):
        """Return a list of all centers."""
        return [cl.center for cl in self.clusters]

    def run(self):
        """Run the k-means to completion."""
        old_c = None
        while old_c != self.centers():
            old_c = copy.deepcopy(self.centers())
            self.iteration()


class Detector:
    """Detect the colors in a logo."""

    def __init__(self, img):
        """Initialize the detector with an image."""
        self.colors = []
        self.img = img.convert('RGBA')
        for x in range(img.width):
            for y in range(img.height):
                p = Color(*self.img.getpixel((x, y)), rnd=4)
                if p.a != 0:
                    self.colors.append(p)
        self.cleanup()

    def cleanup(self):
        """Remove colors that are outliers."""
        color_d = {}
        for p in self.colors:
            if p not in color_d:
                color_d[p] = 0
            color_d[p] += 1
        total = len(self.colors)

        self.colors = []
        for co, count in color_d.items():
            if count / total > 0.01:
                self.colors += [co for _ in range(count)]

    def run(self, count=10):
        """Return a list of colors in the image."""
        km = KMeans(self.colors, count)
        km.run()
        colors = set(km.centers())
        uniques = Color.unique(colors)
        if len(uniques) == 0:
            return [Color(0, 0, 0), Color(255, 255, 255)]
        elif len(uniques) == 1:
            return [uniques[0], Color(255, 255, 255)]
        else:
            return uniques
