### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

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


def validate_data(age, investment_amount, risk_level, investment_term, intent_request):
    # Validate age input
    if age is not None:
        age = parse_int(age)
        if age <= 18 or age >= 65:
            return build_validation_result(
                False,
                "age",
                "Your age should be greater than 18 and less than 65. "
                "Please provide a valid age.",
            )

    # Validate investment amount input
    if investment_amount is not None:
        investment_amount = parse_int(investment_amount)
        if investment_amount < 10000:
            return build_validation_result(
                False,
                "investmentAmount",
                "The minimum investment amount is $10000. "
                "Please provide a valid investment amount.",
            )

    # Validate risk level input
    if risk_level is not None:
        risk_levels = ["none", "low", "medium", "high"]
        if risk_level.lower() not in risk_levels:
            return build_validation_result(
                False,
                "riskLevel",
                "Your risk level should be one of the following options: none, low, medium, high. "
                "Please provide a valid risk level.",
            )
            
    # Validate the time horizon input
    if investment_term is not None:
        investment_terms = ["short", "medium", "long"]
        if investment_term.lower() not in investment_terms:
            return build_validation_result(
                False,
                "timeHorizon",
                "Your time horizon should be one of the following options: short, medium, long. "
                "Please provide a valid investment time horizon.",
            )

    return build_validation_result(True, None, None)

def get_rec(risk_level):
    # Determine recommended portfolio
    if risk_level.lower() == "none":
        portfolio_recommendation = "We recommend investing 100% of your portfolio in U.S. investment-grade bonds through the iShares Core U.S. Aggregate Bond ETF (AGG) or in U.S. Treasury bonds."
    elif risk_level.lower() == "low":
        portfolio_recommendation = "We recommend investing in the S&P 500 index through the ETF 'SPY'."
    elif risk_level.lower() == "medium":
        portfolio_recommendation = "We recommend allocating capital into individual mid-cap and large-cap stocks such as AAPL or ROKU. These stocks provide a balance of growth and stability."
    elif risk_level.lower() == "high":
        portfolio_recommendation = "We recommend diversification into more volatile sectors of the market. Do consider small-cap, biotech, or penny stocks as there is massive potential for growth. Be reminded that substantial losses can be incurred."
    else:
        portfolio_recommendation = "Invalid Risk Level"
    return portfolio_recommendation

def time_horizon(investment_term):
    # Determine the investor's timeframe for his investments
    if investment_term.lower() == "short":
        time_response = "the timeframe for your investments should be under 1 year."
    elif investment_term.lower() == "medium":
        time_response = "your investment time horizon is between 1-5 years."
    elif investment_term.lower() == "long":
        time_response = "your investments should be held for at least 5 years."
    else: 
        time_response = "Invalid Investment Time Horizon. Please indicate the preferred timeframe for your investments."
    return time_response


### Intents Handlers ###
def buildProfile(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    # Get slot values
    first_name = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    investment_amount = get_slots(intent_request)["investmentAmount"]
    risk_level = get_slots(intent_request)["riskLevel"]
    investment_term = get_slots(intent_request)["timeHorizon"]
    source = intent_request["invocationSource"]

    # Validate user input
    if source == "DialogCodeHook":
        slots = get_slots(intent_request)

        # Validate age
        validation_result = validate_data(age, investment_amount, risk_level, investment_term, intent_request)
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
        
    portfolio_recommendation = get_rec(risk_level)
    
    time_response = time_horizon(investment_term)
    
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """Thank you, {}, {} Based on your time horizon, {}"""
            .format(first_name.capitalize(), portfolio_recommendation, time_response),
        },
    )
    

### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "buildProfile":
        return buildProfile(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")



### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)