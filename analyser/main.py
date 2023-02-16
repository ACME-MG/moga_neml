from modules.api import API
api = API("", 2)
api.define_conditions(800, 80)
api.define_model("evpwd")
api.assess_dependency(1000)