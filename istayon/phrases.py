import random

# to format like "{yes|no} {name}{yes_end|maybe_end|no_end}"


def get_name():
    return get_weighted_option(names)


def get_yes():
    return get_weighted_option(yeses)


def get_maybe():
    return get_weighted_option(maybes)


def get_no():
    return get_weighted_option(nos)


def get_yes_end():
    return get_weighted_option(yes_ends)


def get_no_end():
    return get_weighted_option(no_ends)


def get_maybe_up_end():
    return get_weighted_option(maybe_up_ends)


def get_maybe_down_end():
    return get_weighted_option(maybe_down_ends)


# if weights are 5, 4, 3, 4, 1, then the weight space looks like
# |     |    |   |    | |
# with the likelihood of the random int falling in the range dependent on the size
# so get rand int, and subtract range sizes until we're at or below zero.
# weighted random from dictionary, where values are weights
def get_weighted_option(phrase_dict):
    total = sum(phrase_dict.values())
    r = random.randint(1, total)
    for phrase, weight in phrase_dict.iteritems():
        r -= weight
        if r <= 0:
            return phrase

names = {"Taylor Swift": 7,
         # "Bae": 5,
         # "Mom": 5,
         "T-Swift": 3,
         "Taylor": 7,
         "Tay": 5,
         "Becky": 5,
         # "Tay Tay": 2,
         # "T-Swizzle": 3,
         # "Shifty Swifty": 3,
         # "Aunt Becky": 3,
         u"\U0001F385": 1,    # santa emoji
         u"\U0001F40D": 3,    # snake emoji
         # u"\U0001F48C": 1,    # love letter emoji
         # u"\U000026C4": 1,    # snowman emoji
         }

yeses = {"Yep!": 4,
         "Yep,": 5,
         "YAAS,": 3,
         # "Everything's shiny, Cap'n,": 1,
         "Yes!": 3,
         "Yes,": 5
         }

maybes = {"Hmm,": 5,
          }


nos = {"No,": 6,
       "Sad day!": 2,
       ":( ": 2
       }

yes_ends = {" is online.": 4,
            " is liking stuff!": 3,
            "'s online.": 4,
            # " is out of her cabinet!": 1
            }

no_ends = {" isn't online.": 5,
           " hasn't liked anything in awhile.": 5,
           " can't come to the phone right now.": 5,
           " isn't online right now.": 4,
           # " is probably hiding in her cabinet.": 1,
           # " must be off mom-crooning to Britney Spears.": 1,
           # " is likely home making caramel delight.": 1,
           # " isn't on. Meerkat Manor must not have wifi.": 1,
           " isn't online, but she found herself and somehow that was everything.": 2,
           " isn't on, but she might be looking for that All Too Well CD so...": 2,
           }

maybe_up_ends = {" might be here. She just liked a few things.": 6,
                 " just liked a few things!": 3
                 }

maybe_down_ends = {" might still be online?": 6,
                   " is here, maybe. She might've just left.": 5,
                   " might be here, or she just left.": 5,
                   " probably went back in her cabinet.": 1
                   }
