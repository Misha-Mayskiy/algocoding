def strip_punctuation_ru(data):
    punctuations = '!()[]{};:\'",<>./?@#$%^&*_~.«»…'

    result = ""
    for char in data:
        if char in punctuations:
            result += ' '
        else:
            result += char

    result = result.replace(' - ', ' ')
    result = result.replace(' — ', ' ')

    return ' '.join(result.split())