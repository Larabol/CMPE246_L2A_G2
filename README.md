# CMPE246_L2A_G2

This repository contains the design, development, and implementation of a team-based embedded systems project for CMPE 246 Computer Engineering Design Studio.
The project focuses on building an open-source Battery Management System (BMS) using the Raspberry Pi 4 Model, integrating hardware, software, and machine learning into a web-connected embedded system.

This repository serves as:

- A complete record of the system design and implementation
- An open-source framework for custom battery management systems
- Documentation for hardware, software, and integration
- A professional portfolio showcasing embedded systems, IoT, and software development

This project develops a custom battery management system for lithium-ion battery packs, designed to:
- Monitor individual cell voltages and temperature
- Perform cell balancing for safe operation
- Estimate State of Charge (SOC) and State of Health (SOH)
- Provide real-time battery data through a web-based dashboard
- Enable remote monitoring over a local network

Instead of relying on physical displays, all system data is processed on the Raspberry Pi and served to users through a browser-based interface.


The system is divided into three layers:

1. Hardware Layer
- Lithium-ion battery pack
- Custom BMS PCB with monitoring ICs
- Voltage and temperature sensing
2. Embedded Processing Layer
- Raspberry Pi running C++ control software
- Communication via I2C and GPIO
- Data processing and system control
3. Application Layer
- Web server and API
- Database for logging battery data
- Browser-based dashboard for visualization

Key Features:

- Embedded System Integration: Raspberry Pi interfacing with battery management hardware via I2C, real-time data acquisition and control
Custom Hardware Design

- PCB-based battery management system: Support for 5-cell 18650 lithium-ion battery pack, integrated sensing and communication circuitry

- Machine Learning Integration: SOC/SOH estimation using XGBoost, data-driven battery analysis

- IoT Functionality: Local network access through a web server, modular and scalable system design

- Web-Based Monitoring Interface: Real-time battery data visualization through a browser-based dashboard using FastAPI and Grafana, enables remote monitoring and logging of voltage, temperature, and battery metrics over a local network
