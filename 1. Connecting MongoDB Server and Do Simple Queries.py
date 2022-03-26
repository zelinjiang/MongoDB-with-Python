from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint


# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('localhost:27017')
db=client.samples_pokemon
pokemons=db.samples_pokemon

print('========== First Query ==========')
# My birthday is Jun 2nd, so 06 + 02 = 8
for pokemon in pokemons.find({"candy_count": {"$gte": 8}}):
    pprint(pokemon['name'])


print('========== Second Query ==========')
# My birthday is Jun 2nd, so num == '006' or '002'
for pokemon in pokemons.find({"$or":[{"num":"006"},{"num":"002"}]}):
    pprint(pokemon['name'])

