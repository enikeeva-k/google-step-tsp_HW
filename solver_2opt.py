#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def create_distances_matrix(cities):
    num_cities = len(cities)

    dist = [[0] * num_cities for i in range(num_cities)]
    for i in range(num_cities):
        for j in range(i, num_cities):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    return dist


def solve_greedy(dist):
    num_cities = len(dist)
    current_city = 0
    unvisited_cities = set(range(1, num_cities))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour


def reverse(tour, left, right):
    while left < right:
        tour[left], tour[right] = tour[right], tour[left]
        left += 1
        right -= 1


def calculate_cost(dist, tour):
    cost = 0
    for i in range(len(tour) - 1):
        cost += dist[tour[i]][tour[i + 1]]
    cost += dist[tour[len(tour) - 1]][tour[0]]
    return cost


def adjust_cost_after_reverse(cost_before_reverse, distances, tour, left, right):
    cost = cost_before_reverse
    # Replace cost at left.
    id_before_left = max(left - 1, 0)
    cost -= distances[tour[left]][tour[id_before_left]]
    cost += distances[tour[right]][tour[id_before_left]]

    # Replace cost at right.
    id_after_right = (right + 1) % len(tour)
    cost -= distances[tour[right]][tour[id_after_right]]
    cost += distances[tour[left]][tour[id_after_right]]

    return cost


def solve_2opt(dist):
    num_cities = len(dist)
    tour = solve_greedy(dist)
    cost = calculate_cost(dist, tour)

    for i in range(num_cities):
        for j in range(i+1, num_cities):
            adjusted_cost = adjust_cost_after_reverse(cost, dist, tour, i, j)

            if adjusted_cost < cost:
                reverse(tour, i, j)

    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1

    cities = read_input(sys.argv[1])
    dist = create_distances_matrix(cities)

    tour = solve_2opt(dist)
    print_tour(tour)
