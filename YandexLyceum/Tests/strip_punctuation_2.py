def strip_punctuation_ru(data):
    punctuations = '!()[]{};:\'",<>./?@#$%^&*_~.«»—…'

    result = ""
    for char in data:
        if char in punctuations:
            result += ' '
        else:
            result += char

    return ' '.join(result.split())
