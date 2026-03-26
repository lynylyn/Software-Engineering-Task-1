import json
currentsession = []

def loginput(prompt):
    response = input(prompt)
    currentsession.append({"prompt": prompt, "response": response})
    return response

def savesession(user_name):
    try:
        file = open("sessions.json")
        sessions = json.load(file)
        file.close()
    except FileNotFoundError:
        sessions = {}
    if user_name not in sessions:
        sessions[user_name] = []
    sessions[user_name].append(currentsession)
    file = open("sessions.json", "w")
    json.dump(sessions, file)

def loadsessions(user_name):
    file = open("sessions.json")
    sessions = json.load(file)
    if user_name in sessions:
        return sessions[user_name]
    else:
        return []