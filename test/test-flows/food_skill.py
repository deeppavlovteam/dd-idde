import logging
from dff.core.keywords import TRANSITIONS, RESPONSE, MISC, PROCESSING
from dff.core import Actor
import dff.conditions as cnd
from utils import condition as dm_cnd
from utils import common
from utils.entity_detection import has_entities, entity_extraction, slot_filling
from utils.generic_responses import generic_response_condition, generic_response_generate
import dff.labels as lbl
logger = logging.getLogger(__name__)
# def always_true():
#     return True
plot = {
    "food_flow": {
        "start_node": {
            TRANSITIONS: {
                "greeting_node": dm_cnd.is_sf("Open"),
                # "greeting_node": always_true(),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            RESPONSE: "",
            MISC: {"speech_functions": ["Open.Attend"]},
        },
        "fallback_node": {
            TRANSITIONS: {},
            RESPONSE: "I would love to tell you more, but I haven't learnt to do yet!",
            MISC: {"speech_functions": [
                "React.Rejoinder.Confront.Challenge.Detach"]}
        },
        "greeting_node": {
            TRANSITIONS: {
                "another_q": cnd.any([dm_cnd.is_sf("React.Respond.Support.Develop.Extend"), dm_cnd.is_sf("React.Respond.Support.Develop.Elaborate"), dm_cnd.is_sf("React.Respond.Support.Register"), dm_cnd.is_sf("React.Respond.Support.Develop.Enhance")]),
                "likes_lasagna": cnd.any(
                    [
                        cnd.any(
                            [
                                # dm_cnd.is_ext_sf("React.Respond.Support.Reply.Agree"),
                                # dm_cnd.is_ext_sf("React.Respond.Support.Reply.Affirm"),
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("pos_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("pos_answer")]),
                    ]
                ),
                "doesnt_like_lasagna": cnd.any(
                    [
                        # dm_cnd.is_ext_sf("React.Respond.Confront.Reply.Disagree"),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("neg_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("neg_answer")]),  # костыль
                    ]
                ),
                "confused_bot": cnd.any([dm_cnd.is_sf("React.Rejoinder.Support.Track.Confirm"), dm_cnd.is_sf("React.Rejoinder.Support.Track.Clarify"),  dm_cnd.is_sf("React.Rejoinder.Support.Response.Resolve")]),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            RESPONSE: "Hi! I was thinking about food when you texted... I'm dreaming about lasagna! Do you like it?",
            MISC: {"speech_functions": ["Open.Attend", "Open.Give.Fact", "Sustain.Continue.Prolong.Elaborate", "React.Rejoinder.Support.Track.Clarify"]},
        },
        "confused_bot": {
            RESPONSE: "Oh, I really don't know what to say... Do you want to talk about cuisines of the world?",
            TRANSITIONS: {
                "doesnt_like_cuisine": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("pos_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("pos_answer")]),
                    ]
                ),
                "doesnt_want_to_cook": cnd.any(
                    [
                        dm_cnd.is_sf("React.Respond.Confront.Reply.Disagree"),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("neg_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("neg_answer")]),
                    ]
                ),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            MISC: {"speech_functions": ["React.Rejoinder.Support.Develop.Extend", "React.Rejoinder.Support.Track.Clarify"]},
        },
        "another_q": {
            RESPONSE: "Oh, I understand! And do you like pasta?",
            TRANSITIONS: {
                "likes_lasagna": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Affirm"),
                                cnd.all([dm_cnd.is_sf("React.Respond"),
                                        dm_cnd.is_midas("pos_answer")]),
                            ]
                        ),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("pos_answer")]),
                    ]
                ),
                "doesnt_like_lasagna": cnd.any(
                    [
                        dm_cnd.is_sf("React.Respond.Confront.Reply.Disagree"),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("neg_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("neg_answer")]),
                    ]
                ),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            MISC: {"speech_functions": ["React.Respond.Support.Register", "React.Rejoinder.Support.Track.Clarify"]},
        },
        "likes_lasagna": {
            TRANSITIONS: {
                "likes_italian": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Affirm")
                            ]
                        ),
                        cnd.any(
                            [cnd.all([dm_cnd.is_sf("React.Rejoinder"), dm_cnd.is_midas("pos_answer")]),
                             cnd.all([dm_cnd.is_sf("React.Respond"), dm_cnd.is_midas("pos_answer")]), ]
                        )
                    ]
                ),
                "doesnt_like_cuisine": cnd.any(
                    [
                        dm_cnd.is_sf("React.Respond.Confront.Reply.Disagree"),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("neg_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("neg_answer")]),
                    ]
                ),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            RESPONSE: "Oh, we are so similar! So you are a fan of Italian cuisine too, aren't you?",
            MISC: {"speech_functions": [
                "React.Respond.Support.Register", "React.Rejoinder.Support.Track.Probe"]}
        },
        "doesnt_like_lasagna": {
            TRANSITIONS: {
                "likes_italian": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("pos_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("pos_answer")]),  # костыль
                    ]
                ),
                "doesnt_like_cuisine": cnd.any(
                    [
                        dm_cnd.is_sf("React.Respond.Confront.Reply.Disagree"),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("neg_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("neg_answer")]),  # костыль
                    ]
                ),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            RESPONSE: "Oh :( So you don't like Italian cuisine?",
            MISC: {"speech_functions": ["React.Respond.Support.Register", "React.Rejoinder.Support.Track.Probe"]},
        },
        "likes_italian": {
            TRANSITIONS: {
                "fav_italian_dish": cnd.any([dm_cnd.is_sf("React.Rejoinder.Support"), dm_cnd.is_sf("React.Respond.Support")]),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            RESPONSE: "What's your favorite Italian dish?",
            MISC: {"speech_functions": ["React.Rejoinder.Support.Track.Clarify"]},
        },
        "doesnt_like_cuisine": {
            TRANSITIONS: {
                "cuisine": has_entities(["tags:misc"]),
                "fav_cuisine": cnd.all([dm_cnd.is_sf("React")]),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            RESPONSE: "Then what's your favorite cuisine?",
            MISC: {"speech_functions": ["React.Rejoinder.Support.Track.Clarify"]},
        },
        "cuisine": {
            PROCESSING: {
                1: entity_extraction(cuisine=["tags:misc"]),
                2: slot_filling,
            },
            RESPONSE: "Oh, [cuisine]! I just adore it!",
            TRANSITIONS: {
                "really_likes_cuisine": cnd.exact_match("yeah"),
                "doesnt_want_to_cook": dm_cnd.is_sf("React"),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            MISC: {"speech_functions": [
                "React.Respond.Support.Register", "Sustain.Continue.Prolong.Elaborate"]}
        },
        "fav_italian_dish": {
            TRANSITIONS: {
                "really_likes_cuisine": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("pos_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("pos_answer")]),  # костыль
                    ]
                ),
                "doesnt_want_to_cook": cnd.any(
                    [
                        dm_cnd.is_sf("React.Respond.Confront.Reply.Disagree"),
                        dm_cnd.is_sf(
                            "React.Rejoinder.Support.Response.Resolve"),
                        dm_cnd.is_sf("React.Respond.Support.Develop"),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("neg_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("neg_answer")]),  # костыль
                    ]
                ),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            RESPONSE: "Yeah, I love it too! Have you ever tried to cook it?",
            MISC: {"speech_functions": ["React.Respond.Support.Register", "React.Rejoinder.Support.Track.Clarify"]},
        },
        "fav_cuisine": {
            TRANSITIONS: {
                "really_likes_cuisine": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                        cnd.all(
                            [cnd.any([dm_cnd.is_sf("React.Rejoinder"),
                                      dm_cnd.is_sf(
                                          "React.Respond.Support.Develop.Extend"),
                                      dm_cnd.is_sf("React.Respond.Support.Develop.Enhance")]),
                             dm_cnd.is_midas("pos_answer")]),
                    ],
                ),
                "doesnt_like_cuisine": cnd.any(
                    [
                        dm_cnd.is_sf("React.Respond.Confront.Reply.Disagree"),
                        dm_cnd.is_sf(
                            "React.Rejoinder.Support.Response.Resolve"),
                        cnd.all(
                            [cnd.any([dm_cnd.is_sf("React.Rejoinder"),
                                      dm_cnd.is_sf(
                                          "React.Respond.Support.Develop.Extend"),
                                      dm_cnd.is_sf("React.Respond.Support.Develop.Enhance")]),
                             dm_cnd.is_midas("neg_answer")]),
                    ],
                ),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            RESPONSE: "Really? Never met a person who liked it!",
            MISC: {"speech_functions": ["React.Respond.Support.Register", "React.Rejoinder.Support.Track.Clarify"]},
        },
        "doesnt_want_to_cook": {
            TRANSITIONS: {
                "adores_cooking_people": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("pos_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("pos_answer")]),  # костыль
                    ]
                ),
                "cooking_is_trouble": cnd.any(
                    [
                        dm_cnd.is_sf("React.Respond.Confront.Reply.Disagree"),
                        dm_cnd.is_sf(
                            "React.Rejoinder.Support.Response.Resolve"),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("neg_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("neg_answer")]),  # костыль
                    ]
                ),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            RESPONSE: "Okay! And do you like cooking?",
            MISC: {"speech_functions": ["React.Respond.Support.Register", "React.Rejoinder.Support.Track.Clarify"]},
        },
        "really_likes_cuisine": {
            TRANSITIONS: {
                "adores_cooking_people": cnd.any(
                    [
                        cnd.any(
                            [
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Agree"),
                                dm_cnd.is_sf(
                                    "React.Respond.Support.Reply.Affirm"),
                            ]
                        ),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("pos_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("pos_answer")]),  # костыль
                    ]
                ),
                "cooking_is_trouble": cnd.any(
                    [
                        dm_cnd.is_sf("React.Respond.Confront.Reply.Disagree"),
                        dm_cnd.is_sf(
                            "React.Rejoinder.Support.Response.Resolve"),
                        cnd.all([dm_cnd.is_sf("React.Rejoinder"),
                                dm_cnd.is_midas("neg_answer")]),
                        cnd.all([dm_cnd.is_sf("React.Respond"),
                                dm_cnd.is_midas("neg_answer")]),  # костыль
                    ]
                ),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            RESPONSE: "That's so cool, I'd love to learn how to cook it one day! Do you like cooking?",
            MISC: {"speech_functions": ["React.Respond.Support.Register", "React.Rejoinder.Support.Track.Clarify"]},
        },
        "adores_cooking_people": {
            TRANSITIONS: {
                "say_goodbye": cnd.any([dm_cnd.is_sf("React"), dm_cnd.is_sf("Open"), ]),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            RESPONSE: "Wow, I just adore people who know how to cook!",
            MISC: {"speech_functions": ["React.Rejoinder.Support.Track.Clarify"]},
        },
        "cooking_is_trouble": {
            TRANSITIONS: {
                "say_goodbye": cnd.any([dm_cnd.is_sf("React"), dm_cnd.is_sf("Open"), ]),
                ("generic_responses_flow", "generic_response"): generic_response_condition,
            },
            RESPONSE: "Yep, I understand. Usually cooking is just too much trouble.",
            MISC: {"speech_functions": ["React.Rejoinder.Support.Track.Clarify"]},
        },
        "say_goodbye": {
            TRANSITIONS: {},
            RESPONSE: "Oh... Sorry, I have to go now. I want to grab some lasagna. Bye!",
            MISC: {"speech_functions": ["React.Respond.Support.Register", "Sustain.Continue.Prolong.Extend", "React.Rejoinder.Confront.Challenge.Detach"]},
        },
    },
    # "generi_responses_flow": {
    #     "start_node": {
    #         RESPONSE: "",
    #         TRANSITIONS: {"generic_response": generic_response_condition},
    #     },
    #     "generic_response": {
    #         RESPONSE: generic_response_generate,
    #         TRANSITIONS: {lbl.repeat(): generic_response_condition},
    #     },
    # }
}
actor = Actor(
    plot,
    start_label=("food_flow", "start_node"),
    fallback_label=("food_flow", "fallback_node"),
)
if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s-%(name)15s:%(lineno)3s:%(funcName)20s():%(levelname)s - %(message)s",
        level=logging.INFO,
    )
    common.run_interactive_mode(actor)
