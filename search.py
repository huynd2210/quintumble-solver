import copy


class SolutionState:
    def __init__(self, remainingSolutionList, solutionListForEachRow, chosenSolutionList=None, gridLength=5):
        if chosenSolutionList is None:
            chosenSolutionList = []

        self.remainingSolutionList = remainingSolutionList
        self.solutionListForEachRow = solutionListForEachRow
        self.chosenSolutionList = chosenSolutionList
        self.gridLength = gridLength

    def __str__(self):
        return {
            "chosenSolutionList": self.chosenSolutionList,
            "remainingSolutionList": self.remainingSolutionList,
            "solutionListForEachRow": self.solutionListForEachRow
        }.__str__()

    def isSolutionFound(self):
        return len(self.chosenSolutionList) == self.gridLength


def chooseCandidate(currentState: SolutionState, solutionCandidate, candidateRowIndex):
    #Is solution candidate in row solution list?
    if solutionCandidate not in currentState.solutionListForEachRow[candidateRowIndex]:
        raise Exception("Solution candidate not in row solution list")
    from solver import filterForRemainingSolutions

    #Invalid candidate
    if solutionCandidate not in currentState.remainingSolutionList:
        return

    remainingSolution = filterForRemainingSolutions(solutionCandidate, currentState.remainingSolutionList)
    otherRows = copy.deepcopy(currentState.solutionListForEachRow)
    otherRows = otherRows[1:]

    chosenSolutionList = currentState.chosenSolutionList.copy()
    chosenSolutionList.append(solutionCandidate)

    return SolutionState(remainingSolution, otherRows, chosenSolutionList, currentState.gridLength)

def getNextStates(currentState: SolutionState):
    #Found the final solution
    if currentState.isSolutionFound():
        return currentState
    nextStates = []

    candidateRowIndex = 0
    for solutionCandidate in currentState.solutionListForEachRow[candidateRowIndex]:
        newState = chooseCandidate(currentState, solutionCandidate, candidateRowIndex)
        if newState is None:
            continue
        nextStates.append(newState)

    return nextStates

solutionLists = []
def dfs(currentState: SolutionState):
    if currentState.isSolutionFound():
        solutionLists.append(currentState)
        return
    nextStates = getNextStates(currentState)
    for newState in nextStates:
        dfs(newState)



