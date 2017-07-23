<!--
title: Oh-bot (Office Hours Bot)
description: Running office hours can be a great way to divert interrupts a team or individual has on a daily basis. However, managing your office hours and knowing what to expect at schedule office hours can be a challenge. The Oh-bot will help manage your team's office hours. This bot will provide insight into when office hours are available and will gather up expected topics for you. Oh-bot also helps records office hour interactions for future review as well.
layout: Doc
-->
# Oh-bot - Your team's Office Hours Bot

![silvermullet](https://user-images.githubusercontent.com/538171/28157153-44a1ff6e-6751-11e7-8921-25b01367e313.jpeg)

The Oh-bot will help manage your team's office hours.

* Set location and time for office hours on a per-team or individual basis.
* Organizes and records who is intending on joining the team's office hours and what topics will be discussed
* Provide insight into past office hours to help make improvements to services team provides


### Present abilities

Oh-bot is able to...
 1. Set your team's office hours. Just ask to set your team's office hours and it will help out.
 2. Retrieve office hours for a known team (Controlled by the Lex slot SetTeam)
 3. Add discussion topic for a team's office hours for a given day
 4. Lookup office hour discussion topics for a given day

### Video walkthrough

[![Oh-bot](https://user-images.githubusercontent.com/538171/28185584-9e5f9428-67b3-11e7-9768-0056c55dbbb7.png)](https://youtu.be/sJlD_Xq2WbE "Oh-bot video walkthrough")

### Technology stack

[AWS Lex Bot](https://docs.aws.amazon.com/lex/latest/dg/what-is.html) + [Slack](https://slack.com/)

[Serverless.com](https://serverless.com/framework/docs/) framework driven setup

[Python 3.6 AWS Lambda Functions](https://aws.amazon.com/about-aws/whats-new/2017/04/aws-lambda-supports-python-3-6/)

[Dynamodb backend](https://aws.amazon.com/documentation/dynamodb/)

### Setup requirements
 * Install serverless ```npm install serverless```
 * Install serverless-package-python-functions ```npm install --save serverless-package-python-functions```
 * copy local_sample.yml to local.yml and update local.yml to use your Slack bot's auth token
 * Run ```serverless deploy```
 * Review lex/full-configuration/oh-bot.json and import into your AWS with adjusted values for the SetTeam slot values


### Lex configuration overview

#### Intents
 * AddDiscusionTopicOfficeHours
 * GetTeamsOfficeHours
 * LookupDiscussionTopics
 * SetTodaysOfficeHours

#### Slots
 * GetDiscussionTopic
 * SetTeam
 * OfficeHoursLocation

#### Dynamodb tables
 * oh-bot-{environment}
 * oh-bot-{environment}-topics

### Local Development

Initial setup script will download latest DynamoDB local service

```
bash localdev_setup.sh
```

To run local DynamoDB on port 8000

```
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -inMemory
```

* oh-bot logo by [Rebecca Meredith](http://www.rebeccameredith.com/about)
