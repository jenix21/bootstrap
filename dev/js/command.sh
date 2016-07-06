#!/usr/bin/env bash

## yeoman
npm install -g generator-angular # angular generator install

yo angular # scaffolding
grunt # build
grunt server # run local server

# sass
sass --watch style.scss:style.css # file
sass --watch stylesheets/sass:stylesheets/compiled # directory
