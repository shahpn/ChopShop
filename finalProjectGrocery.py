from cmath import inf
import random
import heapq


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
                # if {nextVertex, vertex} not in aisles:
                aisles.append([vertex, nextVertex])
        return aisles  # f"Graph Edges: {aisles}"

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
        # for i in reversed(travel):
        #
        #     if travel[i] == 0:
        #         continue
        #
        #     else:
        #
        #         if minDist > travel[i] and i not in visited and i in aisles:
        #             dest = i
        #             minDist = travel[i]
        #
        # visited.append(dest)
        #
        # # Update fun stats
        # backPath.insert(0, dest)
        # totalCost += minDist
        # check.pop(check.index(dest))

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
        if item not in groceryList:
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

    # print(aisleLayout.printEdges())

    all = aisleLayout.printEdges()
    optimal = aisleLayout.shoppingPath(aisles)
    # print(optimal)

    firstTry = []
    frozenFirst = []
    secondTry = []
    thirdTry = []
    frozenThird = []
    cannotDo = []
    moved = []
    replacements = []

    res = list(zip(optimal, optimal[1:] + optimal[:1]))
    for item in res:
        firstTry.append(list(item))

    for item in all:
        secondTry.append(item)

    # print(firstTry)
    # print(secondTry)
    for item in firstTry:
        if item in secondTry and item != ['Checkout', 'Entrance']:
            thirdTry.append(item)
    print(f"Paths that can be achieved: {thirdTry}")
    for item in thirdTry:
        if item in firstTry and item != ['Checkout', 'Entrance']:
            firstTry.remove(item)
    cannotDo = firstTry
    print(f"Paths that cannot be achieved: {cannotDo}")

    divider()


    def pathGen(start, end, currentPath):
        currentPath.append(start)
        if start == end:
            print(f"Path found: {currentPath}")
            replacements.append(currentPath)
            return
        else:
            # print(f"Starting with the vertex: {start}:")
            neighbors = []
            distances = []
            for i in all:
                if start in i:
                    for x in i:
                        if x is not start and x not in neighbors:
                            neighbors.append(x)
            # print(f"Which can go to the vertexes: {neighbors}")
            # print(f"We are currently at the distance {aisleLayout.dijkstra(start)[end]} from the goal.")
            for potential in neighbors:
                # distances.append(aisleLayout.dijkstra(potential)[end])
                for key in aisleLayout.dijkstra(potential):
                    if key is potential:
                        distances.append({key: aisleLayout.dijkstra(potential)[end] + aisleLayout.dijkstra(start)[potential]})
            chosen = None
            chosenDis = None
            for pair in distances:
                if chosen is None:
                    chosen = list(pair.keys())[0]
                    chosenDis = list(pair.values())[0]
                elif int(list(pair.values())[0]) < chosenDis:
                    chosen = list(pair.keys())[0]
                    chosenDis = list(pair.values())[0]
            # print(f"From the neighbors, here is the distances to our goal of {end}: {distances}")
            # print(f"To get closer to the goal, we choose to move to: {chosen}, which has a distance of: {chosenDis}")
            pathGen(chosen, end, currentPath)


    for neededPath in cannotDo:
        # if neededPath != ['Checkout', 'Entrance'] and neededPath != cannotDo[-1]:
        print(f"Path bust be found between {neededPath[0]} and {neededPath[1]}")
        # allDis1 = aisleLayout.dijkstra(neededPath[0])
        # print(allDis1)
        # dis = aisleLayout.dijkstra(neededPath[0])[neededPath[1]]
        # print(f"Current distance to {neededPath[1]}: {dis}")
        #
        # allDis2 = aisleLayout.dijkstra(neededPath[1])
        # print(allDis2)
        # dis2 = aisleLayout.dijkstra(neededPath[1])[neededPath[0]]
        # print(f"Current distance to {neededPath[0]}: {dis2}")
        #
        # combined = {}
        # for key, val in allDis1.items():
        #     newEntry = {key: val + allDis2[key]}
        #     combined.update(newEntry)
        #
        # print(f"Mediator aisled between {neededPath[0]} and {neededPath[1]}: {(sorted(combined.items(), key=lambda x: x[1]))}")
        #
        # divider()
        pathGen(neededPath[0], neededPath[1], [])
        divider()
    # for i in thirdTry:
    #     for x in i:
    #         if x not in frozenThird:
    #             frozenThird.append(x)
    # print(f"These elements should not be moved: {frozenThird}")
    # for i in firstTry:
    #     for x in i:
    #         if x not in frozenThird and x not in frozenFirst:
    #             frozenFirst.append(x)
    # print(f"These elements should be moved: {frozenFirst}")
    #
    # divider()
    #
    # for item in cannotDo:
    #     for item2 in all:
    #         # print(f"Edges from {item[1]}: {aisleLayout.dijkstra(item[1])}")
    #         if item[0] == item2[0]:
    #             if item2[1] in optimal and item2[1] not in frozenThird:
    #                 print(f"{item2[0]} can reach {item2[1]} which is in our required aisles.")
    #             # print(f"{item2[0]} can go to {item2[1]}")
    #             distances = aisleLayout.dijkstra(item2[0])
    #             # print(f"{item2[0]} is this far from other vertices: {distances}")
    #
    #     divider()

    shoppingPathClone = aisleLayout.shoppingPath(aisles)
    res = list(zip(shoppingPathClone, shoppingPathClone[1:] + shoppingPathClone[:1]))
    cannotDo = [tuple(x) for x in cannotDo]
    for i in res:
        if i in cannotDo:
            next1 = replacements.pop(0)
            res[res.index(i)] = next1

    if ['Checkout', 'Entrance'] in res:
        res.remove(['Checkout', 'Entrance'])

    print(f"Full Path: {res}")

    cleanPath = []
    for val in res:
        for inVal in val:
            cleanPath.append(inVal)

    print(f"Clean Path: {cleanPath}")

    previous_value = None
    finalPath = []

    for elem in cleanPath:
        if elem != previous_value:
            finalPath.append(elem)
            previous_value = elem

    print(f"Final Path: {finalPath}")
