# reddit-auto-saved-downloader
Docker image that'll check your reddit accounts saved posts on a cronjob interval and download and save any new submissions containing pictures that are found. It does not save any comments or other posts! 

This script is made purely for the purpose of downloading all your reddit saved pictures!

## Git flow information
branches:
* `master`
  * Clean branch protected. No git push allowed. Only merge request from `alpha` branch. This is the `production` branch and must be clean.
* `alpha`
  * (Half-)clean branch which is ready to be set into production. No git push allowed. Only merge requests from `feature/*` or `fix/*` branches.
* `feature/[user-story-id]`
  * A branch derived from `alpha` that is created specifically for that feature.
* `fix/[issue]`
  * A branch derived from `alpha` that is created for that specific issue (id).
* `test/[test-name]`
  * A branch derived from `alpha` that has no finished product and is only created for testing. No merge back allowed.


# Running on your own server

Its extremely simple to run this bot on your own server. You can do it with or without docker, I recommend with docker! I'll tell you how to run both regardless though.

## Step 1 Adding your reddit account

You must go to [reddit app preferences](https://www.reddit.com/prefs/apps/) and create a new app of type script. Enter the following details:

> Name: auto-saved-pictures-downloader
>
> select the script type
>
> Description [optional]: Python script running on a cronjob that automatically downloads all saved posts containing pictures
>
> About url [optional]: https://github.com/spark-156/reddit-auto-saved-downloader
>
> Redirect uri: http://localhost:8080/reddit_callback

Press the create app button and copy the client and secret id! Then go to reddit_accounts.json under the /App folder. Add all the credentials and youll be good to go. 

> Yes you need to enter your password and username. This script uses the basic password flow Oauth authorization flow. These credentials are only kept in your reddit_accounts.json and are never sent to me or anyone else. For more on 

Hint: you can copy the dictionary or everything within the {} brackets and add more accounts like so:

```
[
  {
    "username": "throwaway1334123", ...
  },
  {
    "username": "spez", ...
  }
]
```
Add as many accounts as you like!
## Step 2 Adding more accounts

Repeat step 1 for every single account you want to add! You can add as many reddit accounts as you want. Don't worry about performance, the first run will be slow with it having to download up to 1000 pictures but it'll only take about 20 to 30 seconds per account worth of api calls after that per refresh. Just don't go crazy on the refresh rate for the cronjob and you'll be fine!

## Step 3 Installing requirements
Next step is to install the requirements if you haven't already.

You must now choose between either docker or python to host this script.

### Docker
Install docker and docker-compose following these instructions:

docker: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

docker-compose: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

### Python 
Install python3. I'll let you google that on your own for your specific os. Whilst you're at it, look into running a virtual environment for python. Search for the term "venv python" and that should send you down the right path.

Then go in to the /App folder in the command line and execute the following command:
```
pip3 install -r requirements.txt
```
This will read all the requirements for you and install them. You can then create a ".env" file within the /Apps folder and add the following contents:
```
limit=
cronjob=
```

## Step 4 Setting environment variables
The following instructions count for both docker and python following step 3! Edit dockers environment variables in the docker-compose.yml file.

There are two environment variables:
> cronjob 
 
> limit

### Cronjob
cronjob is a 7 long string that is structured like so:
> cronjob=0 0 */2 * * * *

This is seven long and will run the script every two hours, this is the default so you dont have to set it if you dont want to change it. Look up how to write cronjob on google if you want to edit it to a custom value. 

If you wish to run this script once only before letting the script exit. Then you must set the cronjob enveronment variable like so:

> cronjob=@reboot

### Limit
limit tells the script how many saved posts it should get starting with the most recent one. You should leave this at the default None by setting it as such:

> limit=

Since it normally takes around 20 to 30 seconds before an account is all checked and done it really isnt worth it to lower this. Unless it is absolutely necessary you should not lower this. The maximum number of saved posts reddit allows you to have is about 1000 so dont bother setting the limit higher than that.

## Step 5 Starting the application
Now that youve set all the environment variables and added your reddit accounts you're all ready to go.

### Docker
Run the command:
```
make start
```
or the equivalent:
```
docker-compose up -d --build
```
You can check the logs with the following command:
```
docker-compose logs -f logs 
```
Remove or keep the "-f" flag if you want to follow the logs and keep a live track of it within your terminal

### Python
Go in to the /App folder and run "python App.py" in the terminal.

## Step 6 Enjoy
This script should now be periodically downloading your reddit saved posts and saving them to a corresponding .json file whilst simultaniously downloading all the pictures.
The pictures will be placed under a folder named after your own reddit username.