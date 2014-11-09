__author__ = 'Marek'

import numpy as np


class StaffRemover:

    def __init__(self, staff, image):
        self.bin_image = image
        self.staff = staff

    def remove_at(self, peak_index, new_image=None):
        if new_image is None:
            new_image = np.array(self.bin_image)

        staff_line_height = 1.1*self.staff.line_height

        # for each pixel try to find longest black run over y-axis
        for pixel_x in xrange(new_image.shape[1]):
            if new_image[peak_index, pixel_x] == 1:
                continue

            min_y = peak_index-1
            while new_image[min_y, pixel_x] == 0 and min_y > 0:
                min_y -= 1

            max_y = peak_index+1
            while new_image[max_y, pixel_x] == 0 and max_y < new_image.shape[0]:
                max_y += 1

            if max_y-min_y < staff_line_height:
                for pixel_y in xrange(min_y, max_y):
                    new_image[pixel_y, pixel_x] = 1

    def remove_all(self):
        new_image = np.array(self.bin_image)

        for peak_index in self.staff.line_indices:
            self.remove_at(peak_index, new_image)

        return new_image
