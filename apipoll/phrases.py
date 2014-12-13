__author__ = 'avaleske'
import random

# to format like "{yes|no} {name}{yes_end|maybe_end|no_end}"


# todo bias these so the entertaining ones come up less often
def get_name():
    return random.choice(names)


def get_yes():
    return random.choice(yeses)

def get_maybe():
    return random.choice(maybes)


def get_no():
    return random.choice(nos)


def get_yes_end():
    return random.choice(yes_ends)


def get_no_end():
    return random.choice(no_ends)


def get_maybe_end():
    return random.choice(maybe_ends)


names = ["Taylor Swift",
         "Bae",
         "Mom",
         "T-Swift",
         "Taylor",
         "Tay",
         "Becky",
         "Tay Tay",
         "T-Swizzle",
         u"\U0001F385"
         ]

yeses = ["Yep!",
         "Yep,"
         "YAAS,",
         "Everything's shiny, Cap'n,",
         "*nods*,",
         "Yes!"
        ]

maybes = ["Hmm...",
          "Huh,",
          "*shrugs*",
          "idk."
         ]

nos = ["No,",
       "Sorry,",
       "Sad day!",
       ":( "
       ]

yes_ends = [" is online!",
            " is online, go reblog everything!",
            " is liking stuff!",
            "'s online.",
            "'s hanging out with us!"
            ]

no_ends = [" isn't online. Sorry. :(",
           " hasn't liked anything in awhile...",
           " isn't online right now.",
           ]

maybe_ends = [" might be online?",
              " might be here. It's hard to tell.",
              "'s here, maybe. She might've just gone offline.",
              " could be online. We can't really tell...",
              " might be here, or might've just left. Give us a few minutes to see.",
              " might be online? It's hard to guess, tbh."
             ]