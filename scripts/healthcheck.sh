#!/bin/sh
set -e

nc -z -w5 localhost 11434 || exit 1
