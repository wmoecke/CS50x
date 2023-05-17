# BINARY CLOCK
#### Video Demo:  https://youtu.be/XgMZY_GMnu4
#### Description:
A Chrome extension that displays a skinnable binary clock on your web browser.
First things first, you need to install this extension in your Chrome web browser:
1. Open Chrome menu
2. Go to _More Tools_ > _Extensions_
3. Click the _Load Unpacked_ button (Developer options must be enabled)


Once the extension is installed, simply click the extension button to toggle the clock's visibility.
Right-clicking the extension button and selecting "Options" from the context menu gives you access to the settings page. From there, you can select from the various skin presets I've made available. You can also change the overall size of the clock, from the settings page.


This extension was entirely coded in HTML/CSS/Javascript, by Werner Moecke (São Paulo, SP, Brazil).
The project comprises 2 .js files, 1 .css file and 2 .html files. The respective names for the .html and .js files give a good hint on what they're there for (e.g., _options_[.js | .html]). That being said, the `index.html` file along with `binary_clock.js` form the code for the main application.


The `options.js` file contains code respective to the `options.html` page. Two functions are present:
- `saveOptions()`: this function is triggered by the _Save_ button, on the options page. It sets the necessary variables in the local storage for the 2 settings (_skin_ and _size_) and provides visual feedback to the user about the save state.
- `restoreOptions()`: this function is triggered by the `DOMContentLoaded` event, which is to say, it is called when the entire DOM is loaded on the options page. It then adds an event listener to the _Save_ button's `click` event, in order to fire the `saveOptions()` function every time this button is clicked. It also reads the variables from the local storage in order to set the values for the 2 list boxes with the ones from local storage.


The `binary_clock.js` file as mentioned before, contains code respective to the main application. It is responsible for all the functionalities that the clock offers. Below is a summary of its functions:
- `startUp()`: After the DOM has been completely loaded (`DOMContentLoaded` event), this function calls `renderBackground()` and starts a 1000ms interval timer that reads the current time as a string formatted to `HHmmss` via a RegExp. After that, it calls `processDots()` passing _time_ as an argument.
- `processDots(time)`: It begins by getting a collection of nodes comprising all divs with ids starting with _dot_ (those are the dots that will be processed). Then, for each dot, it converts the time digit indexed by the dot's id's first of 2 digits from the time string (char array) to binary. After that, it determines if this dot is set by extracting the binary digit from the previously converted time part (indexed by the second of the dot's id's 2 digits). Finally, it calls `renderDot()` passing the _dot_ div and the _bit_ (set or unset) as arguments. This concludes getting the current time converted to binary and setting the bits for every dot.
- `renderDot(dot, bit)`: The main body of this function is about styling the dots according to the skin selected in the options page, as it can be seen in the `switch` statement. So reading the `skin` variable from the local storage and further deciding what CSS property (or properties) to apply to a dot according to the skin and bit (1 or 0) is all this function is about.
- `renderBackground()`: As previously mentioned, this is a one-time call function, which renders the `#container` div, according to the skin and size selected in the options page. It complements the `renderDot()` function, by setting the CSS properties for the container.
- `convertToBinary(decimal)`: This function is responsible for converting a decimal number to binary. It performs a series of bitwise operations to achieve that. Ultimately, it returns a string padded with zeroes in order to form a consistent 6-digit binary string.


That is all there is to know about this project. If you wish to get in touch with me, write an e-mail to: wmoecke@gmail.com.
