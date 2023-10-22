import requests
from Class.Champion import Champion
from Class.Item import Item

class League:
    ""
    def __init__(self, versions) -> None:
        self.versions = versions
        self.items_info = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{self.versions[0]}/data/fr_FR/item.json").json()["data"]
        self.items = {self.items_info[item]["name"]: Item(self.items_info[item],self.versions[0]) for item in self.items_info}        
        self.champions_info = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{self.versions[0]}/data/fr_FR/champion.json").json()["data"]
        self.champions = {self.champions_info[champion]["name"]: Champion(self.champions_info[champion]) for champion in self.champions_info}
