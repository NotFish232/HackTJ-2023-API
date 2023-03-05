from flask import Flask, request
import os
import pickle

app = Flask(__name__)

models = os.listdir("pretrained")

print(models)

def is_int(element: str) -> bool:
    try:
        int(element)
        return True
    except ValueError:
        return False


def is_float(element: str) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

def predict(name: str, money: float, days: int) -> float:
    with open(f"pretrained/{name}.pkl", "rb") as f:
        model = pickle.load(f)
    
    initial, after = model.predict([[0], [days]])

    return after / (initial / money)

@app.route("/")
def home_route() -> tuple[dict, int]:
    return {"info": "to get started, visit /predict"}, 200


@app.route("/predict")
def predict_route() -> tuple[dict, int]:
    stock = request.args.get("stock")
    money = request.args.get("money")
    time = request.args.get("time")

    if not stock:
        return {"error": "query parameter 'stock' was not provided"}, 400
    
    if not money:
        return {"error": "query parameter 'money' was not provided"}, 400
    
    if not time:
        return {"error": "query parameter 'time' was not provided"}, 400
    
    if f"{stock}.pkl" not in models:
        return {"error": f"stock '{stock}' does not exist"}, 400
    
    if not is_int(time):
        return {"error": f"{time} is not an integer"}, 400
    
    if not is_float(money):
        return {"error": f"{money} is not a float"}, 400

    days = 30 * int(time)
    money = float(money)

    prediction = predict(stock, money, days)

    return {"prediction": prediction}, 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080")