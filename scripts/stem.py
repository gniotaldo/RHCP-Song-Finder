def is_vowel(letter):
    return letter in 'aeiou'

def measure(word):
    m = 0
    prev_is_vovel = False

    for i in range(1, len(word)):
        if is_vowel(word[i]):
            prev_is_vovel = True
        elif prev_is_vovel and not is_vowel(word[i]):
            m += 1
            prev_is_vovel = False
    return m

def star_d(word):
    return len(word) >= 2 and word[-1] == word[-2] and not is_vowel(word[-1])

def star_o(word):
    if len(word) < 3:
        return False
    return (
        not is_vowel(word[-1])
        and is_vowel(word[-2])
        and not is_vowel(word[-3])
        and word[-1] not in "wxy"
    )

def step_1a(word):
    if word.endswith("sses"):
        return word[:-2]
    elif word.endswith("ies"):
        return word[:-2]
    elif word.endswith("ss"):
        return word
    elif word.endswith("s"):
        return word[:-1]
    return word

def step_1b(word):
    if word.endswith("eed"):
        if measure(word[:-3]) > 0:
            return word[:-1]
    elif word.endswith("ed") or word.endswith("ing"):
        base = word[:-2] if word.endswith("ed") else word[:-3]
        if any(is_vowel(letter) for letter in base):
            word = base
            if word.endswith("at"):
                return word + "e"
            elif word.endswith("bl"):
                return word + "e"
            elif word.endswith("iz"):
                return word + "e"
            elif star_d(word) and word[-1] not in "lsz":
                return word[:-1]
            elif measure(word) == 1 and star_o(word):
                return word + "e"
    return word

def step_1c(word):
    if word.endswith("y") and any(is_vowel(letter) for letter in word[:-1]):
        return word[:-1] + "i"
    return word

def step_2(word):
    suffixes = {
        "ational": "ate", "tional": "tion", "enci": "ence", "anci": "ance",
        "izer": "ize", "abli": "able", "alli": "al", "entli": "ent",
        "eli": "e", "ousli": "ous", "ization": "ize", "ation": "ate",
        "ator": "ate", "alism": "al", "iveness": "ive", "fulness": "ful",
        "ousness": "ous", "aliti": "al", "iviti": "ive", "biliti": "ble"
    }
    for suffix, replacement in suffixes.items():
        if word.endswith(suffix) and measure(word[:-len(suffix)]) > 0:
            return word[:-len(suffix)] + replacement
    return word

def step_3(word):
    suffixes = {
        "icate": "ic", "ative": "", "alize": "al", "iciti": "ic",
        "ical": "ic", "ful": "", "ness": ""
    }
    for suffix, replacement in suffixes.items():
        if word.endswith(suffix) and measure(word[:-len(suffix)]) > 0:
            return word[:-len(suffix)] + replacement
    return word

def step_4(word):
    suffixes = [
        "al", "ance", "ence", "er", "ic", "able", "ible", "ant", "ement",
        "ment", "ent", "ou", "ism", "ate", "iti", "ous", "ive", "ize"
    ]
    for suffix in suffixes:
        if word.endswith(suffix) and measure(word[:-len(suffix)]) > 1:
            return word[:-len(suffix)]
    if word.endswith("ion") and measure(word[:-3]) > 1 and word[-4] in "st":
        return word[:-3]
    return word

def step_5a(word):
    if word.endswith("e"):
        m = measure(word[:-1])
        if m > 1 or (m == 1 and not star_o(word[:-1])):
            return word[:-1]
    return word

def step_5b(word):
    if measure(word) > 1 and star_d(word) and word[-1] == "l":
        return word[:-1]
    return word

def stem_word(word):
    word = word.lower()
    word = step_1a(word)
    word = step_1b(word)
    word = step_1c(word)
    word = step_2(word)
    word = step_3(word)
    word = step_4(word)
    word = step_5a(word)
    word = step_5b(word)
    return ''.join(word)
