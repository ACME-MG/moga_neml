from modules.api import API
api = API("", 2)
api.add_curve({"type": "creep", "temp": 800, "stress": 80})
api.define_model("evpwd")
api.assess_params(1000)