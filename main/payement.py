import requests

BASE_URI = "https://www.klikandpay.com/paiement/order1.pl"
MARCHAND_ID = ""




def make_payement(user, package) -> bool:
    payement = {
        "ID": MARCHAND_ID,
        "NOM": user.last_name,
        "PRENOM": user.first_name,
        "EMAIL": user.email,
        "PAYS":  user.country,  # format iso 3166,
        "MONTANT": package.price  # package?
    }

    req = requests.post(BASE_URI, data=payement, headers={
        'Accept-Charset': 'UTF8',
        'Accept': 'application/json'
    })

    if req.status_code == 200:
        response = req.json()
        return response.get("Response", "").lower() == "ok"

    return False

