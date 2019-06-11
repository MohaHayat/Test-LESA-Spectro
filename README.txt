LESA-PYTHON-SPECTRO

[DESC]
This library takes the the python ported Ocean Optics Seabreeze library by Andreas Poehlmann (ap) and optimizes and develops it for LESA's LED measurement research. 

[INSTALLATION]
This installation guide is for linux but can be easily altered for windows and mac operatings systems. Refer to https://github.com/ap--/python-seabreeze for further documentation. 
	
	For Ubuntu-Linux using Anaconda:
	
	(I) Install ap's python Seabreeze:	 
	
	1. ap's python-seabreeze is packaged with Anaconda. Install Anaconda on your machine.	
	2. Run the following in terminal:
	   conda install -c poehlmann python-seabreeze 
	   this will install the module and dependencies LESA's python library uses 
	3. Install the following file into /etc/udev/rules.d. File: https://raw.githubusercontent.com/ap--/python-seabreeze/master/misc/10-oceanoptics.rules
	   A back-up can be found on the LESA github repository. 
	4. You can use 'curl' to easily install the above file into the /etc/udev/rules.d directory
	   You can find curl documentation here: https://curl.haxx.se/ 
	5. After saving the .rules file to /etc/udev/rules.d , run the following: 
	   sudo udevadm control --reload-rules 
	6. Re-plug your spectrometer.  
	
	(II) Install LESA-PYTHON-SPECTRO 

[USAGE]
After installing python-Seabreeze, you can now use LESA's library. 

The following is an example of possible use cases. For full documentation refer to the LESA github repository or the JazSpectroLib. 

First locate and install the library file: from [OPT].JazSpectroLib import *

Create the object to start scanning: jz = Jaz(desired_low, desired_max, int_time)
	Where desired_low is the low bound of the desired intensity range 
	Where desired_max is the high bound of the desired intensity range
	Where int_time is a user given integration time 

Now you can use jz to control the spectrometer: 

	Use the auto-scanner to scan an area: jz.auto_scanner(runs, secs) 
	Where runs is the number of times you want to take a reading, and secs is an 	interval time in seconds. Note: currently the reading already has a built 	in .5 second delay time. 

	Use pause to force the spectrometer to wait: jz.pause(secs) 
	Where secs is an interval time in seconds. 

	Use get_sepctrum_pot to get one reading and produce a plot: 	jz.get_spectrum_plot() 
	
	Use raw_get to get two raw arrays of wave len and intensity arrays: a, b = 	jz.raw_get(int_time)
	
	Where 'a' and 'b' are turned into numpy float64 arrays
	Where int_time is a user entered integration time 

	Use plot_graph to plot two arrays: jz.plot_graph(a,b) 
	Where a and b are arrays. The purpose of this is to read two arrays from a 	file and produce a plot
	or to plot two arrays from raw_get 

	Use add_to_file to add whatever data you gathered to a file: 	jz.add_to_file(spec_inten)

	Where spec_inten is a np array of intensities. 
	Every time you create a Jaz object, our library will create a text data file 	and will automatically set wave lengths as the x-axis. Every time you run 	auto_scanner or run add_to_file, the data is added to the text data file. The 	file’s name is the time it was created, ie the same time the Jaz object is 	created.  

