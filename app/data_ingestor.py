import json
import csv


class DataIngestor:
    def __init__(self, csv_path: str):

        self.data = []
        # Read the CSV file and store its contents in csv_data
        with open(csv_path,  encoding="utf-8", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data.append(row)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    # Functie ajutatoare care returneaza un dictionar cu media fiecarui stat
    def dict_of_means(self, data):
        states_means = {}

        for row in self.data:
            location_desc = row['LocationDesc']
            data_value = float(row['Data_Value']) 
            question = row['Question']

            if question == data['question']:
                if location_desc not in states_means:
                    states_means[location_desc] = [data_value, 1] #[valoare, counter]
                else:
                    # Se adauga valoarea la suma valorilor pt stat și se incrementeaza counter-ul
                    states_means[location_desc][0] += data_value
                    states_means[location_desc][1] += 1

        # Calculul mediei pentru fiecare stat
        for state, values in states_means.items():
            states_means[state] = values[0] / values[1]

        return states_means

    # Functie ajutatoare pentru calcularea mediei globale/ a unui stat anume
    def mean_function(self, data):
        mean = 0
        counter = 0
        for row in self.data:
            location_desc = row['LocationDesc']
            data_value = float(row['Data_Value'])
            question = row['Question']

            if question == data['question']:
                if 'state' in data and data['state'] == location_desc or 'state' not in data:
                    mean += data_value
                    counter += 1

        mean = mean / counter
        return mean

    def states_mean(self, job_id, data):
        states_means = self.dict_of_means(data)
       
        # Sortare crescatoare
        states_means = dict(sorted(states_means.items(), key=lambda x:x[1]))

        result = {"status": "done", "data": states_means}
        with open(f"./results/job_id_{int(job_id)}.json", mode="w", encoding="utf-8") as file:
            json.dump(result, file)

    def state_mean(self, job_id, data):
        mean = self.mean_function(data)
        result = {"status": "done", "data": {data['state'] : mean}}
        with open(f"./results/job_id_{int(job_id)}.json", mode="w", encoding="utf-8") as file:
            json.dump(result, file)

        return mean

    def best5(self, job_id, data):
        states_means = self.dict_of_means(data)

        # Daca e in best_is_max, se sorteaza descrescator si se iau primele 5 valori
        if data['question'] in self.questions_best_is_max:
            states_means = dict(sorted(states_means.items(), key=lambda x:x[1], reverse=True)[:5])
        # Daca nu, se sorteaza crescator si se iau primele 5 valori
        else:
            states_means = dict(sorted(states_means.items(), key=lambda x:x[1])[:5])

        result = {"status": "done", "data": states_means}
        with open(f"./results/job_id_{int(job_id)}.json", mode="w", encoding="utf-8") as file:
            json.dump(result, file)

    def worst5(self, job_id, data):
        states_means = self.dict_of_means(data)
       
        if data['question'] not in self.questions_best_is_max:
            states_means = dict(sorted(states_means.items(), key=lambda x:x[1], reverse=True)[:5])
        else:
            states_means = dict(sorted(states_means.items(), key=lambda x:x[1])[:5])

        result = {"status": "done", "data": states_means}
        with open(f"./results/job_id_{int(job_id)}.json", "w") as file:
            json.dump(result, file)

    def global_mean(self, job_id, data):
        mean = self.mean_function(data)
        result = {"status": "done", "data": {"global_mean" : mean}}
        with open(f"./results/job_id_{int(job_id)}.json", mode="w", encoding="utf-8") as file:
            json.dump(result, file)

   
    def diff_from_mean(self, job_id, data):
        global_mean = self.mean_function(data)
        states_means = self.dict_of_means(data)

        for state in states_means:
            states_means[state] = global_mean - states_means[state]

        result = {"status": "done", "data": states_means}
        with open(f"./results/job_id_{int(job_id)}.json", mode="w", encoding="utf-8") as file:
            json.dump(result, file)

    def state_diff_from_mean(self, job_id, data):
        state = data['state']
        state_mean = self.mean_function(data)
        del data['state']
        diff = self.mean_function(data) - state_mean
        result = {"status": "done", "data": {state : diff}}
        with open(f"./results/job_id_{int(job_id)}.json", mode="w", encoding="utf-8") as file:
            json.dump(result, file)


    def mean_by_category(self, job_id, data):
        means_by_category = {}

        for row in self.data:
            location_desc = row['LocationDesc']
            data_value = float(row['Data_Value'])
            question = row['Question']
            stratification_1 = row['Stratification1']
            stratification_category_1 = row['StratificationCategory1']

            category_tuple = (location_desc, stratification_category_1, stratification_1)

            if question == data['question'] and stratification_1 != '':
                if category_tuple not in means_by_category:
                    means_by_category[category_tuple] = [data_value, 1] #[valoare, counter]
                else:
                    # Se adauga valoarea la suma valorilor pt tuplu și se incrementeaza counter-ul
                    means_by_category[category_tuple][0] += data_value
                    means_by_category[category_tuple][1] += 1

        # Se calculeaza media pentu fiecare tuplu
        for category_tuple, values in means_by_category.items():
            means_by_category[category_tuple] = values[0] / values[1]

        # Setransforma tuplul in string
        means_by_category = {str(tuple_to_str) : value for tuple_to_str,
                              value in means_by_category.items()}

        result = {"status": "done", "data": means_by_category}

        with open(f"./results/job_id_{int(job_id)}.json", mode="w", encoding="utf-8") as file:
            json.dump(result, file)

    def state_mean_by_category(self, job_id, data):
        state_means_by_category = {}

        for row in self.data:
            location_desc = row['LocationDesc']
            data_value = float(row['Data_Value']) 
            question = row['Question']
            stratification_1 = row['Stratification1']
            stratification_category_1 = row['StratificationCategory1']

            category_tuple = (stratification_category_1, stratification_1)
            if question == data['question'] and location_desc == data['state']:
                if category_tuple not in state_means_by_category:
                    state_means_by_category[category_tuple] = [data_value, 1]
                else:
                    state_means_by_category[category_tuple][0] += data_value
                    state_means_by_category[category_tuple][1] += 1
                    
        for category_tuple, values in state_means_by_category.items():
            state_means_by_category[category_tuple] = values[0] / values[1]

        state_means_by_category = {data['state'] : {str(tuple_to_str) : value for tuple_to_str, 
                                                    value in state_means_by_category.items()}}

        result = {"status": "done", "data": state_means_by_category}

        with open(f"./results/job_id_{int(job_id)}.json", mode="w", encoding="utf-8") as file:
            json.dump(result, file)
