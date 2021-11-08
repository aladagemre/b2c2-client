# -*- coding: utf-8 -*-
"""
Request for Quote
    - Instrument
    - Side
    - Quantity
    - ?

    Display information. Ask: "Would you like to execute the RFQRequest?"
    - Yes => Create order => Validated => Display account balance &  the trade information contained in the order response
    - compute your balance before actually receiving it from our engine so you can see if they match.


"""

action_question = [
    {
        "type": "list",
        "name": "action",
        "message": "What do you want to do?",
        "choices": [
            "List Instruments",
            "Request for Quote (RFQRequest)",
            "Create Order",
            "Display Balance",
            "Display Order History",
            "Display Trade History",
            "Display Order Details",
            "Display Trade Details",
            "Token Settings",
            "API URL Settings",
            "Check connection",
            "Quit",
        ],
    }
]


def get_list_instruments_question(instruments):
    return [
        {
            "type": "list",
            "name": "instrument_action",
            "message": "Do you want a Request for Quote (RFQ) for an instrument? Choose below.",
            "choices": ["No Thanks"] + instruments,
        }
    ]
