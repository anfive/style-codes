# The Servizio Web App

The Servizio web app is a convenient tool for Style Judges to rate duels. The app computes the style score (and the encoding Style Code) for both athletes on the fly. It also provides a Decode function to decode Style Codes.

The app can be found at [servizio.ludosportincom.org](https://servizio.ludosportincom.org) and it works with the major browsers. See below for browser support.

The app is an evolution of the Android app [Servizio](servizio-app.md). The app was developed by Alessandro Luppi.

### Installing the app

The app can be installed on an Android, iPhone, and on Windows from the browser (using the Progressive Web Apps technology). It is recommended to install the app for better usability.

To install the app on your device:

**Android**:

- Open [servizio.ludosportincom.org](https://servizio.ludosportincom.org) using Google Chrome.
- From the menu (three dots at the top right), tap "Add to Home".

The app can be installed similarly using Firefox.

**iPhone**:

- Open [servizio.ludosportincom.org](https://servizio.ludosportincom.org) using Safari.
- Tap "Share".
- Scroll down and tap "Add to Home Screen".

**Windows**

- Open [servizio.ludosportincom.org](https://servizio.ludosportincom.org) using Chrome or Edge.
- Click on the "Install" button that appears at the right of the address bar (it might take a few seconds).

### How to use the app

The main interface of the app is represented in the picture below.

![Main interface](images/webapp/servizio-0.png)

The interface can be used to rate both athletes in a duel at the same time. The left part of the interface refers to the first athlete, while the right part refers to the second athlete.

Pressing the buttons marked with a **+** sign adds a point in the corresponding category for the corresponding athlete. The Style score and Style Code is automatically updated when a point is added.

The first 8 categories (all except `PEN`) have a minimum value of 0 and a maximum value of 3. Pressing the corresponding **+** button again when the value is 3 will reset the value to zero.

The `PEN` category has a maximum value of 20, which also wraps back to zero. To reset the `PEN` value to zero quickly, long-press (hold) the corresponding **+** button for a few seconds.

Long-press (hold) the `RESET` button for a few seconds to reset *all* values to zero for both athletes.

Press the `DECODE` button to enter Decode mode.

### Decode mode

Decode mode allows decoding a Style Code into the original judgement (combination of points in the 9 categories). Enter the alphanumeric code in the text field to decode it automatically, if it corresponds to a valid style code.

Press the `CLEAR` button to clear the entered Style Code. Press the *back* button on your device to return to the main interface.

![Decode mode](images/webapp/servizio-1.png)

### Browser support

The app has been tested with updated versions of the browsers below. It might still work with untested browsers.

Windows:
- Mozilla Firefox
- Google Chrome
- Microsoft Edge

Android
- Mozilla Firefox
- Google Chrome
- Microsoft Edge

iPhone:
- Safari
- Google Chrome

The app has been reported to **not** work correctly with Mi browser.