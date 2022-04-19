from cmath import inf
from flask import Flask
import random
import heapq
import webpageText



app = Flask(__name__)
@app.route("/")
def siteRun():
    a = webpageText.home()
    return a

# @app.route("/")
# def home():
#     text = "Test page <h1>mommy<h1>"
#     return text

# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}"

# if __name__ == "__main__":
#     app.run()
app.run()

def divider():
    print("-------------------------")


def genAisleList(groceryList, aisleContents, requiredAisles=['Entrance'], i='Aisle 1'):
    # Base case, once the list is empty we have our aisles

    if len(groceryList) == 0:
        requiredAisles.append('Checkout')
        return requiredAisles

    # Checks first to see if the chosen aisle has any of the items on our list

    if len(set(aisleContents[i]).intersection(set(groceryList))) != 0:

        removeItems = set(aisleContents[i]).intersection(
            set(groceryList))  # List of items to remove from the grocery list
        requiredAisles.append(
            i)  # Adds the aisle to the list of places we NEED to see bc it's just so pretty and worth the money
        # temp = list(aisleContents)                                         # This was a dumb test ignore it

        # We now remove the items from our list that also exist in our current aisle

        for item in removeItems:
            groceryList.remove(item)

        # If we're at the end of our aisle, we do one last check. If we are at the end, returns our required MUST SEE aisles
        if i != 'Aisle 13':
            index = list(aisleContents)[list(aisleContents).index(i) + 1]
            return genAisleList(groceryList, aisleContents, requiredAisles, index)

        else:
            requiredAisles.append('Checkout')
            return requiredAisles


    # This is for when the aisle is a miserable failure with nothing that we want.
    # Does the same check for aisle 13 to avoid falling into the abyss

    else:
        if i != 'Aisle 13':
            index = list(aisleContents)[list(aisleContents).index(i) + 1]
            return genAisleList(groceryList, aisleContents, requiredAisles, index)

        else:
            requiredAisles.append('Checkout')
            return requiredAisles


class layout:

    def __init__(self, dictionary=None):
        if dictionary is None:
            dictionary = []
        self.dictionary = dictionary

    def printVertices(self):
        return f"Graph Vertices: {list(self.dictionary.keys())}"

    def printEdges(self):
        aisles = []
        for vertex in self.dictionary:
            for nextVertex in self.dictionary[vertex]:
                if {nextVertex, vertex} not in aisles:
                    aisles.append({vertex, nextVertex})
        return f"Graph Edges: {aisles}"

    def printGraph(self):
        print(f"Current Graph: {self.dictionary}")

    def dijkstra(self, start):

        distances = {vertex: float('infinity')
                     for vertex in self.dictionary.keys()}

        distances[start] = 0

        pq = [(0, start)]
        while len(pq) > 0:
            dist, v = heapq.heappop(pq)

            if dist > distances[v]:
                continue

            for path, cost in self.dictionary[v].items():
                distance = dist + cost

                if distance < distances[path]:
                    distances[path] = distance
                    heapq.heappush(pq, (distance, path))

        return distances

        # if longOutput:
        #     dists = []
        #     for vtx in self.dictionary.keys():
        #         dists.append(
        #             f"The distance between the {start} and the {vtx} is {distances[vtx]}.")
        #     return dists

        # else:
        #     dists = []
        #     for vtx in self.dictionary.keys():
        #         dists.append(f"{distances[vtx]}:{vtx}")
        #     return f"{start}{dists}"

        # for reqItem in groceryList:
        #     for aisle in aisleItems:
        #         for item in aisleItems[aisle]:
        #             if item == reqItem:
        #                 if aisle not in requiredAisles:
        #                     requiredAisles.append(aisle)
        #                     return self.genAisleList(groceryList, requiredAisles, index)

    def shoppingPath(self, aisles, frontPath=['Entrance'], backPath=['Checkout'], finalPath=[],
                     visited=['Entrance', 'Checkout'], totalCost=0, check=None):

        # Base case, checks to see if the required
        if (len(set(visited).intersection(set(aisles))) == len(aisles)):
            finalPath = frontPath + backPath
            return finalPath

        # Always reset this otherwise headaches ensue
        minDist = inf

        # Cheat code for headaches to be gone
        if check == None:
            check = aisles[:]

        # Use the dijkstra method to find distances from the front of the check list
        travel = self.dijkstra(check[0])

        # Now we search for the one closest to our current location
        for i in travel:

            # current = list(travel.keys())[list(travel).index(i)]

            # Skips iteration if we're looking at the node we're already standing on
            if travel[i] == 0:
                continue

            else:

                # Updates the total cost, the distance, and makes sure the location is both in our required lists and also not already visited
                if minDist > travel[i] and i not in visited and i in aisles:
                    dest = i
                    minDist = travel[i]

        visited.append(dest)

        # Update some stats and remove unnecesary locations
        frontPath.append(dest)
        totalCost += minDist
        check.pop(check.index(dest))

        # Resest for HEADACHES
        minDist = inf

        if (len(set(visited).intersection(set(aisles))) == len(aisles)):
            finalPath = frontPath + backPath
            return finalPath

        # Use dijkstra again but this time backward, ask me when I've slept why. !!!!REASONING COULD BE DUMB AND NOT RIGHT!!!!
        travel = self.dijkstra(check[-1])

        # Traverses the aisles backward because I'm quirky. Note: I'm now realizing I probably didn't have to do this.
        # Does the same thing as the first loop, just for the back of the check list.
        for i in reversed(travel):

            if travel[i] == 0:
                continue

            else:

                if minDist > travel[i] and i not in visited and i in aisles:
                    dest = i
                    minDist = travel[i]

        visited.append(dest)

        # Update fun stats
        backPath.insert(0, dest)
        totalCost += minDist
        check.pop(check.index(dest))

        # ANOTHA ONE
        return self.shoppingPath(aisles, frontPath, backPath,
                                 finalPath, visited, totalCost, check)

        # Iterates through our required super special photogenic aisles
        # for i in requiredAisles:

        #     # Returns if
        #     if (len(frontPath) + len(backPath) == len(requiredAisles)):
        #         finalPath = frontPath.append(backPath)
        #         break

        #     else:

        #         minDist = inf

        #         travel = self.dijkstra(requiredAisles[requiredAisles.index(i)])

        #         for i in travel:

        #             # current = list(travel.keys())[list(travel).index(i)]

        #             if travel[i] == 0:
        #                 continue

        #             else:

        #                 if minDist > travel[i] and i not in visited:
        #                     dest = i
        #                     minDist = travel[i]

        #         frontPath.append(dest)
        #         totalCost += minDist

        #         if (len(frontPath) + len(backPath) == len(requiredAisles)):
        #             finalPath = frontPath.append(backPath)
        #             break

        #         minDist = inf

        #         travel = self.dijkstra(requiredAisles[requiredAisles.index(i)])

        #         for i in reversed(travel):

        #             # current = list(travel.keys())[list(travel).index(i)]

        #             if travel[i] == 0:
        #                 continue

        #             else:

        #                 if minDist > travel[i] and i not in visited:
        #                     dest = i
        #                     minDist = travel[i]

        # return finalPath

        # dist = self.dijkstra('Aisle 2')
        # print(dist)
        # formattedDistances = []

        # for item in dist:
        #     formattedDistances.append(item[:-1])

        # formattedDistances.sort(key=lambda x: int(x.split()[-1]))
        # # print(formattedDistances)
        # closestLocations = []

        # for item in formattedDistances:
        #     closestLocations.append(item.split(' is')[0].split("and the ", 1)[1])
        #     print(dist)


if __name__ == '__main__':
    divider()

    aisleLayout = layout({
        'Entrance': {'Aisle 1': 2, 'Aisle 2': 4, 'Aisle 3': 6, 'Aisle 4': 9, 'Checkout': 8},
        'Aisle 1': {'Aisle 5': 2, 'Aisle 2': 2, 'Entrance': 2, 'Checkout': 9},
        'Aisle 2': {'Aisle 1': 2, 'Aisle 6': 2, 'Aisle 3': 2, 'Entrance': 4, 'Checkout': 7},
        'Aisle 3': {'Aisle 2': 2, 'Aisle 7': 2, 'Aisle 3': 4, 'Entrance': 6, 'Checkout': 5},
        'Aisle 4': {'Aisle 3': 2, 'Aisle 8': 2, 'Entrance': 9, 'Checkout': 2},
        'Aisle 5': {'Aisle 1': 2, 'Aisle 6': 2, 'Aisle 9': 2},
        'Aisle 6': {'Aisle 5': 2, 'Aisle 2': 2, 'Aisle 7': 2, 'Aisle 10': 2},
        'Aisle 7': {'Aisle 6': 2, 'Aisle 3': 2, 'Aisle 8': 2, 'Aisle 11': 2},
        'Aisle 8': {'Aisle 7': 2, 'Aisle 4': 2, 'Aisle 12': 2},
        'Aisle 9': {'Aisle 5': 2, 'Aisle 10': 2, 'Aisle 13': 4},
        'Aisle 10': {'Aisle 9': 2, 'Aisle 6': 2, 'Aisle 11': 2, 'Aisle 13': 3},
        'Aisle 11': {'Aisle 10': 2, 'Aisle 7': 2, 'Aisle 12': 2, 'Aisle 13': 3},
        'Aisle 12': {'Aisle 11': 2, 'Aisle 8': 2, 'Aisle 13': 4},
        'Aisle 13': {'Aisle 9': 4, 'Aisle 10': 3, 'Aisle 11': 3, 'Aisle 12': 4},
        'Checkout': {'Entrance': 8, 'Aisle 4': 2, 'Aisle 3': 5, 'Aisle 2': 7}
    })

    aisleItems = {
        'Aisle 1': {'Spaghetti', 'Rigatoni', 'Macaroni', 'Penne', 'Pasta Sauce', 'Meatballs'},
        'Aisle 2': {'Coke', 'Sprite', 'Dr. Pepper', 'Fanta', 'Root Beer', 'Ginger Ale'},
        'Aisle 3': {'White Bread', 'Rye Bread', 'Wheat Bread', 'Pumpernickel Bread'},
        'Aisle 4': {'Apples', 'Bananas', 'Grapes', 'Oranges', 'Pineapples', 'Carrots', 'Lettuce', 'Celery', 'Cucumbers',
                    'Asparagus', 'Broccoli', 'Cauliflower'},
        'Aisle 5': {'Bottled Water', 'Purified Water', 'Sparkling Water', 'Mineral Water'},
        'Aisle 6': {'Apple Juice', 'Grape Juice', 'Orange Juice', 'Pineapple Juice', 'Prune Juice'},
        'Aisle 7': {'Beans', 'Chicken Noodle Soup', 'Sardines', 'Green Beans', 'Peas', 'Beef Stew'},
        'Aisle 8': {'Saffron', 'Paprika', 'Cayenne', 'Turmeric', 'Thyme', 'Oregano', 'Ginger', 'Cumin', 'Salt',
                    'Black Pepper'},
        'Aisle 9': {'Prescription Drugs', 'Nonprescription Drugs', 'Vitamins', 'Minerals'},
        'Aisle 10': {'Shampoo', 'Conditioner', 'Lotion', 'Toothpaste', 'Toothbrushes', 'Soap', 'Deodorant',
                     'Hairspray'},
        'Aisle 11': {'Candy', 'Chips', 'Chocolate', 'Cookies', 'Popcorn', 'Pretzels'},
        'Aisle 12': {'Milk', 'Cheese', 'Butter', 'Eggs', 'Yogurt'},
        'Aisle 13': {'Ice Cream', 'Frozen Vegetables', 'Frozen Meats', 'Frozen Pizza', 'Frozen Fruit'}
    }

    # Testing things because I'm a dumbass
    # test = 'Aisle 1'
    # # test2 = aisleItems[test][random.choice(list(aisleItems[test]))]
    # test3 = random.choice(list(aisleItems[test]))

    # print(test)
    # print(test3)

    # print(aisleItems)

    numItems = random.randint(5, 10)

    index = 0

    groceryList = []

    while index < numItems:
        aisleChoice = random.choice(list(aisleItems))
        item = random.choice(list(aisleItems[aisleChoice]))
        groceryList.append(item)
        index += 1

    #########################
    #   SEE GENAISLELIST    #
    #########################

    # requiredAisles = []
    # for reqItem in groceryList:
    #     for aisle in aisleItems:
    #        for item in aisleItems[aisle]:
    #             if item == reqItem:
    #                 if aisle not in requiredAisles:
    #                     requiredAisles.append(aisle)
    #                     continue

    # print(len(aisleItems['Aisle 1'].intersection(groceryList)))

    # print(genAisleList(groceryList, aisleItems))

    print()
    print("The items we need are:")
    print()
    print(groceryList)
    aisles = genAisleList(groceryList, aisleItems)
    print()
    print("These items are in:")
    print()
    print(aisles)
    print()
    print("The best path through is:")
    print()
    print(aisleLayout.shoppingPath(aisles))
    print()
    # print("The total cost was:")
    # print()
    # print()

    divider()

