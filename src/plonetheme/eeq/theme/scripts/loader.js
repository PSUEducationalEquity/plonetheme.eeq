requirejs.config({
    "paths" : {
        "eeq-scripts": "++theme++psu-educational-equity/build/eeq-scripts.min"
    },
    "shim" : {
        "eeq-scripts" : ["jquery"]
    }
});

require(["eeq-scripts"], function (scripts) {
    // load up our primary js via require
});
