import itertools
import time
from typing import Tuple, List

import search
from scrape import scrapeForPuzzle, splitStringIntoGrid
from search import SolutionState, dfs


def loadWordList(path):
    with open(path, 'r') as f:
        return set([word.strip() for word in f.readlines()])

def filterNonWords(cartesianProducts, wordSet):
    filteredWords = []
    for characters in cartesianProducts:
        potentialWord = "".join(characters)
        potentialWord = potentialWord.lower()
        if potentialWord in wordSet:
            filteredWords.append(potentialWord)

    return filteredWords
def solve(grid):
    cartesianProducts = generateCartesianProduct(grid)
    wordSet = loadWordList('fiveLettersWords.txt')
    solutionList = filterNonWords(cartesianProducts, wordSet)

    solutionListForEachRow = []
    for i in range(len(grid)):
        solutionListForEachRow.append(getPotentialSolutionsForRow(grid, solutionList, i))

    root = SolutionState(solutionList, solutionListForEachRow)
    dfs(root)
    solutions = []
    for solution in search.solutionLists:
        solutions.append(solution.chosenSolutionList)
    return solutions

def filterForRemainingSolutions(chosenString, solutionList:List[str]):
    usedCharacterIndex = enumerateCharacterIndexFromString(chosenString)
    filteredSolution = solutionList

    for usedCharacterEntry in usedCharacterIndex:
        filteredSolution = filterOutUsedCharacters(filteredSolution, usedCharacterEntry)

    return filteredSolution

def enumerateCharacterIndexFromString(string):
    return [(char, index) for index, char in enumerate(string)]

def filterOutUsedCharacters(solutionList: List[str], usedCharactersIndex: Tuple[str, int]):
    char, index = usedCharactersIndex
    # Filter out strings where the character at the specified index does not match the given character
    filteredSolutions = [s for s in solutionList if len(s) > index and s[index] != char]
    return filteredSolutions

# Since the first letter of each row is already determined, we filter out all words that do not start with that letter
def getPotentialSolutionsForRow(grid, filteredWords, index) -> List[str]:
    firstCharacterInRow = grid[index][0].lower()
    rowSolutions = []

    for validWord in filteredWords:
        if firstCharacterInRow in validWord[0]:
            rowSolutions.append(validWord)
    return rowSolutions
def generateCartesianProduct(grid):
    allColumns = getAllColumn(grid)
    return list(itertools.product(*allColumns))

def getColumn(grid, index):
    return [row[index] for row in grid]

def getAllColumn(grid):
    return [getColumn(grid, i) for i in range(len(grid[0]))]


def solveTodaysPuzzle():
    puzzleGrid = scrapeForPuzzle()
    print("Puzzle grid:")
    print(puzzleGrid)
    correctSolutions = solve(puzzleGrid)
    print("Solutions:")
    return correctSolutions

if __name__ == '__main__':
    # print(solveTodaysPuzzle())

    message = """Press 1 or 2 to select an option:
1. Solve todays puzzle
2. Solve a custom puzzle
    """
    print(message)
    option = int(input())
    while option != 1 and option != 2:
        print("Invalid option. Please enter 1 or 2")
        option = int(input())

    if option == 1:
        print("Solving todays puzzle...")
        #Avoid potential loading issues with selenium
        time.sleep(1)
        print(solveTodaysPuzzle())
    elif option == 2:
        print("Enter the grid as a string, line by line. e.g sntar aluid ttosl uodwe mrark")
        string = input().replace(" ", "")
        grid = splitStringIntoGrid(string)
        print("Solutions:")
        print(solve(grid))
