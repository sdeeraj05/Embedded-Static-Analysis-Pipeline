# Embedded-Static-Analysis-Pipeline
A Python-based automation tool designed to execute static code analysis on embedded firmware, parse the raw tool logs, and generate consolidated quality reports for CI/CD pipeline integration.

## Overview
This repository contains a Python-based automation pipeline designed to run static code analysis on embedded C firmware (such as STM32 projects). Developed during a summer internship at Niyata Infotech, this tooling automates code quality checks, rule enforcement, and report parsing, making it ready for seamless integration into modern SDLC workflows and cloud-based CI/CD environments like Microsoft Azure.

## Features
* **Automated Execution:** Scripted execution of static analysis tools against target microcontroller source code.
* **CI/CD Ready:** Structured for easy deployment within automated pipelines (e.g., Azure Pipelines, GitHub Actions).
* **Report Generation:** Automatically parses raw analysis logs and generates consolidated summary reports for developer review.
* **Custom Configuration:** Centralized configuration files to define and manage strict coding standard rules.

## Repository Structure
* `scripts/`: Core Python automation scripts and pipeline triggers.
* `config/`: Configuration files and rule sets for the underlying static analysis tools.
* `tests/`: Unit tests validating the Python automation logic and parsing accuracy.
* `requirements.txt`: Python package dependencies.

## Getting Started
1. Clone this repository.
2. Set up a virtual environment: `python -m venv venv`
3. Activate the environment and install dependencies: `pip install -r requirements.txt`
4. Execute the main pipeline script, passing your target firmware directory as an argument.
