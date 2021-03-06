import sys
import json
import urllib
import urllib2
import re
import time

import LEP

def count_all():
    try:
        with open(LEP.congress_file, 'w') as f:
            # TODO(mike.xu): make range configurable
            for c in range(93, 115):
                n = count_congress(c)
                line = '{},{}\n'.format(c, n)
                f.write(line)
    # TODO(mike.xu): more specific error handling
    except:
        print('Error writing congress file: {}'.format(sys.exc_info()[0]))

def count_congress(c):
    q = {
        'chamber': 'Senate',
        'congress': str(c),
        'source': 'legislation',
        'type': 'bills'
    }
    params = {
        'q': json.dumps(q),
    }
    url = 'https://www.congress.gov/search?{}'.format(urllib.urlencode(params))
    print(url)

    soup = None
    tries = 0
    while soup is None and tries < 5:
        if tries > 0:
            time.sleep(tries + 1)
        soup = LEP.get_soup(url)
        tries = tries + 1
    
    ele = soup.select('.results-number')
    if len(ele) < 1:
        raise AppError('Could not find result count element')
    result_str = ''.join(ele[0].find_all(text=True, recursive=False)).strip()
    return int(re.sub(r'[^0-9]*', '', result_str))    

if __name__ == '__main__':
    count_all()
