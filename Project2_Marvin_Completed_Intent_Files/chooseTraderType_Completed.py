### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json


### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response


def validate_data(trader_type, intent_request):
    # Validate the indicator selected
    if trader_type is not None:
        list_traders = ["intraday", "swing", "fundamental", "momentum"]
        if trader_type.lower() not in list_traders:
            return build_validation_result(
                False,
                "typeTrader",
                "Currently, we only provide information regarding these trader types: intraday, swing, fundamental, momentum. "
                "Please select one.",
            )
            
    return build_validation_result(True, None, None)

def get_trader(trader_type):
    # Determine the indicator chosen
    if trader_type.lower() == "intraday":
        trader_chosen = "As an intraday trader, you will actively enter positions throughout the day and close all positions by the end of day."
    elif trader_type.lower() == "swing":
        trader_chosen = "As a swing trader, you will enter into positions and look to close them out within 1-10 days."
    elif trader_type.lower() == "fundamental":
        trader_chosen = "As a fundamental trader, you will look to trade based off of analyst reports, company earnings, or news in general. "
    elif trader_type.lower() == "momentum":
        trader_chosen = "As a momentum trader, you will look to enter and exit positions based on various technical indicators. The goal is to profit off of short-term price volatility. "
    else:
        trader_chosen = "Invalid Type of Trader"
    return trader_chosen



### Intents Handlers ###

def typeOfTrader(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    # Get slot values
    trader_type = get_slots(intent_request)["typeTrader"]
    source = intent_request["invocationSource"]

    # Validate user input
    if source == "DialogCodeHook":
        slots = get_slots(intent_request)

        # Validate age
        validation_result = validate_data(trader_type, intent_request)
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Clear invalid slot
            
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )
        
        output_session_attributes = intent_request["sessionAttributes"]
        
        return delegate(output_session_attributes, get_slots(intent_request))
    

    trader_chosen = get_trader(trader_type)
    
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """{}"""
            .format(trader_chosen),
        },
    )
    


### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "typeOfTrader":
        return typeOfTrader(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")



### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)