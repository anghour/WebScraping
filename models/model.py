__author__= "Azziz ANGHOUR"
__email__= "anghour@gmail.com"
__version__= "1.0.0"


class Country:
    def __init__(self, id, name, main_link, supply_chain_link):
        self.id = id
        self.name = name
        self.main_link = main_link
        self.supply_chain_link = supply_chain_link

    def __repr__(self):
        return str(self.__dict__)

class Organisation:

    def __init__(self, name, client, description):
        self.name = name
        self.client = client
        self.description = description

    def __repr__(self):
        return str(self.__dict__)

class WindFarmElement :

    def __init__(self, role, organisation):
        self.role = role
        self.organisation = organisation

    def __repr__(self):
        return str(self.__dict__)

class WindFarm:

    def __init__(self, title):
        self.title = title
        self.wind_farm_element_list = []

    def __repr__(self):
        return str(self.__dict__)


class CountrySuppyChain:

    def __init__(self, country, wind_farm_map):
        self.country = country
        self.wind_farm_map = wind_farm_map

    def __repr__(self):
        return str(self.__dict__)




