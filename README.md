# robinhood-ext
This project is to implement some features that Robinhood lack of, for example, insightful/interactive visualization, news NLP analytics, trade execution/strategies. This is connected to Robinhood via an unofficial python APIs in this [repo](https://github.com/Jamonek/Robinhood).

## Run Locally
This web application requires you to input your Robinhood username and password but it is never stored in the application. If you are not comfortable, you could definitely run it locally in your computer. Go into the project directory, and start the FLask server by python3.
```
pip3 install -r requirements.txt
python3 main.py
```

## Deploy to Google Cloud App Enginee
The project is ready for GCP AppEng. You should install cloud SDK in your computer, then push by below command.
```
gcloud app deploy
```