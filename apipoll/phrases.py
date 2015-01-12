__author__ = 'avaleske'
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
         "Bae": 5,
         "Mom": 5,
         "T-Swift": 3,
         "Taylor": 7,
         "Tay": 5,
         "Becky": 5,
         "Tay Tay": 2,
         "T-Swizzle": 3,
         u"\U0001F385": 2,   # santa emoji
         u"\U0001F48C": 5    # love letter emoji
         }

yeses = {"Yep!": 4,
         "Yep,": 5,
         "YAAS,": 3,
         "Everything's shiny, Cap'n,": 1,
         "*nods*,": 1,
         "Yes!": 3,
         "Yes,": 5
         }

maybes = {"Hmm...": 5,
          "idk.": 1
          }


nos = {"No,": 6,
       "Sad day!": 3,
       ":( ": 1
       }

yes_ends = {" is online.": 4,
            " is online, go reblog everything!": 1,
            " is liking stuff!": 3,
            "'s online.": 4,
            "'s hanging out with us!": 2,
            }

no_ends = {" isn't online. :/": 3,
           " hasn't liked anything in awhile.": 4,
           " isn't online right now.": 6
           }

maybe_up_ends = {" might be here. She just liked a few things.": 3,
                 " just liked a few things, but might not stay.": 6
                 }

maybe_down_ends = {" might still be online?": 6,
                   "'s here, maybe. She might've just left.": 5,
                   " might be here, or just left. Refresh in a minute or two?": 5
                   }