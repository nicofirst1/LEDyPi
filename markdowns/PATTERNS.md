Here's a list of available patterns.

# Fixed

### Game of Life

Watch how life evolves with the famous [game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) algorithm.

![gof demo](Resources/gof_demo.gif)

### Water

Simulate the deepness of the ocean.

![water demo](Resources/water_demo.gif)

### Storm

Can be a light rain or a heavy storm, you decide.

![storm demo](Resources/storm.gif)


### Fire

Light up the temperature with some fire.

![water demo](Resources/fire_demo.gif)


# Interactive

### Equation
You can input a custom equation for the rgb values. Such equation can depend on:
- time: a time-step is kept so to evolve the function through time
- index: the position of the led-strip can also be used

For example the following patters is given with:
- red = _cos(t)_
- green = _sin(t)_
- blue = _idx_

![equation demo](Resources/equation_demo.gif)


### Music Reactive (click gif for video)
[![audio demo](Resources/audio_demo2.gif)](https://youtu.be/7PXDBr3uZmA) 

This pattern uses a microphone to visualize the music on your led strip. There are three different type of visualization:
- Spectrum: split the strip on subsequent frequency bands and visualize the amplitude as a mix of rgb values
- Energy: use an energy function to plot the sound on the leds
- Scroll: record the audio amplitude on a scrolling timeline.


### Image
Designing a pattern can become hard and take some time, so why not using a pre-made pattern?

With _Image_ you can use an URL pointing to an image and LedyPi will download it and display it for you.

![image demo](Resources/image_demo.gif)