roles = {
    "Assassin": "Assassin",
    "Fighter": "Combattant",
    "Mage": "Mage",
    "Marksman": "Tireur",
    "Support": "Support",
    "Tank": "Tank",
}

class Champion:
    def __init__(self, info_champion: dict) -> None:
        ""
        self.name = info_champion["name"]
        self.id = info_champion["key"]
        self.image = f"https://ddragon.leagueoflegends.com/cdn/{info_champion['version']}/img/champion/{info_champion['image']['full']}"
        self.tags = []
        self.title = info_champion["title"]
        self.splash_art = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{info_champion['id']}_0.jpg"
        for tag in info_champion["tags"]:
            self.tags.append(roles[tag])
