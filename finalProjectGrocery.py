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
                aisles.append([vertex, nextVertex])

        return aisles

    def printGraph(self):
        print(f"Current Graph: {self.dictionary}")

    def dijkstra(self, start):

        distances = {vertex: float('infinity') for vertex in self.dictionary.keys()}

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
        return self.shoppingPath(aisles, frontPath, backPath, finalPath, visited, totalCost, check)


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

    numItems = random.randint(5, 10)

    index = 0

    groceryList = []

    while index < numItems:

        aisleChoice = random.choice(list(aisleItems))
        item = random.choice(list(aisleItems[aisleChoice]))

        if item not in groceryList:
            groceryList.append(item)
            index += 1

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

    divider()

    # Clones edges and optimal path for ease of use. ☺
    all = aisleLayout.printEdges()
    optimal = aisleLayout.shoppingPath(aisles)

    # Creates some lists to organize path sections. ☺
    firstTry = []
    secondTry = []
    thirdTry = []
    cannotDo = []
    replacements = []

    # Zips the list of aisles into lists of 2 consecutive aisles for path checking. ☺
    res = list(zip(optimal, optimal[1:] + optimal[:1]))
    for item in res:
        firstTry.append(list(item))

    for item in all:
        secondTry.append(item)

    for item in firstTry:
        if item in secondTry and item != ['Checkout', 'Entrance']:
            thirdTry.append(item)

    # List of path segments we can naturally complete. ☺
    print(f"Paths that can be achieved: {thirdTry}")

    for item in thirdTry:
        if item in firstTry and item != ['Checkout', 'Entrance']:
            firstTry.remove(item)

    cannotDo = firstTry

    # List of path segments that cannot be naturally completed. ☺
    print(f"Paths that cannot be achieved: {cannotDo}")

    divider()

    # Function to generate paths for the segments that currently cannot be traversed. ☺
    def pathGen(start, end, currentPath):

        currentPath.append(start)

        if start == end:
            # Path found between required start and end node. ☺
            print(f"Path found: {currentPath}")
            replacements.append(currentPath)
            return

        else:
            neighbors = []
            distances = []

            # Find all potential next neighbors from the start node.
            for i in all:
                if start in i:
                    for x in i:
                        if x is not start and x not in neighbors:
                            neighbors.append(x)

            # Compare all potential neighboring nodes' weights. ☺
            for potential in neighbors:
                for key in aisleLayout.dijkstra(potential):
                    if key is potential:
                        distances.append(
                            {key: aisleLayout.dijkstra(potential)[end] + aisleLayout.dijkstra(start)[potential]})

            chosen = None
            chosenDis = None

            # Determine next step in pathfinding function. ☺
            for pair in distances:

                if chosen is None:
                    chosen = list(pair.keys())[0]
                    chosenDis = list(pair.values())[0]

                elif int(list(pair.values())[0]) < chosenDis:
                    chosen = list(pair.keys())[0]
                    chosenDis = list(pair.values())[0]

            pathGen(chosen, end, currentPath)

    # Determine what path segments cannot be completed and then aim to solve them. ☺
    for neededPath in cannotDo:
        print(f"Path bust be found between {neededPath[0]} and {neededPath[1]}")
        pathGen(neededPath[0], neededPath[1], [])
        divider()

    shoppingPathClone = aisleLayout.shoppingPath(aisles)

    # Zip again. ☺
    res = list(zip(shoppingPathClone, shoppingPathClone[1:] + shoppingPathClone[:1]))

    cannotDo = [tuple(x) for x in cannotDo]

    # Format new path segments. ☺
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

    # Replace old path segments which cannot be completed with new segments that can be completed. ☺
    for elem in cleanPath:
        if elem != previous_value:
            finalPath.append(elem)
            previous_value = elem

    print(f"Final Path: {finalPath}")
