# Fluffy Friend Finder

## Demo
https://furry-friend-finder.krishnanshankar.repl.co/

## Inspiration
We were inspired to create Fluffy Friend Finder after conducting research regarding overcrowded pounds which revealed how too many animals that enter shelters are euthanized. Research conducted by the ASPCA found that approximately 1.5 million animals are euthanized annually, while 6 to 8 million animals continue entering pounds annually. Within pounds, dogs and cats face harsh treatment. We wanted to try and do our part to help save the lives of our fluffy friends by connecting rescued dogs, cats, and rabbits to families that will welcome and give them a loving home.

## What it does
The Fluffy Friend Finder is a simple website that allows users to enter in the different traits which they would like to see in a companion (size, age, etc.) and connects them with rescued animal in a pound which meets those preferences. Since owning a fluffy companion many be a new experience for many families, the Fluffy Friend Finder also has a helpful map which provides people with the ability to easily find pet stores near them. It also includes information about timings and services provided by the store. Important tips for how to take care of a pet are also given.

## How we built it
Fluffy Friend Finder was built using Python, specifically the PetPy and Flask libraries. Flask is a web framework that allows for rapid development. PetPy is a API wrapper for the Petfinder API by Purina that allows developers to access the Petfinder database of animals that are ready for adoption. PetPy allowed for sorting of animals based on given traits, so we connected a frontend form with the sorting of PetPy to return all animals a person would be interested in. For the map that returned the location of all nearby pet stores, we used Folium, a Python library that allows for the rapid development of interactive HTML maps. We then embedded the map's HTML into a iframe to display.

## Challenges we ran into
One of the main challenges we really ran into was styling the website so that it appeared user friendly and presentable. It took time to research and find the right color themes and how to properly use CSS to our needs since we were new to frontend work. It also took some time to figure out exactly how to determine the users location when trying to find nearby pet stores.

## Accomplishments that we're proud of
We are really proud of the evolution of our frontend, as stated before, frontend development was a weak point for us. The frontend of Fluffy Friend Finder saw many changes as we made adjustments and tweaked many things to ensure a pleasurable user experience. Our frontend took the most time and effort and we take extreme pride in the final outcome. 

## What we learned
We learned a lot of HTML and CSS styling and also how to properly use the power of Flask and Jinja for our templates. Working with Folium was also a new experience which proved to be very easy as the library is very intuitive to use.

## What's next for Fluffy Friend Finder
What's next for Fluffy Friend Finder is to continue helping people get connected to animals in need of a home and providing people with the ability to help volunteer to help animals if they are unable to adopt one. We can build a forum where pounds and other animal facilities can request the help of volunteers to help keep animals safe.
