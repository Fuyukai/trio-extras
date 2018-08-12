#!/usr/bin/env bash

py.test --cov=trio_extras --strict -v
codecov
