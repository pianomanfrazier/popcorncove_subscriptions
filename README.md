# Popcorn Cove Subscription Service

This app tracks customers' subscriptions boxes. The users can input new customers, search for existing customers, create a new subscription or modify an existing subscription. Finally the user can export all the subscription boxes going out that month to a spreadsheet and print out address shipping labels.

[YouTube video demo](https://youtu.be/P_8gmr_Ol-4)

## Screenshots

![Step 1](/docs/images/step1.png)
![Step 2](/docs/images/step2.png)
![Step 3](/docs/images/step3.png)
![Manage Items](/docs/images/items.png)
![Export Subscriptions](/docs/images/export.png)

## Development

Several environment variables are required for proper startup of the app. For the best database development experiece spin up a postgres database using:

```bash
docker run --name flask-postgres -e POSTGRES_PASSWORD=supersecret -p 5432:5432 -d postgres
```

Here is a sample `.env` file:

```bash
ADMIN_USER="admin"
ADMIN_PASSWORD="supersecret"
FLASK_APP="./server.py"
DATABASE_URL="postgresql://postgres:supersecret@localhost/postgres"
```

Then run the app

```bash
pip install virtualenv
virtualenv -p python3 venv
source ./venv/bin/activate
pip install -r requirements.txt
flask run
```

The app then uses basic http auth to authorize the user. Be sure to deploy this on https or the credentials are easy to grab from the header.

To develop the client use the webpack dev server.

```bash
cd client
npm run dev
```

## TODO

- allow admin to delete customer
- add loading status to all AJAX buttons
- lazy load customers when searching (i.e. limit 10 on type ahead)
- add server logging support see https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xviii-deployment-on-heroku
