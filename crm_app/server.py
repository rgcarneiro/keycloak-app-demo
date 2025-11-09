from flask import Flask, render_template, url_for, session, abort, redirect
from authlib.integrations.flask_client import OAuth
import json
from urllib.parse import quote_plus, urlencode

import os
from dotenv import load_dotenv
import pathlib

path = pathlib.Path(__file__).parent.parent.resolve()
load_dotenv(f"{path}/.env")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET")

oauth = OAuth(app)
oauth.register(
    "crmApp",
    client_id=os.getenv("CRM_OAUTH2_CLIENT_ID"),
    client_secret=os.getenv("CRM_OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
        "code_challenge_method": "S256"
    },
    server_metadata_url=f"{os.getenv('OAUTH2_ISSUER')}/.well-known/openid-configuration",
)


@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4)
    )


@app.route("/callback")
def callback():
    token = oauth.crmApp.authorize_access_token()
    session["user"] = token

    return render_template("crm.html")


@app.route("/login")
def login():
    if "user" in session:
        abort(404)
    return oauth.crmApp.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    id_token = session["user"]["id_token"]
    session.clear()

    return redirect(os.getenv("OAUTH2_ISSUER")
                    + "/protocol/openid-connect/logout?"
                    + urlencode(
                        {
                            "post_logout_redirect_uri": url_for("loggedout", _external=True),
                            "id_token_hint": id_token
                        },
                        quote_via=quote_plus,
    )
    )


@app.route("/loggedout")
def loggedout():
    if "user" in session:
        abort(404)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("CRM_FLASK_PORT"), debug=True)
