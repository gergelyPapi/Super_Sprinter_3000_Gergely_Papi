from flask import Flask, render_template, redirect, request, url_for
import csv

app = Flask(__name__)

def read_database(csv_database):
    csv_reader = csv.reader(open(csv_database))
    csv_reader_lists = []
    for list in csv_reader:
        csv_reader_lists.append(list)
    return csv_reader_lists

@app.route('/')
def route_list():
    database= read_database("user_stories.csv")
    return render_template("list.html", database=database)

@app.route('/story')
def route_edit():
    return render_template("form.html")

@app.route('/story/<story_id>', methods=["POST", "GET"])
def save_story(story_id):
    database= read_database("user_stories.csv")
    current_entry_information = []
    for list in database:
        if list[0] == story_id:
            for list_item in list:
                current_entry_information.append(list_item)
    return render_template("form.html", current_entry_information=current_entry_information)

@app.route("/save_user_story", methods=["POST"])
def save_user_story():
    csv_database = read_database("user_stories.csv")
    row_count = sum(1 for row in csv_database)
    user_story_manager = []
    user_story_manager.append(row_count+1)
    user_story_manager.append(request.form["Story Title"])
    user_story_manager.append(request.form["User Story"])
    user_story_manager.append(request.form["Acceptance criteria"])
    user_story_manager.append(request.form["Business value"])
    user_story_manager.append(request.form["Estimation"])
    user_story_manager.append(request.form["Status"])
    csv_writer = csv.writer(open("user_stories.csv", "a"))
    csv_writer.writerow(user_story_manager)
    return redirect('/')

@app.route("/update_user_story", methods=["POST"])
def update_user_story():
    existing_list = csv.reader(open("user_stories.csv"))
    replaced_item = [item for item in existing_list]
    replaced_item[int(request.form["ID"])-1][1] = request.form["Story Title"]
    replaced_item[int(request.form["ID"])-1][2] = request.form["User Story"]
    replaced_item[int(request.form["ID"])-1][3] = request.form["Acceptance criteria"]
    replaced_item[int(request.form["ID"])-1][4] = request.form["Business value"]
    replaced_item[int(request.form["ID"])-1][5] = request.form["Estimation"]
    replaced_item[int(request.form["ID"])-1][6] = request.form["Status"]
    writer = csv.writer(open("user_stories.csv", 'w'))
    writer.writerows(replaced_item)
    return redirect('/')


@app.route("/remove_user_story", methods=["POST"])
def remove_user_story():
    csv_database = read_database("user_stories.csv")
    for row in csv_database:
        if row[0] == request.form["ID"]:
            writer = csv.writer(open("user_stories.csv", 'w'))
            print(row)
            writer.writerows(row)
    return redirect('/')

    
if __name__ == "__main__":
    app.run(
        debug=True, # Allow verbose error reports
        port=2000 # Set custom port
    )