from app import webserver
from flask import request, jsonify
import json

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405
  

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")
 
    # Verifică dacă job_id este valid
    if webserver.job_counter < int(job_id):
        return jsonify({'status': 'error', 'reason': 'Invalid job_id'})
    # Daca statusul e "running", returneaza asta
    elif webserver.tasks_runner.jobs[int(job_id)] == "running":
        return jsonify({'status': 'running'}), 200
    # Daca job-ul e terminat, returneaza continutul fisierului cu nume corespunzator din results/
    else:
        with open(f"./results/job_id_{int(job_id)}.json", encoding="utf-8") as file:
            return jsonify(json.load(file))



@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # Se primesc datele request-ului
    data = request.json
    print(f"Got request {data}")
  
    job_id = webserver.job_counter
    # Se adauga o noua intrare in dictionarul de job-uri
    webserver.tasks_runner.jobs[job_id] = "running"
    webserver.tasks_runner.jobs_type[job_id] = "states_mean"

    # Se pune job-ul in queue
    webserver.tasks_runner.task_queue.put(job_id)

    # Se apeleaza metoda corespunzatoare din DataIngestor
    webserver.data_ingestor.states_mean(job_id, data)

    # Se incrementeaza counter-ul
    webserver.job_counter += 1
    return jsonify({'status': 'done', 'job_id': job_id}), 200

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    data = request.json
    print(f"Got request {data}")
   
    job_id = webserver.job_counter
    webserver.tasks_runner.jobs[job_id] = "running"
    webserver.tasks_runner.jobs_type[job_id] = "state_mean"
    webserver.tasks_runner.task_queue.put(job_id)
    webserver.data_ingestor.state_mean(job_id, data)

    webserver.job_counter += 1
    return jsonify({'status': 'done', 'job_id': job_id}), 200


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    data = request.json
    print(f"Got request {data}")
   
    job_id = webserver.job_counter
    webserver.tasks_runner.jobs[job_id] = "running"
    webserver.tasks_runner.jobs_type[job_id] = "best5"
    webserver.tasks_runner.task_queue.put(job_id)
    webserver.data_ingestor.best5(job_id, data)

    webserver.job_counter += 1
    return jsonify({'status': 'done', 'job_id': job_id}), 200


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    data = request.json
    print(f"Got request {data}")
  
    job_id = webserver.job_counter
    webserver.tasks_runner.jobs[job_id] = "running"
    webserver.tasks_runner.jobs_type[job_id] = "worst5"
    webserver.tasks_runner.task_queue.put(job_id)
    webserver.data_ingestor.worst5(job_id, data)

    webserver.job_counter += 1
    return jsonify({'status': 'done', 'job_id': job_id}), 200


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    data = request.json
    print(f"Got request {data}")
   
    job_id = webserver.job_counter
    webserver.tasks_runner.jobs[job_id] = "running"
    webserver.tasks_runner.jobs_type[job_id] = "global_mean"
    webserver.tasks_runner.task_queue.put(job_id)
    webserver.data_ingestor.global_mean(job_id, data)

    webserver.job_counter += 1
    return jsonify({'status': 'done', 'job_id': job_id}), 200

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    data = request.json
    print(f"Got request {data}")
   
    job_id = webserver.job_counter
    webserver.tasks_runner.jobs[job_id] = "running"
    webserver.tasks_runner.jobs_type[job_id] = "diff_from_mean"
    webserver.tasks_runner.task_queue.put(job_id)
    webserver.data_ingestor.diff_from_mean(job_id, data)

    webserver.job_counter += 1
    return jsonify({'status': 'done', 'job_id': job_id}), 200

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    data = request.json
    print(f"Got request {data}")
  
    job_id = webserver.job_counter
    webserver.tasks_runner.jobs[job_id] = "running"
    webserver.tasks_runner.jobs_type[job_id] = "state_diff_from_mean"
    webserver.tasks_runner.task_queue.put(job_id)
    webserver.data_ingestor.state_diff_from_mean(job_id, data)

    webserver.job_counter += 1
    return jsonify({'status': 'done', 'job_id': job_id}), 200

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    data = request.json
    print(f"Got request {data}")
   
    job_id = webserver.job_counter
    webserver.tasks_runner.jobs[job_id] = "running"
    webserver.tasks_runner.jobs_type[job_id] = "mean_by_category"
    webserver.tasks_runner.task_queue.put(job_id)
    webserver.data_ingestor.mean_by_category(job_id, data)

    webserver.job_counter += 1
    return jsonify({'status': 'done', 'job_id': job_id}), 200

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    data = request.json
    print(f"Got request {data}")
   
    job_id = webserver.job_counter
    webserver.tasks_runner.jobs[job_id] = "running"
    webserver.tasks_runner.jobs_type[job_id] = "state_mean_by_category"
    webserver.tasks_runner.task_queue.put(job_id)
    webserver.data_ingestor.state_mean_by_category(job_id, data)

    webserver.job_counter += 1
    return jsonify({'status': 'done', 'job_id': job_id}), 200

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown_response():
    webserver.tasks_runner.stop()

    return jsonify({'status': 'shotdown'}), 200

@webserver.route('/jobs', methods=['GET'])
def jobs_response():
    return jsonify({'status': 'done', 'data' : webserver.tasks_runner.jobs}), 200
   
@webserver.route('/num_jobs', methods=['GET'])
def num_jobs_response():
    if webserver.tasks_runner.shutdown:
        return jsonify({'status': 'done', 'data' : {'num_jobs' : 0}}), 200
    else:
        num_jobs = webserver.tasks_runner.task_queue.qsize()
        return jsonify({'status': 'done', 'data' : {'num_jobs' : num_jobs}}), 200

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
