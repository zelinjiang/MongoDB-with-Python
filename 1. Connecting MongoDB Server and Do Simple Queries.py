from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint


# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient('localhost:27017')
db=client.samples_pokemon
pokemons=db.samples_pokemon

print('========== First Query ==========')
# Write a query and return the Pokemons that have candycount equal to the sum of month and date of your birthday
# My birthday is Jun 2nd, so 06 + 02 = 8
for pokemon in pokemons.find({"candy_count": {"$gte": 8}}):
    pprint(pokemon['name'])


print('========== Second Query ==========')
# Return the Pokemon that have 'num' equal to the month or date of your birthday
# My birthday is Jun 2nd, so num == '006' or '002'
for pokemon in pokemons.find({"$or":[{"num":"006"},{"num":"002"}]}):
    pprint(pokemon['name'])

