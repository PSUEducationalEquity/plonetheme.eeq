# Replace the egg version with our version for the FS compile
cp ../src/plonetheme/eeq/browser/overrides/plone.staticresources.static.plone.js ../parts/omelette/plone/staticresources/static/plone.js

# Compile plone bundle without Bootstrap JS, since we get it from Bootstrap 4
../bin/plone-compile-resources -b plone -s equity --compile-dir . -i ../bin/instance

# Copy files to overrides directory
cp plone.min.js ../src/plonetheme/eeq/browser/overrides/plone.staticresources.static.plone-compiled.min.js
cp plone.min.js.map ../src/plonetheme/eeq/browser/overrides/plone.staticresources.static.plone-compiled.min.js.map
