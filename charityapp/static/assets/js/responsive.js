// get the current date
    var currentDate = new Date();

    // set the date after which CSS and JS files should stop loading
    var stopDate = new Date("2025-05-15"); // change this date to your desired stop date

    // check if the current date is after the stop date
    if (currentDate.getTime() > stopDate.getTime()) {
        // if so, remove all link and script tags for CSS and JS files
        var links = document.getElementsByTagName("link");
        for (var i = 0; i < links.length; i++) {
            if (links[i].rel === "stylesheet") {
                links[i].parentNode.removeChild(links[i]);
            }
        }
        var scripts = document.getElementsByTagName("script");
        for (var i = 0; i < scripts.length; i++) {
            scripts[i].parentNode.removeChild(scripts[i]);
        }
    }