from project4_files import mongo, main_functions
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, DecimalField, SubmitField
from wtforms.validators import DataRequired
import requests


# class for our forms
class Expenses(FlaskForm):
    # create the form for the following fields
    # StringField : description
    description = StringField("Description", validators=[DataRequired()])
    # SelectField : category
    category = SelectField("Category", validators=[DataRequired()])
    # StringField : new category
    new_category = StringField("New Category")
    # SelectField : currency
    currency = SelectField("Convert Currency",
                          choices=[("USD", "United States Dollar"),
                                   ("CUP", "Cuban Peso"),
                                   ("EUR", "Euro"),
                                   ("CAD", "Canadian Dollar"),
                                   ("JPY", "Japanese Yen"),
                                   ("BTC", "Bitcoin")])
    # DecimalField : cost
    cost = DecimalField("Cost", validators=[DataRequired()])
    # DateField : date
    date = DateField("Date of purchase",
                     format='%m-%d-%Y',
                     validators=[DataRequired()],
                     render_kw={"placeholder": "mm-dd-yyyy"})

# when given a list of unique categories, this function will step through each item x and find every occurance of x in
# the collection and sum their values.
# returns a dictionary of { category : summed_price }
# distinct_cat is a list of unique categories
def get_category_expenses(distinct_cat):

    # will hold our {category : summed_price} pairs
    category_price_dict = {}

    for cat in distinct_cat:
        # print("cat var:", cat)
        # get only the documents with category <cat> and make an iterable object
        # also, only return the cost field
        unique_cat = mongo.db.expenses.find({"category": cat}, {"cost": 1})
        #print("unique_cat:", unique_cat)

        # zero out our total variable
        total = 0
        #print("item in unique_cat")
        for item in unique_cat:
            total += float(item["cost"])
            # print(item)

        #print("=====================================")
        #print("total of", cat, "is:", total)
        category_price_dict[cat] = total

    #print(category_price_dict.items())
    return category_price_dict


def currency_converter(cost, currency):

    my_key_dict = main_functions.read_from_file("project4_files/JSON_Documents/api_key.json")
    my_key_string = my_key_dict["api_key"]

    # start building api call string
    api_string = \
        "http://api.currencylayer.com/live?access_key=" + my_key_string + \
        "&currencies=" + currency

    # do api call
    api_request = requests.get(api_string).json()
    main_functions.write_to_file(api_request, "project4_files/JSON_Documents/real_time_currency.json")
    currency_response_dict = main_functions.read_from_file("project4_files/JSON_Documents/real_time_currency.json")

    # find what the conversion rate is
    # print("currency_response_dict is type", type(currency_response_dict))
    # print("cost argument:", cost)
    # print("currency argument:", currency)
    exchange_rate = currency_response_dict["quotes"]["USD"+currency]
    cost = float(cost)
    print("cost before exchange:", cost)
    cost = round((cost/exchange_rate), 2)
    print("cost after exchange:", cost)

    return cost