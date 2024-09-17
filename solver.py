import itertools
from typing import Tuple, List

import search
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


if __name__ == '__main__':
    # grid = [
    #     ['S', 'E', 'I', 'F', 'R'],
    #     ['C', 'H', 'W', 'I', 'W'],
    #     ['A', 'T', 'A', 'E', 'T'],
    #     ['B', 'W', 'R', 'A', 'E'],
    #     ['W', 'O', 'E', 'L', 'Y']
    # ]

    grid = [
        ['S', 'N', 'T', 'A', 'R'],
        ['A', 'L', 'U', 'I', 'D'],
        ['T', 'T', 'O', 'S', 'L'],
        ['U', 'O', 'D', 'W', 'E'],
        ['M', 'R', 'A', 'R', 'K']
    ]
    solve(grid)

    correctSolutions = search.solutionLists

    for i in correctSolutions:
        print(i.chosenSolutionList)
