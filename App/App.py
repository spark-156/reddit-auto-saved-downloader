import os
import json
import requests
import requests.auth

PORT = os.environ.get("PORT", "The port is not set")
CLIENT_ID = os.environ.get("CLIENT_ID", "The client id is not set")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", "The client secret is not set")
REDIRECT_URI = os.environ.get("REDIRECT_URI", "The redirect uri is not set")

# Log all env variables
print(f"[Log] PORT = {PORT}\n[Log] CLIENT_ID = {CLIENT_ID} \n[Log] CLIENT_SECRET = {CLIENT_SECRET}\n[Log] REDIRECT_URI = {REDIRECT_URI}")

def get_username(access_token):
    headers = {"Authorization": "bearer " + access_token}
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    me_json = response.json()
    return me_json['name']
    
def get_token(code):
	client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
	post_data = {"grant_type": "authorization_code",
				 "code": code,
				 "redirect_uri": REDIRECT_URI}
	response = requests.post("https://ssl.reddit.com/api/v1/access_token",
							 auth=client_auth,
							 data=post_data)
	token_json = response.json()
	return token_json["access_token"]

from flask import Flask, abort, request
app = Flask(__name__)

@app.route('/')
def homepage():
  print("log")
  text = '<a href="%s">Authenticate with reddit</a>'
  return text % make_authorization_url()

def make_authorization_url():
	# Generate a random string for the state parameter
	# Save it for use later to prevent xsrf attacks
	from uuid import uuid4
	state = str(uuid4())
	save_created_state(state)
	params = {"client_id": CLIENT_ID,
			  "response_type": "code",
			  "state": state,
			  "redirect_uri": REDIRECT_URI,
			  "duration": "permanent",
			  "scope": "identity"}
	import urllib
	url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.parse.urlencode(params)
	return url

# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.
def save_created_state(state):
	pass
def is_valid_state(state):
	return True

@app.route('/reddit_callback')
def reddit_callback():
  error = request.args.get('error', '')
  if error:
    return "Error: " + error
  state = request.args.get('state', '')
  if not is_valid_state(state):
    # Uh-oh, this request wasn't started by us!
    abort(403)
  code = request.args.get('code')
  # We'll change this next line in just a moment
  access_token = get_token(code)
  return "Your reddit username is: %s" % get_username(access_token)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=PORT)