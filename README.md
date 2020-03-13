# Model Discussion

## Home system


## Photovoltaic system
The model is based in solar radiation data obtained from:
https://re.jrc.ec.europa.eu/pvg_tools/en/tools.html#DR

The data can be found in the file radiation_data.csv.
The curve is affected by weather conditions, reader geolocation and time of the year.
Since no data about those variables has been provided, a random location and date has been choosen.
Since the platform only provides one measurement per hour, a polynomial of order three has been fitted to the data in order to obtain a continuous function.
Then the values have been scaled to obtain a maximum value of 3.25, similar to the maximum power value of the given graph.

It is understood that the two slope functions, before and after the "bell", represent a time of the day when either there is no direct sun incident on the cells or part of the installation is cover with shadows.
These shadows might been cast by nearby objects, or the system itself, and due to the sun position.
In order to reproduce these lines, an educated guess has been taken to set the time when system is under "direct" sunlight and when there is no sunlight.

We can say that in our model, there is sunlight between 5.30 and 17.00 and the system is under direct sunlight from 7.15 until 15.40.

The given example shows some noise all over the curve, and accentuated between 12.00 and 16.00. It is understood that this noise can be caused by multiple things, such as clouds passing by.
To reproduce this noise...

## Model improvements
The model has been based on little data obtained for a photovoltaic system with two axis mounted type. 
Having a different mounted type might produce those slopes that were created artificially.
Also, having the date and the geolocation of the reader, the actual times of sunrise, down and sunlight could have been found.
More data points would also help improving the model.