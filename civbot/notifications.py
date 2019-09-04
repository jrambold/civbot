def getSlackId(steam_name):
    usercomp = {
        'wraithcube': '<@U33KZ0E95>',
        'cowtastic': '<@U32S2CLTU>',
        'dejavood0o': '<@U32UN4LGM>',
        'pouchnort': '<@U33Q58S3E>',
        'mr goopy daddy': '<@U33HC4X0E>',
        'spadefish': '<@U35MSNBUM>',
        'kalamari tank': '<@U32U6FD50>',
        'davis': '<@U32UUHARF>',
        'hack': '<@UMPH45VPT>',
    }
    name = steam_name.lower()
    if name in usercomp:
        return usercomp[name]
    return steam_name
