def token_write(ACCESS_TOKEN, REFRESH_TOKEN, filename = 'upnext/tokens.txt'):
    openfile = open(filename, 'r+')
    openfile.write(ACCESS_TOKEN + '\n' + REFRESH_TOKEN)
    openfile.close()


def token_read(filename = 'upnext/tokens.txt'):
    openfile = open(filename, 'r+')
    tokens = openfile.read()
    tokens = tokens.splitlines()
    token_dict = dict()
    token_dict['ACCESS_TOKEN'] = tokens[0]
    token_dict['REFRESH_TOKEN'] = tokens[1]
    openfile.close()
    return token_dict
