<!--
title: Oh-bot (Office Hours Bot)
description: The Oh-bot will help manage your team's office hours, by facilitating what people will be bringing to your office hours daily to work on. Oh-bot also helps records office hour interactions for future review.
layout: Doc
-->
# Oh-bot - Your team's Office Hours Bot

The Oh-bot will help manage your team's office hours.

* Set location and time for office hours
* Organizes and records who is intending to join the team's office hours and what topics will be discussed
* Provide insight into past office hours to help make improvements to services team provides

Serverless framework driven setup

### Present abilities

Oh-bot is able to...
 1. Set your team's office hours. Just ask to set your team's office hours and it will help out.
 2. Retrieve office hours for a known team 

### Local Development

Initial setup script will download latest DynamoDB local service

```
bash localdev_setup.sh
```

To run local DynamoDB on port 8000

```
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -inMemory
```
