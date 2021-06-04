requirejs.config({
    "paths" : {
        "bootstrap": "https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.bundle.min",
        "main": "++theme++psu-educational-equity/build/main.min"
    },
    "shim" : {
        "bootstrap" : ["jquery"]
    }
});

require(["bootstrap", "main"], function (bootstrap, main) {
    // load up our primary js via require
});
