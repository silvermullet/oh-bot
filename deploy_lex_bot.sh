#!/bin/bash

while getopts "ha:" opt; do
   case $opt in
      h) echo -e $USAGE && exit
      ;;
      a) AWSACCT="$OPTARG"
      ;;
      \?) echo "Invalid option -$OPTARG" >&2 && exit
      ;;
   esac
done

if [[ -z $AWSACCT ]]; then
  echo "Must provide an account for Lambda association, -a option... $AWSACCT"
  exit
fi

function prep_build {
  echo "Prep AWS Lex build..."
  mkdir -p ./_build_lex
  cp lex/full-configuration/*.json _build_lex/
}

function swap_in_account_number {
  echo "Using account number: $AWSACCT"
  sed -i -e "s/REPLACE_ME_ACCT/$AWSACCT/g" _build_lex/*.json
}

function put_slots {
  echo "Deploying slot GetDiscussionTopic..."
  aws lex-models put-slot-type \
    --name GetDiscussionTopic \
    --cli-input-json file://_build_lex/put-slot-type-GetDiscussionTopic.json
  echo "Deploying slot OfficeHoursLocation..."
  aws lex-models put-slot-type \
    --name OfficeHoursLocation \
    --cli-input-json file://_build_lex/put-slot-type-OfficeHoursLocation.json
  echo "Deploying slot SetTeam..."
  aws lex-models put-slot-type \
    --name SetTeam \
    --cli-input-json file://_build_lex/put-slot-type-SetTeam.json
}

function put_intents {
  echo "Deploying intent AddDiscussionTopicOfficeHours..."
  aws lex-models put-intent \
    --name AddDiscusionTopicOfficeHours \
    --cli-input-json file://_build_lex/put-intent-AddDiscussionTopicOfficeHours.json
  echo "Deploying intent GetTeamsOfficeHours..."
  aws lex-models put-intent \
    --name GetTeamsOfficeHours \
    --cli-input-json file://_build_lex/put-intent-GetTeamsOfficeHours.json
  echo "Deploying intent LookUpDiscussionTopic..."
  aws lex-models put-intent \
    --name LookupDiscussionTopics \
    --cli-input-json file://_build_lex/put-intent-LookupDiscussionTopic.json
  echo "Deploying intent SetTodaysOfficeHours..."
  aws lex-models put-intent \
    --name SetTodaysOfficeHours \
    --cli-input-json file://_build_lex/put-intent-SetTodaysOfficeHours.json
}

function main {
  prep_build
  swap_in_account_number
  put_slots
  put_intents
}

main
