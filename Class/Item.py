import re
class Item:
    def __init__(self, info_item: dict, version:str) -> None:
        ""
        self.name = info_item["name"]
        image = info_item["image"]["full"]
        self.id = int(image.split(".")[0])
        self.image = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/item/{image}"
        if info_item["description"] != "" and info_item["maps"]["11"] and not ("requiredAlly" in info_item) and "raritylegendary" not in self.name and not ("inStore"  in info_item):
            xml_data = info_item["description"]

            def remplacer_br(match):
                return '\n'
            
            self.description = re.sub(r'<br\s*/?>', remplacer_br, xml_data)
            self.description = re.sub(r'<.*?>', '', self.description)
        else:
            self.description = ""
    