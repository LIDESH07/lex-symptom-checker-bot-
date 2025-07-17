def lambda_handler(event, context):
    intent_name = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent'].get('slots', {})

    # Helper function to safely extract slot values
    def get_slot_value(slot_name):
        slot = slots.get(slot_name)
        if slot and 'value' in slot:
            return slot['value'].get('interpretedValue')
        return None

    # ✅ GREETING INTENT – Route to HealthSymptomChecker
    if intent_name == "GreetingIntent":
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": "Symptom"
                },
                "intent": {
                    "name": "HealthSymptomChecker",
                    "state": "InProgress",
                    "slots": {
                        "Symptom": None,
                        "Duration": None,
                        "Severity": None,
                        "Action": None
                    }
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Hi! I'm your virtual health assistant. Let's get started — what symptom are you experiencing?"
                }
            ]
        }

    # ✅ HEALTH SYMPTOM CHECKER INTENT
    if intent_name == "HealthSymptomChecker":
        Symptom = get_slot_value('Symptom')
        Duration = get_slot_value('Duration')
        Severity = get_slot_value('Severity')
        Action = get_slot_value('Action')

        # If required slots are still missing, let Lex continue slot elicitation
        if not all([Symptom, Duration, Severity]):
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": (
                            "Symptom" if not Symptom else
                            "Duration" if not Duration else
                            "Severity"
                        )
                    },
                    "intent": {
                        "name": intent_name,
                        "state": "InProgress",
                        "slots": {
                            "Symptom": {"value": {"interpretedValue": Symptom}} if Symptom else None,
                            "Duration": {"value": {"interpretedValue": Duration}} if Duration else None,
                            "Severity": {"value": {"interpretedValue": Severity}} if Severity else None,
                            "Action": {"value": {"interpretedValue": Action}} if Action else None,
                        }
                    }
                },
                "messages": []
            }

        # Generate response advice based on severity
        Symptom = Symptom.lower()
        Severity = Severity.lower()
        Duration = Duration.lower()

        if Severity == "severe":
            advice = f"Since your {Symptom} has been severe for {Duration}, I recommend seeking immediate medical attention."
        elif Severity == "moderate":
            advice = f"A moderate {Symptom} for {Duration} should be monitored. If it worsens, consider seeing a doctor."
        else:
            advice = f"A mild {Symptom} lasting {Duration} may resolve with rest, hydration, and home care."

        # Action response
        action_response = ""
        if Action:
            Action = Action.lower()
            if "book" in Action:
                action_response = "I can help you book a doctor appointment."
            elif "talk" in Action:
                action_response = "I can connect you to a medical expert shortly."
            elif "schedule" in Action:
                action_response = "Scheduling a consultation now."

        final_message = f"{advice} {action_response}".strip()

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent_name,
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": final_message
                }
            ]
        }

    # ❓ Fallback if unknown intent
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": intent_name,
                "state": "Failed"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "I'm not sure how to help with that. Please try again."
            }
        ]
    }