# Space Project
## A simple data engineering project

<img src="https://img.shields.io/badge/Language-Python-yellow"> <img src="https://img.shields.io/badge/Postgres-blue"> <img src="https://img.shields.io/badge/Prefect-gray"> <img src="https://img.shields.io/badge/-Docker-9cf">
<img src = "https://img.shields.io/badge/Data%20Modeling-blue"> <img src = "https://img.shields.io/badge/Data%20Engineering-red"> 

<p align="center"><img src= "https://user-images.githubusercontent.com/92702848/217097355-658b747d-039e-440f-8930-83e8d5d2abc8.jpg"></p>

# Briefing

The primary goal of this project was to develop a simple, but efficient, data engineering structure by combining personal interests with data processing tools. The chosen theme was outer space, focusing on the following topics:

- Crew members currently aboard the International Space Station (ISS).
- Periodic tracking of the ISS location.
- Recording solar flares (Flares) that have impacted Earth.
- Identifying Near Earth Objects (NEOs) close to Earth.



## Data Sources
The data was collected through the following APIs:

- [ISS Location and Crew Information](http://api.open-notify.org/)

- [NEOs (Near Earth Objects)](https://www.neowsapp.com/swagger-ui/index.html)

- [Solar Flares | Nasa DONKI](https://api.nasa.gov/)



**NOTE**: Since the NASA API requires an API key, sensitive configurations were stored in a .env file, which was excluded from the repository for security reasons.

## Development Process
**Step 1:** Prototyping with Jupyter Notebook
The project began with Jupyter Notebook as the initial environment for developing and testing the Python classes used for data consumption. This allowed for rapid prototyping, debugging, and testing of API connections and data handling.

**Step 2:** Object-Oriented Programming (OOP)
The development transitioned to a more modular and scalable approach using Object-Oriented Programming (OOP).

Versatility: The OOP structure provided flexibility for extending functionality or adding new APIs.
Modularization: Each class encapsulates specific logic related to API consumption, making the codebase cleaner and easier to maintain.

## Technologies and Tools Used

### Programming Language

Python served as the backbone of this project, utilized for:

API connections using the **requests** library.
Data processing and manipulation with **pandas**.
Retry management and fault tolerance using the **tenacity** library to ensure robust API data collection.

The tenacity library was instrumental in implementing automated, controlled retry attempts for API connections in case of temporary failures. Its integration with **Prefect** further enhanced the resilience of the data ingestion process, ensuring reliability even under unstable conditions.

### Orchestration
The Prefect orchestration tool was chosen for scheduling and managing data workflows.

* Modern and robust: Prefect stands out for its modern architecture, providing an efficient solution for pipeline governance and control.

* User-friendly configuration: Compared to Airflow, Prefect offers a simpler and more intuitive setup, making the development and monitoring of workflows more accessible.

* Seamless Python Integration: Prefect’s compatibility with libraries like tenacity strengthens the workflow’s ability to handle external API failures gracefully.

**Summary:** Prefect was used as the primary scheduler, offering governance, monitoring, and enhanced reliability for the implemented data flows.

### Database 

The collected data was stored in a **PostgreSQL** database configured within **Docker**, ensuring portability and simplified management / isolated and consistent environment.

# Directory Structure Overview

### Components
In this directory, each script is responsible for handling data processing related to its specific API. The logic for interacting with and processing the data from the APIs is encapsulated in each script, following Object-Oriented Programming (OOP) principles. The only exception is data_sender.py, which primarily consists of functions for sending the processed data to the appropriate destination, rather than using OOP.

**flares.py, iss.py, and neos.py** each contain classes that manage API connections, data retrieval, and processing in an OOP approach, ensuring modularity and reusability of the code.

In essence, the scripts focus on organizing the data handling and API interactions, with a consistent OOP structure, except for data_sender.py, which is more function-based.

### Prefect_Scheduler
Scripts responsible for orchestrating and scheduling data pipelines using **Prefect and Tenacity**, ensuring resilience and efficiency in API consumption.

- flares_data.py

Schedule and manage the collection of solar flare data from the NASA DONKI API.

- iss_crew.py

Orchestrate the consumption of information about the ISS crew using the Open Notify API.

- iss_position.py

Periodically collect the location of the ISS, ensuring up-to-date latitude and longitude data.

- neos_data.py

Manage the consumption of data on Near Earth Objects (NEOs) using the NEOWS API.


