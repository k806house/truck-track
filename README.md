# Truck & Track

### Setup

1. Get [Google Api Key](https://developers.google.com/maps/documentation/javascript/get-api-key) and set value in [envs.py](envs.py)

2. Install requirements
```
pip3 install -r requirements.txt
```

3. Run app
```
python3 app.py
```

4. API will be available `localhost:8080`

### Endpoints

**/predict**

Predicts the time from the factory to the customer.

Input parameters:
- `address` (string) --- customer address
- `volume` (float) --- order volume (m3)
- `date` (string) --- date and time of delivery

Output: list of predicted datetimes

Example request:
```
curl localhost:8080/predict?&address=Yonge-Dundas%20Square%2C%20Dundas%20Street%20East%2C%20Торонто%2C%20Онтарио%2C%20Канада&volume=10&date=2021-09-26T13%3A30%3A42.933Z
```

### Links

[Frontend](https://github.com/k806house/HachZurich)

[RnD](https://github.com/k806house/truck-track-ml-rnd)
