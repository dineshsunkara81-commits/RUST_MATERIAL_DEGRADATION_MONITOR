def predict_risk(material, environment, age):

    material = material.lower()
    environment = environment.lower()

    if material == "iron":

        if environment == "coastal":
            return "High"

        elif environment == "rainy" and age >= 3:
            return "High"

        elif age >= 5:
            return "Medium"

        else:
            return "Low"

    elif material == "steel":

        if environment == "industrial":
            return "High"

        elif age >= 6:
            return "Medium"

        else:
            return "Low"

    elif material == "aluminium":

        if age >= 10:
            return "Medium"

        return "Low"

    return "Low"