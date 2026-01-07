import sys

from werkzeug.exceptions import InternalServerError

sys.path.append('..')

import logging.config

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import InputRequired, Optional

from big_application.workers import *
from big_application.logger_setup import dict_config


logging.config.dictConfig(dict_config)

logger = logging.getLogger("skillbox")
app = Flask(__name__)


class WorkerForm(FlaskForm):
   x = IntegerField(validators=[InputRequired()])
   y = IntegerField(validators=[InputRequired()])


@app.route("/worker1", methods=["POST"])
def _worker1_endpoint():
   form = WorkerForm()

   if form.validate_on_submit():
       x, y = form.x.data, form.y.data

       result = worker1(x, y)
       return f"{x} ** {y} = {result}"

   logger.error(f"Cannot process form {form.errors}")

   return "Cannot process form", 400


@app.route("/worker2", methods=["POST"])
def _worker2_endpoint():
   form = WorkerForm()

   if form.validate_on_submit():
       x, y = form.x.data, form.y.data

       result = worker2(x, y)
       return f"{y} ** {x} = {result}"

   logger.error(f"Cannot process form {form.errors}")

   return "Cannot process form", 400


@app.route("/worker3", methods=["POST"])
def _worker3_endpoint():
   form = WorkerForm()

   if form.validate_on_submit():
       x, y = form.x.data, form.y.data

       result = worker3(x, y)
       return f"{x} ** {y} = {result}"

   logger.error(f"Cannot process form {form.errors}")

   return "Cannot process form", 400


@app.errorhandler(Exception)
def handle_exception(e: Exception):
    logger.exception(e)
    return "Internal server error", 500


if __name__ == "__main__":
   app.config["WTF_CSRF_ENABLED"] = False

   app.run(debug=True)
