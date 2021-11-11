from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
import requests
import json
# Your friendly example event
# Keep in mind that the command name will be derived from the class name
# but in lowercase

base_url = "https://api.thegraph.com/subgraphs/name/catgirlcoin/catgirl-bsc"
head =  {"accept": "application/json, text/plain, */*", "accept-language": "en-US,en;q=0.9", "content-type": "application/json"}


# So, a command class named Random will generate a 'random' command
class catgirl(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Attempts to get cat girl"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params' 
        # argument in the handle() method
        # If no params are expected, leave this list empty or set it to None
        params = ["catID"]
        super().__init__(description, params)

    # Override the handle() method
    # It will be called every time the command is received
    async def handle(self, params, message, client):
        try: 
            body = "{\"operationName\":\"GetCatgirls\",\"variables\":{\"skip\":0,\"orderDirection\":\"desc\",\"first\":1,\"orderBy\":\"timestamp\",\"where\":{\"id\":\"" + str(hex(int(params[0]))) + "\",\"rarity_in\":[0,1,2,3,4]}},\"query\":\"query GetCatgirls($first: Int, $skip: Int = 0, $orderBy: String, $orderDirection: String = asc, $where: Catgirl_filter) {\\n  catgirls(\\n    first: $first\\n    skip: $skip\\n    orderBy: $orderBy\\n    orderDirection: $orderDirection\\n    where: $where\\n  ) {\\n    id\\n    characterId\\n    season\\n    rarity\\n    nyaScore\\n    __typename\\n  }\\n}\\n\"}"
        except:
            await message.channel.send('Something went wrong, check catID or try again later')
            return

        try:
            response = requests.post(base_url, data=body, headers = head)
        except:
            await message.channel.send('Something went wrong, check catID or try again later')
            return
        
        print(response.text)
        catdata = json.loads(response.text)
        catstats = catdata["data"]["catgirls"][0]
        print("cat ID is = " + params[0])
        print("nyaScore = " + catstats["nyaScore"])
        print("rarity = " + catstats["rarity"])
        print("season = " + catstats["season"])
        print("character = " + catstats["characterId"])
        kittyname = "Not Found"
        catRarity = int(catstats["rarity"])
        catSeries = int(catstats["characterId"])
        if (catSeries == 0):
            if (catRarity== 0):
                kittyname = "Mae"
            elif (catRarity == 1):
                kittyname = "Kita"
            elif (catRarity == 2):
                kittyname = "Hana"
            elif (catRarity == 3):
                kittyname = "Celeste"
            elif (catRarity == 4):
                kittyname = "Mittsy"
        elif (catSeries == 1):
            if (catRarity == 0):
                kittyname = "Lisa"
            elif (catRarity == 1):
                kittyname = "Aoi"
            elif (catRarity == 2):
                kittyname = "Rin"
        else:
            kittyname = "Must be a new one"

        body = "{\"operationName\":\"GetCount\",\"variables\":{\"id\":\"" + (catstats["rarity"] +":" + catstats["characterId"]) + "\"},\"query\":\"query GetCount($id: String) {\\n  characterCount(id: $id) {\\n    id\\n    total\\n    __typename\\n  }\\n}\\n\"}"

        response2 = requests.post(base_url,
                data=body,
                headers = head
                )
        
        print(response2.text)
        catAmount = json.loads(response2.text)
        catCount = catAmount["data"]["characterCount"]['total']

        rarityStars = get_emoji(":star:") * (int(catstats["rarity"]) + 1)
        catinfo = "Catgirl {} has the following stats:\n".format(params[0]) + "Season: {}\n".format(catstats["season"]) + "Character: {}\n".format(kittyname) + "Rarity: {}\n".format(rarityStars) + "NyaScore: {}\n".format(catstats["nyaScore"] + "\n" + "Number of owners: {}\n".format(catCount))
                 
        await message.channel.send(catinfo)