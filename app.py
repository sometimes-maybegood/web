from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

TRANSPORT_GRAPH = {
    'Москва': [
        {'to': 'Санкт-Петербург', 'type': 'train', 'time': 240, 'cost': 1500},
        {'to': 'Сочи', 'type': 'plane', 'time': 150, 'cost': 4000}
    ],
    'Санкт-Петербург': [
        {'to': 'Сочи', 'type': 'train', 'time': 600, 'cost': 2500}
    ]
}

HOTELS = {
    'Сочи': [
        {'name': 'Отель "Морской"', 'price': 3500, 'distance': 0.5},
        {'name': 'Хостел "Горный"', 'price': 1200, 'distance': 1.2}
    ]
}


def dijkstra(start, end, criteria='cost'):
    graph = {}
    for city, routes in TRANSPORT_GRAPH.items():
        graph[city] = []
        for route in routes:
            weight = route['cost'] if criteria == 'cost' else route['time']
            graph[city].append((route['to'], weight, route['type']))

    queue = [(0, start, [])]
    visited = set()

    while queue:
        weight, node, path = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            path = path + [(node, weight)]

            if node == end:
                return {'total': weight, 'path': path}

            if node in graph:
                for neighbor, edge_weight, transport_type in graph[node]:
                    if neighbor not in visited:
                        total = weight + edge_weight
                        heapq.heappush(queue, (total, neighbor, path))

    return None


@app.route('/')
def index():
    return render_template('map.html')


@app.route('/route', methods=['POST'])
def calculate_route():
    data = request.json
    start = data['start']
    end = data['end']
    criteria = data.get('criteria', 'cost')

    result = dijkstra(start, end, criteria)
    hotels = HOTELS.get(end, [])

    return jsonify({
        'route': result,
        'hotels': hotels
    })


if __name__ == '__main__':
    app.run(debug=True)