# Chasing the ISS! (And streaming data)

<img src="https://img.shields.io/badge/Status-Under%20Development-yellowgreen"> <img src="https://img.shields.io/badge/Language-Python-yellow"> <img src="https://img.shields.io/badge/DBMS%20-PostgreSQL-informational"> <img src="https://img.shields.io/badge/-Kafka-white"> <img src="https://img.shields.io/badge/-Docker-9cf">

<p align="center"><img src= "https://user-images.githubusercontent.com/92702848/217097355-658b747d-039e-440f-8930-83e8d5d2abc8.jpg"></p>

<p align="center">"Ground Control to Major Tom..."</p>


# 🌌 Briefing

Initially, I thought about ways to start a space trip, but I wasn't sure where to start, so I built a rocket using components that could take me to the ISS.

Jokes aside, the idea of monitoring the ISS seemed like an excellent starting point for the project, both because of the information we have about it and the fact that it is relatively simple to access through the use of APIs. Our goal is to monitor its trajectory around the Earth, which is blue!

The project was based on Object-Oriented Programming, with the aim of providing robustness to the codes and modularizing our objectives, aiming for greater scalability in the future, in case we also want to monitor other space objects that may be valid within the scope of this project.

The "Components" file received this name precisely because it alludes to the components of a rocket, but you will notice that when accessing it, we will see other information closer to "locations" than to a propeller or fuselage.

Beyond creating objects capable of providing information about the ISS and ourselves in relation to the Earth, it is also important to capture and structure this information for future studies, applying, perhaps, Data Science concepts. For this, I created an architecture in Docker, containing a Postgres database so that we can transmit the data to DB.

(Note: You can consult the docker-compose through Docker_configurations, where we also have the JSON used to configure the connector.)


# :rocket: APIs

 - Open Notify - International Space Station Current Location: http://open-notify.org/Open-Notify-API/ISS-Location-Now/  

# :telescope: POO - Components

 - `My_Location:` get informations about my current position (latitude, longitude and also my city - through the IP).
 - `InternationalSpaceStation:` return informations about the API status, current latitude, longitude and about the astronauts.
 - `Astrolabe:` using the inheritance concept, here, we can chase the ISS with the compass, current country of ISS, and the distance between me and the astronauts. At this point its important to highlight that the distance use the haversine formula, which considers the non-euclidean geometry of the Earth, that's return the distance more accurately.
 - `Image Of Day:` here we can access the NASA's image of the day, if you want you can access it with your personal API key, but if you don't have any key, don't worry, there's a DEMO key (with some requests limits).
 - `IssDataStreaming:` also using the inheritance, here we can start our streaming and send data to Postgres.

# :space_invader:	Data Architecture - Engineering

Our Python file responsible for data streaming is configured using the "psycopg2" library to send the data to the database, feeding the "iss_monitoring" table. So far, as it satisfies the project scope, I haven't tought any substantial changes in the query, but we can consider future scalability if it is necessary to adapt for other satellites/celestial bodies that feed another database and, consequently, tables.

(Note: The configurations adopted follow a very simple pattern that satisfies our studies. For a higher level of security, it is up to the user to configure Postgres in our docker-compose file, bearing in mind that the image used already brings a Debezium extension.)

<p align="center">
  <img src="https://github.com/LeifrEiriksson/chasing_the_iss/assets/92702848/882c2a7f-7dce-4634-a4c7-e3bc638b6dca">
</p>


