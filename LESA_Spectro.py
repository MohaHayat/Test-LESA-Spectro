import seabreeze.spectrometers as sb
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np


class Spectro:
    def __init__(self, desired_low, desired_max, int_time):

        # set vars
        self.desired_low = desired_low
        self.desired_max = desired_max
        self.int_time = int_time
        self.file_name = ''
        # init
        self.dark_inten = []
        self.spec_wave = []
        self.spec_inten = []
        self.FLAG_done = 0
        self.FLAG = 0
        self.data = np.array([])

        self.init_device()

    # DESC: uses two given arrays to produce a matplotlib graph
    # IN: x axis array of wave length
    # OUT: x,y graphical plot
    def plot_graph(self, wave_array, inten_array):

        # --- DISPLAY DATA---
        plt.xlabel('Wave Length')
        plt.ylabel('Intensity')

        # type of data plot
        plt.plot(wave_array, inten_array)

        # plot
        plt.show()
        return self.FLAG_done

    # DESC: check to see if the spectrometer's max value is in range of the user's desired values
    # IN: max intensity range, low intensity range, max value of given spectrum
    # OUT: bool TRUE, int 1, or int 2 depending on if the max value of the given spectrum is in the desired range
    def int_check(self, range_max, range_low, val):

        if (val < range_max) and (val > range_low):     # if value is in desired range

            return True
        elif val > range_max:   # if value is larger than the desired max

            self.int_time -= 5000
            return False

        else:                   # if the value is smaller than the desired low

            self.int_time += 5000
            return False

    # DESC: get spectrum wave len and intensity, check to see if the values are in a desired range, change integration
    # time depending on if the value is in range, return an x- axis array of wave len and a y axis array of intensities
    # IN:  spectrometer obj, int desired max val, int desired low val, int integer time, np array of dark values
    # OUT: np array of spec wave len, np array of intensities, FLAG
    def get_spectrum(self, secs):

        self.pause(secs)

        # set integration time
        self.spec.integration_time_micros(self.int_time)

        # get spec wave lens
        spec_wave = self.spec.wavelengths()

        # get spec intensities
        spec_inten = self.spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)

        # subtract dark reading intensities from spec intensities
        spec_inten -= self.dark_inten

        # get the maximum intensity of the first read
        max_int = max(spec_inten)

        # check to see if the max intensity value is in the desired range and change integration time
        checker = self.int_check(self.desired_max, self.desired_low, max_int)

        # while the checker value is not true, and the max int value is not in range.
        while not checker:

            # set new integration time from int_check
            self.spec.integration_time_micros(self.int_time)

            # get new spec wave lens
            spec_wave = self.spec.wavelengths()

            # wait
            self.pause(secs)

            # get new reading of spec intensities
            spec_inten = self.spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)

            # subtract dark reading from new spec intensities reading
            spec_inten -= self.dark_inten

            # get new max intensity val
            max_int = max(spec_inten)

            # check if new val is in range of desired intensities
            checker = self.int_check(self.desired_max, self.desired_low, max_int)

        # return array to be stored in file or plotted
        return spec_wave, spec_inten, self.FLAG_done

    # DESC: gets spectrum and returns numpy arrays, no checking performed, no data storage, only returns raw data
    # IN: int integration time
    # OUT: wave len np array and intensity np array, FLAG
    def raw_get(self, int_time):
        # set integration time
        self.spec.integration_time_micros(int_time)

        # get spec wave lens
        spec_wave = self.spec.wavelengths()

        # get spec intensities
        spec_inten = self.spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)

        spec_inten -= self.dark_inten

        return spec_wave, spec_inten, self.FLAG_done

    # DESC: get singular plot of the current spectrum
    # IN: none
    # OUT: a plot of the spectrum, return FLAG
    def get_spectrum_plot(self):
        spec_wave, spec_inten, self.FLAG = self.get_spectrum(1)

        self.plot_graph(spec_wave, spec_inten)
        return self.FLAG_done

    # DESC: pause for any amount of time
    # IN: integer number of seconds
    # OUT: print statement
    def pause(self, secs):

        time.sleep(secs)

    # DESC: get dark spectrum intensity readings
    # IN: spectrometer object
    # OUT: np array of intensities np.float 64
    def get_dark(self):

        # get wave len / inten data
        self.spec_wave = self.spec.wavelengths()
        spec_inten = self.spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)

        max_int = max(spec_inten)
        while max_int >= 3000:
            spec_inten = self.spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)
            max_int = max(spec_inten)

        self.dark_inten = spec_inten

        return self.FLAG_done

    # DESC: initialize the device
    # IN: none
    # OUT: prints device type connected, returns spectrometer device
    def init_device(self):

        # call list of all connected spectrometers
        devices = sb.list_devices()
        # create object for spectrometers(s)
        self.spec = sb.Spectrometer(devices[0])

        return self.FLAG_done

    # DESC: create data with default spec wave len
    # IN: spectrometer device
    # OUT: create file named whatever the time is, save the wave len spectrum to the file
    def create_file(self):
        now = datetime.datetime.now()
        self.file_name = str(now.month) + '-' + str(now.day) + '-' + str(now.hour) + "-" + str(now.min)

        spec_wave = self.spec.wavelengths()

        np.savetxt(self.file_name, spec_wave, fmt='%10.5f')    # store wave len data

        return self.FLAG_done

    # DESC: append intensity data to file
    # IN: np array of spectrum intensity
    # OUT: append np array to existing file.
    def add_to_file(self, spec_inten):

        file = open(self.file_name, 'a+')                   # open file to append

        file.write("K \n")                                  # row delimiter -  new entry is separated by k

        np.savetxt(file, spec_inten, fmt='%10.5f')         # append data to file

        file.close()                                       # close file

        return self.FLAG_done

    def which_device(self):

        return self.spec.model, self.spec.serial_number, self.spec.pixels       # return device specifications


if __name__ == '__main__':

    jz = Spectro(10000, 60000, 10000)

    print(jz.which_device())

    jz.get_dark()
    jz.create_file()

    counter = 0
    flag = 0

    while counter <= 5:
        a, b, flag = jz.get_spectrum(0)
        jz.add_to_file(b)
        counter += 1

    jz.get_spectrum_plot()
