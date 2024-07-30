from player import Player
import random
AQUA = (0, 175, 185)
LIGHTRED = (240, 113, 103)

excerpts = [["gatsby", "in", "my", "younger", "and", "more", "vulnerable", "years", "my", "father", "gave", "me", "some", "advice", "that", "ive", "been", "turning", "over", "in", "my", "mind", "ever", "since", "whenever", "you", "feel", "like", "criticizing", "anyone", "he", "told", "me", "just", "remember", "that", "all", "the", "people", "in", "this", "world", "havent", "had", "the", "advantages", "that", "youve", "had", "they", "were", "born", "without", "privilege", "or", "opportunity", "it's", "easy", "to", "judge", "others", "without", "considering", "their", "circumstances", "but", "true", "empathy", "requires", "understanding", "and", "compassion", "so", "before", "you", "condemn", "someone", "try", "to", "see", "the", "world", "through", "their", "eyes", "and", "walk", "in", "their", "shoes", "only", "then", "can", "you", "truly", "appreciate", "the", "complexities", "of", "human", "existence", "and", "the", "struggles", "that", "many", "face", "every", "day"],
            ["hammy", "to", "be", "or", "not", "to", "be", "that", "is", "the", "question", "whether", "tis", "nobler", "in", "the", "mind", "to", "suffer", "the", "slings", "and", "arrows", "of", "outrageous", "fortune", "or", "to", "take", "arms", "against", "a", "sea", "of", "troubles", "and", "by", "opposing", "end", "them", "to", "die", "to", "sleep", "no", "more", "and", "by", "a", "sleep", "to", "say", "we", "end", "the", "heartache", "and", "the", "thousand", "natural", "shocks", "that", "flesh", "is", "heir", "to", "tis", "a", "consummation", "devoutly", "to", "be", "wishd", "to", "die", "to", "sleep", "to", "sleep", "perchance", "to", "dream", "ay", "theres", "the", "rub", "for", "in", "that", "sleep", "of", "death", "what", "dreams", "may", "come", "when", "we", "have", "shuffled", "off", "this", "mortal", "coil", "must", "give", "us", "pause", "theres", "the" ]]


class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.text = excerpts[random.randint(0, len(excerpts) - 1)]
        self.players = [Player(50, 550, AQUA, self.text), Player(50, 550, LIGHTRED, self.text)]
        self.winner = False
        self.reset = False

    def connected(self):
        return self.ready


