#!/usr/bin/env python3

# from linkedin_v2 import linkedin
import urllib3
from linkedin_v2 import linkedin
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlencode, quote_plus
import random
import json

from rauth import OAuth2Service

API_KEY='86kl0i8z0pt51w'
API_SECRET='tLampHKkdkuW9PA6'
API_CODE='AQSLUpq-6rIizbBqBM156Wbsrz-nG0OWVdVOdBTma4Ikxpi6hBM3qlfkjKhWX6-8-RSRw16AVq8bAXh79RERujzO1zhn_Fby7XoBs05PmlgtUguVZh-uXjAgvOJjMUa1zrOBE7wyGnNY_g6M_jYlzJj3FiisKfm1FEaa648wLGLmkqPORj4eqPIDOwoCVw&state=bdb91dafdaafe5aaf2776e65b83067'
RETURN_URL = 'https://localhost/auth/callback'


def main():
  # payload = {
  #   'response_type': 'code',
  #   'client_id' : CLIENT_ID,
  #   'redirect_uri': redir_url,
  #   'state': '987654321',
  #   'scope': 'r_basicprofile'
  # }
  
  # authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL)
  # print(authentication.authorization_url)
  # application = linkedin.LinkedInApplication(authentication)

  # authentication.authorization_code = API_CODE
  # authentication.get_access_token()
  # pairs = []
  # for k,v in params.items():
  #   pairs += ['%s=%s' % (k, v)]
  # par_string = urlencode(payload, quote_via=quote_plus)
  # # print(par_string)
  # # url = 'https://www.linkedin.com/jobs/view/1056880115'
  # url = 'https://www.linkedin.com/oauth/v2/authorization?%s' % par_string
  # print(url)
  # fp = urllib.request.urlopen(url)
  # mybytes = fp.read()
  # content = mybytes.decode("utf8")
  # fp.close()

  # # # soup = BeautifulSoup(content, 'html')
  # print(content)

  # with open('vacancy.txt') as f:
  #   f.write(content)

  # details_node = soup.find("meta", {"name": "og:description"})

  # print(details_node)

  linkedin = OAuth2Service(
      client_id=API_KEY,
      client_secret=API_SECRET,
      name='linkedin',
      authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
      access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
      base_url='https://api.linkedin.com/v1/')

  # redirect_uri = 'https://github.com/litl/rauth/'

  # params = {'response_type': 'code',
  #           'scope': 'r_fullprofile',
  #           'state': ''.join(str(random.randrange(9)) for _ in range(24)),
  #           'redirect_uri': redirect_uri}

  # authorize_url = linkedin.get_authorize_url(**params)

  # print 'Visit this URL in your browser: ' + authorize_url
  # code = raw_input('Enter code from browser: ')

  session = linkedin.get_auth_session(data={'grant_type': 'authorization_code',
                                            'code': API_CODE,
                                            'redirect_uri': RETURN_URL},
                                      decoder=json.loads)

  r = session.get('people/~',
                  params={'type': 'SHAR',
                          'format': 'json',
                          'oauth2_access_token': session.access_token},
                  bearer_auth=False)

  print(r.json())



if __name__ == "__main__":
    main()