# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import json

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


def load_json(file_name):
    with open("data/botInfo.json") as config:
        return json.load(config)


class ActionShowScheduleWorld(Action):

    def name(self) -> Text:
        return "action_show_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tournament_data = load_json("data/botInfo.json")

        for match in tournament_data["Tournament"]["Schedule"]:
            player1 = tournament_data["Tournament"]["Schedule"][match]["1"]
            player2 = tournament_data["Tournament"]["Schedule"][match]["2"]
            date = tournament_data["Tournament"]["Schedule"][match]["Date"]
            info = match + ": " + player1 + " VS " + player2 + " will begin at " + date
            dispatcher.utter_message(
                text=str(info)
            )

        return []


class ActionShowInfo(Action):

    def name(self) -> Text:
        return "action_show_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tournament_data = load_json("data/botInfo.json")

        for row in ["Name", "Info", "Prize", "Game"]:
            message = row + ": " + tournament_data["Tournament"][row]
            dispatcher.utter_message(
                text=str(message)
            )

        return []


class ActionReturnEmpty(Action):

    def name(self) -> Text:
        return "action_return_empty"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tournament_data = load_json("data/botInfo.json")

        cnt = 0
        for match in tournament_data["Tournament"]["Schedule"]:
            player1 = tournament_data["Tournament"]["Schedule"][match]["1"]
            player2 = tournament_data["Tournament"]["Schedule"][match]["2"]
            if player1 == "Empty":
                cnt += 1

            if player2 == "Empty":
                cnt += 1

        if cnt == 0:
            message = "There are no places left"
        else:
            message = "There are {place}".format(place=cnt) + " places left"

        dispatcher.utter_message(
            text=str(message)
        )

        return []
