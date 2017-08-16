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

function add_lambda_policies {
  echo "Adding lambda policy 2 for set_office_hours..."
  aws lambda add-permission \
    --region us-east-1 \
    --function-name set_office_hours \
    --statement-id 2 \
    --principal lex.amazonaws.com \
    --action lambda:InvokeFunction \
    --source-arn arn:aws:lex:us-east-1:${AWSACCT}:intent:AddDiscusionTopicOfficeHours:*
  echo "Adding lambda policy 3 for set_office_hours..."
  aws lambda add-permission \
    --region us-east-1 \
    --function-name set_office_hours \
    --statement-id 3 \
    --principal lex.amazonaws.com \
    --action lambda:InvokeFunction \
    --source-arn arn:aws:lex:us-east-1:${AWSACCT}:intent:SetTodaysOfficeHours:*
  echo "Adding lambda policy 1 for add_discussion_topic..."
  aws lambda add-permission \
    --region us-east-1 \
    --function-name add_discussion_topic \
    --statement-id 1 \
    --principal lex.amazonaws.com \
    --action lambda:InvokeFunction \
    --source-arn arn:aws:lex:us-east-1:${AWSACCT}:intent:AddDiscusionTopicOfficeHours:*
  echo "Adding lambda policy 1 for get_office_hours..."
  aws lambda add-permission \
    --region us-east-1 \
    --function-name get_office_hours \
    --statement-id 1 \
    --principal lex.amazonaws.com \
    --action lambda:InvokeFunction \
    --source-arn arn:aws:lex:us-east-1:${AWSACCT}:intent:AddDiscusionTopicOfficeHours:*
  echo "Adding lambda policy 2 for get_office_hours..."
  aws lambda add-permission \
    --region us-east-1 \
    --function-name get_office_hours \
    --statement-id 2 \
    --principal lex.amazonaws.com \
    --action lambda:InvokeFunction \
    --source-arn arn:aws:lex:us-east-1:${AWSACCT}:intent:GetTeamsOfficeHours:*
  echo "Adding lambda policy 1 for lookup_discussion_topics..."
  aws lambda add-permission \
    --region us-east-1 \
    --function-name lookup_discussion_topics \
    --statement-id 1 \
    --principal lex.amazonaws.com \
    --action lambda:InvokeFunction \
    --source-arn arn:aws:lex:us-east-1:${AWSACCT}:intent:AddDiscusionTopicOfficeHours:*
  echo "Adding lambda policy 2 for lookup_discussion_topics..."
  aws lambda add-permission \
    --region us-east-1 \
    --function-name lookup_discussion_topics \
    --statement-id 2 \
    --principal lex.amazonaws.com \
    --action lambda:InvokeFunction \
    --source-arn arn:aws:lex:us-east-1:${AWSACCT}:intent:LookupDiscussionTopics:*
}

function put_slots {
  echo "Deploying slot GetDiscussionTopic..."
  aws lex-models put-slot-type \
    --name GetDiscussionTopic \
    --cli-input-json file://_build_lex/put-slot-type-GetDiscussionTopic.json \
    --region us-east-1 \
    --checksum ""
  echo "Deploying slot OfficeHoursLocation..."
  aws lex-models put-slot-type \
    --name OfficeHoursLocation \
    --cli-input-json file://_build_lex/put-slot-type-OfficeHoursLocation.json \
    --region us-east-1 \
    --checksum ""
  echo "Deploying slot SetTeam..."
  aws lex-models put-slot-type \
    --name SetTeam \
    --cli-input-json file://_build_lex/put-slot-type-SetTeam.json \
    --region us-east-1 \
    --checksum ""
}

function put_intents {
  echo "Deploying intent AddDiscussionTopicOfficeHours..."
  aws lex-models put-intent \
    --name AddDiscusionTopicOfficeHours \
    --cli-input-json file://_build_lex/put-intent-AddDiscussionTopicOfficeHours.json \
    --region us-east-1 \
    --checksum ""
  echo "Deploying intent GetTeamsOfficeHours..."
  aws lex-models put-intent \
    --name GetTeamsOfficeHours \
    --cli-input-json file://_build_lex/put-intent-GetTeamsOfficeHours.json \
    --region us-east-1 \
    --checksum ""
  echo "Deploying intent LookUpDiscussionTopic..."
  aws lex-models put-intent \
    --name LookupDiscussionTopics \
    --cli-input-json file://_build_lex/put-intent-LookupDiscussionTopic.json \
    --region us-east-1 \
    --checksum ""
  echo "Deploying intent SetTodaysOfficeHours..."
  aws lex-models put-intent \
    --name SetTodaysOfficeHours \
    --cli-input-json file://_build_lex/put-intent-SetTodaysOfficeHours.json \
    --region us-east-1 \
    --checksum ""
}

function put_bot {
  aws lex-models put-bot \
    --name OfficeHoursBot \
    --cli-input-json file://_build_lex/put-bot.json \
    --region us-east-1 \
    --checksum ""
}

function main {
  #add_lambda_policies
  prep_build
  swap_in_account_number
  put_slots
  put_intents
  put_bot
}

main
