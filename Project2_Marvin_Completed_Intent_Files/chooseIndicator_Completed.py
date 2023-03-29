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


def validate_data(tech_indicator, intent_request):
    # Validate the indicator selected
    if tech_indicator is not None:
        list_indicators = ["sma", "ema", "vwap", "rsi", "macd"]
        if tech_indicator.lower() not in list_indicators:
            return build_validation_result(
                False,
                "indicatorSelected",
                "Currently, we only support the following technical indicators: sma, ema, vwap, rsi, macd. "
                "Please select one.",
            )
            
    return build_validation_result(True, None, None)

def get_tech(tech_indicator):
    # Determine the indicator chosen
    if tech_indicator.lower() == "sma":
        indicator_chosen = "You have selected the simple moving average. Here's a link to learn more: https://www.investopedia.com/terms/s/sma.asp"
    elif tech_indicator.lower() == "ema":
        indicator_chosen = "You have selected the exponential moving average. Here's a link to learn more: https://www.investopedia.com/terms/e/ema.asp"
    elif tech_indicator.lower() == "rsi":
        indicator_chosen = "You have selected the RSI indicator (relative strength index). Here's a link to learn more: https://www.investopedia.com/terms/r/rsi.asp"
    elif tech_indicator.lower() == "macd":
        indicator_chosen = "You have selected the MACD indicator (moving average convergence divergence). Here's a link to learn more: https://www.investopedia.com/terms/m/macd.asp"
    elif tech_indicator.lower() == "vwap":
        indicator_chosen = "You have selected the VWAP indicator (volume weight average price). Here's a link to learn more: https://www.investopedia.com/terms/v/vwap.asp"
    else:
        indicator_chosen = "Invalid Technical Indicator"
    return indicator_chosen



### Intents Handlers ###

def chooseIndicator(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    # Get slot values
    tech_indicator = get_slots(intent_request)["indicatorSelected"]
    source = intent_request["invocationSource"]

    # Validate user input
    if source == "DialogCodeHook":
        slots = get_slots(intent_request)

        # Validate age
        validation_result = validate_data(tech_indicator, intent_request)
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
    

    indicator_chosen = get_tech(tech_indicator)
    
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """{}"""
            .format(indicator_chosen),
        },
    )
    


### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "chooseIndicator":
        return chooseIndicator(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")



### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)