from application import app, db
from application.models import FriendsCharacter
from application.forms import AddCharacterForm
from flask import request, jsonify, render_template, redirect


def format_character(character):
    return {
        "id": character.id,
        "name": character.name,
        "age": character.age,
        "catch_phrase": character.catch_phrase,
    }


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# @app.route("/characters", methods=["GET", "POST"])
# def create_character():
#     # Retrieved data from client
#     data = request.json
#     # Created a new character using data
#     character = FriendsCharacter(data["name"], data["age"], data["catch_phrase"])
#     # Send character to DB
#     db.session.add(character)
#     db.session.commit()
#     # Return JSON response back to the user
#     return jsonify(
#         id=character.id, name=character.name, age=character.age, catch_phrase=character.catch_phrase
#     )

# @app.route("/characters", methods=["GET"])
# def get_characters():
#     # request.method to distingiuish methods
#     characters = FriendsCharacter.query.all()
#     character_list = []
#     for character in characters:
#         character_list.append(format_character(character))
#     return character_list


@app.route("/characters", methods=["GET", "POST"])
def characters():
    # request.method to distingiuish methods
    method = request.method
    print(method)
    form = AddCharacterForm()

    if method == "POST":
        if form.validate_on_submit():
            character = FriendsCharacter(form.name.data, form.age.data, form.catch_phrase.data)
            db.session.add(character)
            db.session.commit()
            return redirect('/')
        else:
            pass #Error handling

        # # Retrieved data from client
        # data = request.json
        # # Created a new character using data
        # character = FriendsCharacter(data["name"], data["age"], data["catch_phrase"])
        # # Send character to DB
        # db.session.add(character)
        # db.session.commit()
        # # Return JSON response back to the user
        # return jsonify(
        #     id=character.id,
        #     name=character.name,
        #     age=character.age,
        #     catch_phrase=character.catch_phrase
        # )
    elif method == "GET":
        characters = FriendsCharacter.query.all()
        character_list = []
        for character in characters:
            character_list.append(format_character(character))
        return render_template('characters.html', characters=character_list, title="Friends", form=form)


# GET /:id
@app.route("/characters/<id>")  # by default GET method
def get_character(id):
    # filter_by
    character = FriendsCharacter.query.filter_by(id=id).first()
    return render_template('character.html', character=character, title=character.name)  # or use jsonify


# DELETE /:id
@app.route("/characters/<id>", methods=["DELETE"])
def delete_character(id):
    character = FriendsCharacter.query.filter_by(id=id).first()
    db.session.delete(character)
    db.session.commit()
    return render_template('deleted.html')


# PATCH /:id
@app.route("/characters/<id>", methods=["PATCH"])
def update_character(id):
    character = FriendsCharacter.query.filter_by(id=id)
    data = request.json
    character.update(
        dict(name=data["name"], age=data["age"], catch_phrase=data["catch_phrase"])
    )
    db.session.commit()
    new_character = character.first()
    return render_template('character.html', character=new_character, title=character.name)
