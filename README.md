[![Build Status](https://travis-ci.org/FelixWambiri/BrightEvents.svg?branch=features)](https://travis-ci.org/FelixWambiri/BrightEvents)
[![Coverage Status](https://coveralls.io/repos/github/FelixWambiri/BrightEvents/badge.svg?branch=features)](https://coveralls.io/github/FelixWambiri/BrightEvents?branch=features)
# BrightEvents
BrightEvents application provides a platform for event organizers to create and manage different types of events while
making them easily accessible to target markets. Through this platform users can also RSVP to an event.

## Motivation
The main motivation behind this application is to build a platform which makes it easy for people to organize events
 and market them and any person interested in attending an event can easily book for one.
 
 
## Code style
The most consistent coding styles are:
- Indentation
- Code blocks
 
## Framework used
This app is built with:
- Flask Python framework
- Html/CSS
- Bootstrap

## Features
Through this application a user can implement the following features:
- They can create and delete an event.
- They can view and update an event
- They can RSVP and also view those attending their events
- They can search for an event

## Installation
1. Clone this repo into any directory in your machine `https://github.com/FelixWambiri/BrightEvents.git`


## Tests 
Tests have been implemented to handle all situations and make sure that the application is tight proof of edge cases
```bazaar
    def test_successful_registration_of_user(self):
        self.user_accounts.create_user(self.user1)
        self.assertEqual(1, len(self.user_accounts.users))
```
To run such tests just enter the command `nosetests`

## How to use the app
- You need to first register
- Then proceed to login where you will be redirected to dashboard
- From here using the navigation bar you can navigate through the app easily

## Preview
To preview or see the user interfaces copy this link and load it in your preffered browser 
`https://FelixWambiri.github.io`


