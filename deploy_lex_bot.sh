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
  echo "Swap in account number provided by -a flag..."
  sed -i -e "s/REPLACE_ME_ACCT/$AWSACCT/g" _build_lex/*.json
}

function put_slots {
  aws lex-models put-slot-type \
    --name GetDiscussionTopic \
    --cli-input-json file://_build_lex/put-slot-type-GetDiscussionTopic.json
  aws lex-models put-slot-type \
    --name OfficeHoursLocation \
    --cli-input-json file://_build_lex/put-slot-type-OfficeHoursLocation.json
  aws lex-models put-slot-type \
    --name SetTeam \
    --cli-input-json file://_build_lex/put-slot-type-SetTeam.json
}

function put_intents {
  aws lex-models put-intent \
    --name AddDiscusionTopicOfficeHours \
    --cli-input-json file://_build_lex/put-intent-AddDiscussionTopicOfficeHours.json
  aws lex-models put-intent \
    --name GetTeamsOfficeHours \
    --cli-input-json file://_build_lex/put-intent-GetTeamsOfficeHours.json
  aws lex-models put-intent \
    --name LookUpDiscussionTopic \
    --cli-input-json file://_build_lex/put-intent-LookUpDiscussionTopic.json
  aws lex-models put-intent \
    --name SetTodaysOfficeHours \
    --cli-input-json file://_build_lex/put-intent-SetTodaysOfficeHours.json
  aws lex-models put-intent \
    --name GetDiscussionTopic \
    --cli-input-json file://_build_lex/put-slot-type-GetDiscussionTopic.json
  aws lex-models put-intent \
    --name OfficeHoursLocation \
    --cli-input-json file://_build_lex/put-slot-type-OfficeHoursLocation.json
}

function main {
  prep_build
  swap_in_account_number
  put_slots
  put_intents
}

main
