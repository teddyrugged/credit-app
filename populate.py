import json
from creditapp.models import Customer, Transaction
import os
filename = os.path.join(os.getcwd(),"sample.json")


def populate_db():
    file = open(filename,"r")
    details = json.loads(file.read())
    print(details)

    for customer in details:
        user = Customer.objects.create(
        name = customer["name"],
        phone = customer["phone_number"],
        bvn = customer["bvn"]
        )
        for transact in customer["transactions"]:
            Transaction.objects.create(
                customer = user,
                transaction_date = transact["date"],
                transaction_amount = transact["amount"],
                transaction_type = transact["transaction_type"],
            )



