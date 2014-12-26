from math import ceil

__author__ = 'Marek'

import numpy as np


class StaffRemover:

    def __init__(self, staff, image):
        self.bin_image = image
        self.staff_finder = staff

    def remove_at(self, peak_index, new_image=None, peak_tolerance=True):
        if new_image is None:
            new_image = np.array(self.bin_image)

        staff_line_height = int(ceil(1.1*self.staff_finder.line_height))

        # for each pixel try to find longest black run over y-axis
        for pixel_x in xrange(new_image.shape[1]):
            # peak = peak_index
            peak = -1

            # find black pixel within tolerance
            for i in xrange(-peak_tolerance*staff_line_height, peak_tolerance*staff_line_height+1):
                if peak_index+i > 0 and peak_index+i < new_image.shape[0] and new_image[peak_index+i, pixel_x] == 0:
                    peak = peak_index+i
                    break

            if peak < 0:
                continue

            min_y = peak-1
            while new_image[min_y, pixel_x] == 0 and min_y > 0:
                min_y -= 1

            max_y = peak+1
            while new_image[max_y, pixel_x] == 0 and max_y < new_image.shape[0]:
                max_y += 1

            if max_y-min_y <= staff_line_height:
                for pixel_y in xrange(min_y, max_y):
                    new_image[pixel_y, pixel_x] = 1

    def remove_all(self):
        new_image = np.array(self.bin_image)

        for staff in self.staff_finder.staffs_with_helper_lines:
            for peak_index in staff:
                if peak_index <= 0 or peak_index >= new_image.shape[0]:
                    continue

                self.remove_at(peak_index, new_image)

        return new_image
