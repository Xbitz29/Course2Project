import numpy as np
from PIL import Image
import networkx as nx
from networkx.algorithms import isomorphism
import sys
import pygame
from pygame.constants import QUIT, K_ESCAPE, KEYDOWN


def load(i):
    try:
        img = Image.open(f"{i}.png")
    except:
        raise Exception("Cannot open picture's file")

    arr = np.array(img)
    data = np.empty(shape=(arr.shape[0], arr.shape[1]), dtype="bool")
    for row in range(data.shape[0]):
        for column in range(data.shape[1]):
            if arr[row, column].sum() <= 255:
                data[row, column] = True
            else:
                data[row, column] = False
    # height, width = data.shape
    return data


def tograph(data):
    pixels = data.shape[0] * data.shape[1]
    graph1 = np.empty(shape=(pixels, pixels), dtype="int")
    for row in range(graph1.shape[0]):
        for column in range(graph1.shape[1]):
            graph1[row, column] = 0
    isvertex = [0] * pixels
    deg1 = [0] * pixels
    for row in range(data.shape[0]):
        for column in range(data.shape[1]):
            if data[row, column]:
                isvertex[row * data.shape[1] + column] = 1
                if (column > 0) and (isvertex[row * data.shape[1] + column - 1]):
                    graph1[row * data.shape[1] + column - 1, row * data.shape[1] + column] = 1
                    deg1[row * data.shape[1] + column - 1] += 1
                    graph1[row * data.shape[1] + column, row * data.shape[1] + column - 1] = 1
                    deg1[row * data.shape[1] + column] += 1
                if (row > 0) and (column < data.shape[1] - 1) and (isvertex[(row - 1) * data.shape[1] + column + 1]):
                    graph1[(row - 1) * data.shape[1] + column + 1, row * data.shape[1] + column] = 1
                    deg1[(row - 1) * data.shape[1] + column + 1] += 1
                    graph1[row * data.shape[1] + column, (row - 1) * data.shape[1] + column + 1] = 1
                    deg1[row * data.shape[1] + column] += 1
                if (row > 0) and (isvertex[(row - 1) * data.shape[1] + column]):
                    graph1[(row - 1) * data.shape[1] + column, row * data.shape[1] + column] = 1
                    deg1[(row - 1) * data.shape[1] + column] += 1
                    graph1[row * data.shape[1] + column, (row - 1) * data.shape[1] + column] = 1
                    deg1[row * data.shape[1] + column] += 1
                if (row > 0) and (column > 0) and (isvertex[(row - 1) * data.shape[1] + column - 1]):
                    graph1[(row - 1) * data.shape[1] + column - 1, row * data.shape[1] + column] = 1
                    deg1[(row - 1) * data.shape[1] + column - 1] += 1
                    graph1[row * data.shape[1] + column, (row - 1) * data.shape[1] + column - 1] = 1
                    deg1[row * data.shape[1] + column] += 1

    for i in range(pixels):
        if deg1[i] == 8:
            deg1[i] = 0
            isvertex[i] = 0
            if (i > data.shape[1] - 1) and (i % data.shape[1] > 0):
                graph1[i - data.shape[1] - 1, i] = 0
                graph1[i, i - data.shape[1] - 1] = 0
                deg1[i - data.shape[1] - 1] -= 1
            if i > data.shape[1] - 1:
                graph1[i - data.shape[1], i] = 0
                graph1[i, i - data.shape[1]] = 0
                deg1[i - data.shape[1]] -= 1
            if (i > data.shape[1] - 1) and (i % data.shape[1] < data.shape[1] - 1):
                graph1[i - data.shape[1] + 1, i] = 0
                graph1[i, i - data.shape[1] + 1] = 0
                deg1[i - data.shape[1] + 1] -= 1
            if i % data.shape[1] > 0:
                graph1[i - 1, i] = 0
                graph1[i, i - 1] = 0
                deg1[i - 1] -= 1
            if i % data.shape[1] < data.shape[1] - 1:
                graph1[i + 1, i] = 0
                graph1[i, i + 1] = 0
                deg1[i + 1] -= 1
            if (i < pixels - data.shape[1]) and (i % data.shape[1] > 0):
                graph1[i + data.shape[1] - 1, i] = 0
                graph1[i, i + data.shape[1] - 1] = 0
                deg1[i + data.shape[1] - 1] -= 1
            if i < pixels - data.shape[1]:
                graph1[i + data.shape[1], i] = 0
                graph1[i, i + data.shape[1]] = 0
                deg1[i + data.shape[1]] -= 1
            if (i < pixels - data.shape[1]) and (i % data.shape[1] < data.shape[1] - 1):
                graph1[i + data.shape[1] + 1, i] = 0
                graph1[i, i + data.shape[1] + 1] = 0
                deg1[i + data.shape[1] + 1] -= 1

    for i in range(pixels):
        row = i // data.shape[1]
        column = i % data.shape[1]
        if (0 < column) and (column < data.shape[1] - 1) and (0 < row) and (row < data.shape[0] - 1):
            if (data[row - 1, column]) and (data[row, column - 1]) and (data[row, column + 1]) \
                    and (data[row + 1, column]):
                if (data[row - 1, column - 1]) and (data[row - 1, column + 1]) and (data[row + 1, column - 1]) \
                        and (not data[row + 1, column + 1]):
                    deg1[i] = 0
                    isvertex[i] = 0
                    if graph1[i, i - data.shape[1] - 1] == 1:
                        deg1[i - data.shape[1] - 1] -= 1
                    graph1[i - data.shape[1] - 1, i] = 0
                    graph1[i, i - data.shape[1] - 1] = 0
                    if graph1[i, i - data.shape[1]] == 1:
                        deg1[i - data.shape[1]] -= 1
                    graph1[i - data.shape[1], i] = 0
                    graph1[i, i - data.shape[1]] = 0
                    if graph1[i, i - data.shape[1] + 1] == 1:
                        deg1[i - data.shape[1] + 1] -= 1
                    graph1[i - data.shape[1] + 1, i] = 0
                    graph1[i, i - data.shape[1] + 1] = 0
                    if graph1[i, i - 1] == 1:
                        deg1[i - 1] -= 1
                    graph1[i - 1, i] = 0
                    graph1[i, i - 1] = 0
                    if graph1[i, i + 1] == 1:
                        deg1[i + 1] -= 1
                    graph1[i + 1, i] = 0
                    graph1[i, i + 1] = 0
                    if graph1[i, i + data.shape[1] - 1] == 1:
                        deg1[i + data.shape[1] - 1] -= 1
                    graph1[i + data.shape[1] - 1, i] = 0
                    graph1[i, i + data.shape[1] - 1] = 0
                    if graph1[i, i + data.shape[1]] == 1:
                        deg1[i + data.shape[1]] -= 1
                    graph1[i + data.shape[1], i] = 0
                    graph1[i, i + data.shape[1]] = 0
                    if graph1[i, i + data.shape[1] + 1] == 1:
                        deg1[i + data.shape[1] + 1] -= 1
                    graph1[i + data.shape[1] + 1, i] = 0
                    graph1[i, i + data.shape[1] + 1] = 0
                if (data[row - 1, column - 1]) and (data[row - 1, column + 1]) and (not data[row + 1, column - 1]) \
                        and (data[row + 1, column + 1]):
                    deg1[i] = 0
                    isvertex[i] = 0
                    if graph1[i, i - data.shape[1] - 1] == 1:
                        deg1[i - data.shape[1] - 1] -= 1
                    graph1[i - data.shape[1] - 1, i] = 0
                    graph1[i, i - data.shape[1] - 1] = 0
                    if graph1[i, i - data.shape[1]] == 1:
                        deg1[i - data.shape[1]] -= 1
                    graph1[i - data.shape[1], i] = 0
                    graph1[i, i - data.shape[1]] = 0
                    if graph1[i, i - data.shape[1] + 1] == 1:
                        deg1[i - data.shape[1] + 1] -= 1
                    graph1[i - data.shape[1] + 1, i] = 0
                    graph1[i, i - data.shape[1] + 1] = 0
                    if graph1[i, i - 1] == 1:
                        deg1[i - 1] -= 1
                    graph1[i - 1, i] = 0
                    graph1[i, i - 1] = 0
                    if graph1[i, i + 1] == 1:
                        deg1[i + 1] -= 1
                    graph1[i + 1, i] = 0
                    graph1[i, i + 1] = 0
                    if graph1[i, i + data.shape[1] - 1] == 1:
                        deg1[i + data.shape[1] - 1] -= 1
                    graph1[i + data.shape[1] - 1, i] = 0
                    graph1[i, i + data.shape[1] - 1] = 0
                    if graph1[i, i + data.shape[1]] == 1:
                        deg1[i + data.shape[1]] -= 1
                    graph1[i + data.shape[1], i] = 0
                    graph1[i, i + data.shape[1]] = 0
                    if graph1[i, i + data.shape[1] + 1] == 1:
                        deg1[i + data.shape[1] + 1] -= 1
                    graph1[i + data.shape[1] + 1, i] = 0
                    graph1[i, i + data.shape[1] + 1] = 0
                if (data[row - 1, column - 1]) and (not data[row - 1, column + 1]) and (data[row + 1, column - 1]) \
                        and (data[row + 1, column + 1]):
                    deg1[i] = 0
                    isvertex[i] = 0
                    if graph1[i, i - data.shape[1] - 1] == 1:
                        deg1[i - data.shape[1] - 1] -= 1
                    graph1[i - data.shape[1] - 1, i] = 0
                    graph1[i, i - data.shape[1] - 1] = 0
                    if graph1[i, i - data.shape[1]] == 1:
                        deg1[i - data.shape[1]] -= 1
                    graph1[i - data.shape[1], i] = 0
                    graph1[i, i - data.shape[1]] = 0
                    if graph1[i, i - data.shape[1] + 1] == 1:
                        deg1[i - data.shape[1] + 1] -= 1
                    graph1[i - data.shape[1] + 1, i] = 0
                    graph1[i, i - data.shape[1] + 1] = 0
                    if graph1[i, i - 1] == 1:
                        deg1[i - 1] -= 1
                    graph1[i - 1, i] = 0
                    graph1[i, i - 1] = 0
                    if graph1[i, i + 1] == 1:
                        deg1[i + 1] -= 1
                    graph1[i + 1, i] = 0
                    graph1[i, i + 1] = 0
                    if graph1[i, i + data.shape[1] - 1] == 1:
                        deg1[i + data.shape[1] - 1] -= 1
                    graph1[i + data.shape[1] - 1, i] = 0
                    graph1[i, i + data.shape[1] - 1] = 0
                    if graph1[i, i + data.shape[1]] == 1:
                        deg1[i + data.shape[1]] -= 1
                    graph1[i + data.shape[1], i] = 0
                    graph1[i, i + data.shape[1]] = 0
                    if graph1[i, i + data.shape[1] + 1] == 1:
                        deg1[i + data.shape[1] + 1] -= 1
                    graph1[i + data.shape[1] + 1, i] = 0
                    graph1[i, i + data.shape[1] + 1] = 0
                if (not data[row - 1, column - 1]) and (data[row - 1, column + 1]) and (data[row + 1, column - 1]) \
                        and (data[row + 1, column + 1]):
                    deg1[i] = 0
                    isvertex[i] = 0
                    if graph1[i, i - data.shape[1] - 1] == 1:
                        deg1[i - data.shape[1] - 1] -= 1
                    graph1[i - data.shape[1] - 1, i] = 0
                    graph1[i, i - data.shape[1] - 1] = 0
                    if graph1[i, i - data.shape[1]] == 1:
                        deg1[i - data.shape[1]] -= 1
                    graph1[i - data.shape[1], i] = 0
                    graph1[i, i - data.shape[1]] = 0
                    if graph1[i, i - data.shape[1] + 1] == 1:
                        deg1[i - data.shape[1] + 1] -= 1
                    graph1[i - data.shape[1] + 1, i] = 0
                    graph1[i, i - data.shape[1] + 1] = 0
                    if graph1[i, i - 1] == 1:
                        deg1[i - 1] -= 1
                    graph1[i - 1, i] = 0
                    graph1[i, i - 1] = 0
                    if graph1[i, i + 1] == 1:
                        deg1[i + 1] -= 1
                    graph1[i + 1, i] = 0
                    graph1[i, i + 1] = 0
                    if graph1[i, i + data.shape[1] - 1] == 1:
                        deg1[i + data.shape[1] - 1] -= 1
                    graph1[i + data.shape[1] - 1, i] = 0
                    graph1[i, i + data.shape[1] - 1] = 0
                    if graph1[i, i + data.shape[1]] == 1:
                        deg1[i + data.shape[1]] -= 1
                    graph1[i + data.shape[1], i] = 0
                    graph1[i, i + data.shape[1]] = 0
                    if graph1[i, i + data.shape[1] + 1] == 1:
                        deg1[i + data.shape[1] + 1] -= 1
                    graph1[i + data.shape[1] + 1, i] = 0
                    graph1[i, i + data.shape[1] + 1] = 0

    for row in range(data.shape[0]):
        for column in range(data.shape[1]):
            if isvertex[row * data.shape[1] + column]:
                if (row > 0) and (column > 0) and (isvertex[row * data.shape[1] + column - 1]) \
                        and (isvertex[(row - 1) * data.shape[1] + column]):
                    graph1[(row - 1) * data.shape[1] + column, row * data.shape[1] + column - 1] = 0
                    deg1[(row - 1) * data.shape[1] + column] -= 1
                    graph1[row * data.shape[1] + column - 1, (row - 1) * data.shape[1] + column] = 0
                    deg1[row * data.shape[1] + column - 1] -= 1
                if (row > 0) and (column < data.shape[1] - 1) and (isvertex[(row - 1) * data.shape[1] + column]) \
                        and (isvertex[(row - 1) * data.shape[1] + column + 1]):
                    graph1[(row - 1) * data.shape[1] + column + 1, row * data.shape[1] + column] = 0
                    deg1[(row - 1) * data.shape[1] + column + 1] -= 1
                    graph1[row * data.shape[1] + column, (row - 1) * data.shape[1] + column + 1] = 0
                    deg1[row * data.shape[1] + column] -= 1
                if (row > 0) and (column > 0) and (isvertex[row * data.shape[1] + column - 1]) \
                        and (isvertex[(row - 1) * data.shape[1] + column - 1]):
                    graph1[(row - 1) * data.shape[1] + column - 1, row * data.shape[1] + column] = 0
                    deg1[(row - 1) * data.shape[1] + column - 1] -= 1
                    graph1[row * data.shape[1] + column, (row - 1) * data.shape[1] + column - 1] = 0
                    deg1[row * data.shape[1] + column] -= 1
                if (row > 0) and (column > 0) and (isvertex[(row - 1) * data.shape[1] + column]) \
                        and (isvertex[(row - 1) * data.shape[1] + column - 1]):
                    graph1[(row - 1) * data.shape[1] + column - 1, row * data.shape[1] + column] = 0
                    deg1[(row - 1) * data.shape[1] + column - 1] -= 1
                    graph1[row * data.shape[1] + column, (row - 1) * data.shape[1] + column - 1] = 0
                    deg1[row * data.shape[1] + column] -= 1

    isvertex1 = np.empty(shape=(data.shape[0], data.shape[1]), dtype="int")
    for row in range(isvertex1.shape[0]):
        for column in range(isvertex1.shape[1]):
            isvertex1[row, column] = 0
    for row in range(data.shape[0]):
        for column in range(data.shape[1]):
            if isvertex[row * data.shape[1] + column]:
                if deg1[row * data.shape[1] + column] == 0:
                    isvertex1[row, column] = 1
                if (column < data.shape[1] - 1) and ((column == 0 and isvertex[row * data.shape[1] + column + 1])
                                                     or ((column > 0)
                                                         and (isvertex[row * data.shape[1] + column - 1] == 0)
                                                         and (isvertex[row * data.shape[1] + column + 1] == 1))
                                                     or (isvertex1[row, column]
                                                         and isvertex[row * data.shape[1] + column + 1] == 1)):
                    isvertex1[row, column] = 1
                    i = column
                    maxi = data.shape[1] - 1
                    while (i < maxi) and (isvertex[row * data.shape[1] + i + 1]):
                        if i + 1 == maxi:
                            isvertex1[row, i + 1] = 1
                            graph1[row * data.shape[1] + i + 1, row * data.shape[1] + column] = 2
                            graph1[row * data.shape[1] + column, row * data.shape[1] + i + 1] = 2
                            break
                        elif deg1[row * data.shape[1] + i + 1] > 2:
                            isvertex1[row, i + 1] = 1
                            graph1[row * data.shape[1] + i + 1, row * data.shape[1] + column] = 2
                            graph1[row * data.shape[1] + column, row * data.shape[1] + i + 1] = 2
                            break
                        elif isvertex[row * data.shape[1] + i + 2] == 0:
                            isvertex1[row, i + 1] = 1
                            graph1[row * data.shape[1] + i + 1, row * data.shape[1] + column] = 2
                            graph1[row * data.shape[1] + column, row * data.shape[1] + i + 1] = 2
                            break
                        i += 1

    for row in range(data.shape[0]):
        for column in range(data.shape[1]):
            if isvertex[row * data.shape[1] + column]:
                if (row < data.shape[0] - 1) and ((row == 0 and isvertex[(row + 1) * data.shape[1] + column])
                                                  or ((row > 0) and (isvertex[(row - 1) * data.shape[1] + column] == 0)
                                                      and (isvertex[(row + 1) * data.shape[1] + column] == 1))
                                                  or (isvertex1[row, column]
                                                      and isvertex[(row + 1) * data.shape[1] + column] == 1)):
                    isvertex1[row, column] = 1
                    i = row
                    maxi = data.shape[0] - 1
                    while (i < maxi) and (isvertex[(i + 1) * data.shape[1] + column]):
                        if i + 1 == maxi:
                            isvertex1[i + 1, column] = 1
                            graph1[(i + 1) * data.shape[1] + column, row * data.shape[1] + column] = 2
                            graph1[row * data.shape[1] + column, (i + 1) * data.shape[1] + column] = 2
                            break
                        elif deg1[(i + 1) * data.shape[1] + column] > 2:
                            isvertex1[i + 1, column] = 1
                            graph1[(i + 1) * data.shape[1] + column, row * data.shape[1] + column] = 2
                            graph1[row * data.shape[1] + column, (i + 1) * data.shape[1] + column] = 2
                            break
                        elif isvertex[(i + 2) * data.shape[1] + column] == 0:
                            isvertex1[i + 1, column] = 1
                            graph1[(i + 1) * data.shape[1] + column, row * data.shape[1] + column] = 2
                            graph1[row * data.shape[1] + column, (i + 1) * data.shape[1] + column] = 2
                            break
                        i += 1
    for row in range(data.shape[0]):
        for column in range(data.shape[1]):
            if isvertex[row * data.shape[1] + column]:
                if (column < data.shape[1] - 1) and (row < data.shape[0] - 1) \
                        and (((column == 0 or row == 0)
                              and (graph1[row * data.shape[1] + column, (row + 1) * data.shape[1] + column + 1] == 1))
                             or ((column > 0 and row > 0)
                                 and (graph1[row * data.shape[1] + column, (row - 1) * data.shape[1] + column - 1] == 0)
                                 and (graph1[
                                          row * data.shape[1] + column, (row + 1) * data.shape[1] + column + 1] == 1))
                             or (isvertex1[row, column]
                                 and graph1[
                                     row * data.shape[1] + column, (row + 1) * data.shape[1] + column + 1] == 1)):
                    isvertex1[row, column] = 1
                    i = row
                    j = column
                    maxi = data.shape[0] - 1
                    maxj = data.shape[1] - 1
                    while (i < maxi and j < maxj) and (
                            graph1[i * data.shape[1] + j, (i + 1) * data.shape[1] + j + 1] == 1):
                        if (i + 1 == maxi) or (j + 1 == maxj):
                            isvertex1[i + 1, j + 1] = 1
                            graph1[(i + 1) * data.shape[1] + j + 1, row * data.shape[1] + column] = 2
                            graph1[row * data.shape[1] + column, (i + 1) * data.shape[1] + j + 1] = 2
                            break
                        elif deg1[(i + 1) * data.shape[1] + j + 1] > 2:
                            isvertex1[i + 1, j + 1] = 1
                            graph1[(i + 1) * data.shape[1] + j + 1, row * data.shape[1] + column] = 2
                            graph1[row * data.shape[1] + column, (i + 1) * data.shape[1] + j + 1] = 2
                            break
                        elif graph1[(i + 1) * data.shape[1] + j + 1, (i + 2) * data.shape[1] + j + 2] == 0:
                            isvertex1[i + 1, j + 1] = 1
                            graph1[(i + 1) * data.shape[1] + j + 1, row * data.shape[1] + column] = 2
                            graph1[row * data.shape[1] + column, (i + 1) * data.shape[1] + j + 1] = 2
                            break
                        i += 1
                        j += 1
    for row in range(data.shape[0]):
        for column in range(data.shape[1]):
            if isvertex[row * data.shape[1] + column]:
                if (column > 0) and (row < data.shape[0] - 1) \
                        and (((column == data.shape[1] - 1 or row == 0)
                              and (graph1[row * data.shape[1] + column, (row + 1) * data.shape[1] + column - 1] == 1))
                             or ((column < data.shape[1] - 1 and row > 0)
                                 and (graph1[row * data.shape[1] + column, (row - 1) * data.shape[1] + column + 1] == 0)
                                 and (graph1[
                                          row * data.shape[1] + column, (row + 1) * data.shape[1] + column - 1] == 1))
                             or (isvertex1[row, column]
                                 and graph1[
                                     row * data.shape[1] + column, (row + 1) * data.shape[1] + column - 1] == 1)):
                    isvertex1[row, column] = 1
                    i = row
                    j = column
                    maxi = data.shape[0] - 1
                    minj = 0
                    while (i < maxi and j > minj) and (
                            graph1[i * data.shape[1] + j, (i + 1) * data.shape[1] + j - 1] == 1):
                        if (i + 1 == maxi) or (j - 1 == minj):
                            isvertex1[i + 1, j - 1] = 1
                            graph1[(i + 1) * data.shape[1] + j - 1, row * data.shape[1] + column] = 2
                            graph1[row * data.shape[1] + column, (i + 1) * data.shape[1] + j - 1] = 2
                            break
                        elif deg1[(i + 1) * data.shape[1] + j - 1] > 2:
                            isvertex1[i + 1, j - 1] = 1
                            graph1[(i + 1) * data.shape[1] + j - 1, row * data.shape[1] + column] = 2
                            graph1[row * data.shape[1] + column, (i + 1) * data.shape[1] + j - 1] = 2
                            break
                        elif graph1[(i + 1) * data.shape[1] + j - 1, (i + 2) * data.shape[1] + j - 2] == 0:
                            isvertex1[i + 1, j - 1] = 1
                            graph1[(i + 1) * data.shape[1] + j - 1, row * data.shape[1] + column] = 2
                            graph1[row * data.shape[1] + column, (i + 1) * data.shape[1] + j - 1] = 2
                            break
                        i += 1
                        j -= 1

    v_amount = 0
    for row in range(isvertex1.shape[0]):
        for column in range(isvertex1.shape[1]):
            if isvertex1[row, column] == 1:
                v_amount += 1
    coordinates = np.empty(shape=(v_amount, 2), dtype="int")
    i = 0
    for row in range(isvertex1.shape[0]):
        for column in range(isvertex1.shape[1]):
            if isvertex1[row, column] == 1:
                coordinates[i, 0] = row  # ИСПРАВИТЬ
                coordinates[i, 1] = column
                isvertex1[row, column] = i + 1
                i += 1
    graph = np.empty(shape=(v_amount, v_amount), dtype="int")
    for row in range(graph.shape[0]):
        for column in range(graph.shape[1]):
            graph[row, column] = 0
    for n in range(v_amount):
        i = coordinates[n, 0]
        j = coordinates[n, 1]
        for m in range(i * data.shape[1] + j, pixels):
            if graph1[i * data.shape[1] + j, m] == 2:
                graph[n, isvertex1[m // data.shape[1], m % data.shape[1]] - 1] = 1
                graph[isvertex1[m // data.shape[1], m % data.shape[1]] - 1, n] = 1
    return coordinates, graph


def isomorph(graph, graph1, coordinates1):
    g = nx.Graph()
    for i in range(graph.shape[0]):
        g.add_node(i)
    for i in range(graph.shape[0]):
        for j in range(i, graph.shape[1]):
            if graph[i, j] == 1:
                g.add_edge(i, j)
    g1 = nx.Graph()
    for i in range(graph1.shape[0]):
        g1.add_node(i)
    for i in range(graph1.shape[0]):
        for j in range(i, graph1.shape[1]):
            if graph1[i, j] == 1:
                g1.add_edge(i, j)
    gm = isomorphism.GraphMatcher(g, g1)
    if gm.is_isomorphic():
        c_list = np.zeros((g.number_of_nodes(), 2), dtype="int")
        for i in range(g.number_of_nodes()):
            c_list[i, 0] = coordinates1[gm.mapping[i], 0]
            c_list[i, 1] = coordinates1[gm.mapping[i], 1]
        return c_list
    else:
        raise Exception("Not isomorphic graphs")


def scale(x, arr):
    s_arr = np.ones((x * arr.shape[0], x * arr.shape[1], 3), dtype=np.uint8) * 255
    for row in range(s_arr.shape[0]):
        for column in range(s_arr.shape[1]):
            s_arr[row, column] = arr[row // x, column // x]
    return s_arr


def animation(frm, fps, position, rows, columns, dict_list, graph, vertex):
    frames = []
    timer = pygame.time.Clock()
    screen = pygame.display.set_mode((500, 500), 0, 32)
    for i in range(1, frm + 1):
        arr = np.ones((rows, columns, 3), dtype=np.uint8) * 255
        for j in range(vertex):
            arr[dict_list[j][i][0], dict_list[j][i][1]] *= 0
        for row in range(graph.shape[0]):
            for column in range(row, graph.shape[1]):
                if graph[row, column] == 1:
                    i1, j1 = dict_list[row][i]
                    i2, j2 = dict_list[column][i]
                    difi = i2 - i1
                    difj = j2 - j1
                    if (abs(difi) >= abs(difj)) and (abs(difi) > 0):
                        if i1 > i2:
                            d = (abs(difj) + 1) / (abs(difi) + 1)
                            diag = d / 2
                            c = j1
                            for r in range(i1 - 1, i2, -1):
                                diag += d
                                if diag >= abs(j1 - c) + 1:
                                    if j1 < j2:
                                        c += 1
                                    else:
                                        c -= 1
                                arr[r, c] *= 0
                        else:
                            d = (abs(difj) + 1) / (abs(difi) + 1)
                            diag = d / 2
                            c = j1
                            for r in range(i1 + 1, i2):
                                diag += d
                                if diag >= abs(j1 - c) + 1:
                                    if j1 < j2:
                                        c += 1
                                    else:
                                        c -= 1
                                arr[r, c] *= 0
                    if (abs(difi) < abs(difj)) and (abs(difj) > 0):
                        if j1 > j2:
                            d = (abs(difi) + 1) / (abs(difj) + 1)
                            diag = d / 2
                            r = i1
                            for c in range(j1 - 1, j2, -1):
                                diag += d
                                if diag >= abs(i1 - r) + 1:
                                    if i1 < i2:
                                        r += 1
                                    else:
                                        r -= 1
                                arr[r, c] *= 0
                        else:
                            d = (abs(difi) + 1) / (abs(difj) + 1)
                            diag = d / 2
                            r = i1
                            for c in range(j1 + 1, j2):
                                diag += d
                                if diag >= abs(i1 - r) + 1:
                                    if i1 < i2:
                                        r += 1
                                    else:
                                        r -= 1
                                arr[r, c] *= 0
        s_arr = scale(8, arr)
        image = Image.fromarray(s_arr, "RGB")
        image.save("data.png")
        frames.append(pygame.image.load("data.png"))

    counter = 0

    while True:
        for evt in pygame.event.get():
            if evt.type == QUIT or (evt.type == KEYDOWN and evt.key == K_ESCAPE):
                sys.exit()
        screen.fill((255, 255, 255))
        screen.blit(frames[counter], position)
        counter = (counter + 1) % frm
        pygame.display.update()
        timer.tick(fps)


def main():
    dict_list = []
    frames = 65
    data = load(1)
    coord, graph = tograph(data)
    vertex = coord.shape[0]
    rows = 50
    columns = 50

    for row in coord:
        dict_list.append({1: (row[0], row[1])})

    for i in range(9, frames + 1, 8):
        data1 = load((i // 8) + 1)
        coord1, graph1 = tograph(data1)
        c_list = isomorph(graph, graph1, coord1)
        for j in range(c_list.shape[0]):
            dict_list[j][i] = (c_list[j, 0], c_list[j, 1])

    for i in range(5, frames + 1, 8):
        for j in range(vertex):
            row = (dict_list[j][i - 4][0] + dict_list[j][i + 4][0]) // 2
            column = (dict_list[j][i - 4][1] + dict_list[j][i + 4][1]) // 2
            dict_list[j][i] = (row, column)

    for i in range(3, frames + 1, 4):
        for j in range(vertex):
            row = (dict_list[j][i - 2][0] + dict_list[j][i + 2][0]) // 2
            column = (dict_list[j][i - 2][1] + dict_list[j][i + 2][1]) // 2
            dict_list[j][i] = (row, column)

    for i in range(2, frames + 1, 2):
        for j in range(vertex):
            row = (dict_list[j][i - 1][0] + dict_list[j][i + 1][0]) // 2
            column = (dict_list[j][i - 1][1] + dict_list[j][i + 1][1]) // 2
            dict_list[j][i] = (row, column)

    # вывод словаря
    # for i in range(len(dict_list)):
    #     print(i + 1, ":")
    #     for j in range(frames):
    #         print("frame ", j + 1, ": ", dict_list[i][j + 1])

    # вывод координат
    # data = load(4)
    # coord, graph = tograph(data)
    # for row in coord:
        # print(row[0], row[1])

    # вывод анимации
    animation(65, 40, (25, 25), rows, columns, dict_list, graph, vertex)


if __name__ == "__main__":
    main()
