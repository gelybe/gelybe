"""
В этом файле будет ваше Flask-приложение
"""
from flask import Flask, request, jsonify
from m_celery import task_blur, subscribers_object, celery
from celery import group

app = Flask(__name__)

@app.route("/blur", methods=["POST"])
def blur():
    images = request.form.getlist("images")

    if images and isinstance(images, list):
        task_group = group(
            task_blur.s(image)
            for image in images)
        result = task_group.apply_async()
        result.save()
        return jsonify({'group_id': result.id}), 202

    else:
        return jsonify({'error': 'Missing or invalid images parameter'}), 400


@app.route('/status/<group_id>', methods=['GET'])
def get_group_status(group_id: str):
   result = celery.GroupResult.restore(group_id)
   if result:
       status = (f"{result.completed_count()} / {len(result)} - {result.completed_count() / len(result) * 100} %")
       return jsonify({'status':  status}), 200
   else:
       return jsonify({'error': 'Invalid group_id'}), 404


@app.route("/subscribe", methods=["POST"])
def subscribe():
    mail = request.form.get("email")
    res = subscribers_object.subscribe(mail)
    return res


@app.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    mail = request.form.get("email")
    res = subscribers_object.unsubscribe(mail)
    return res

if __name__ == "__main__":
    app.run(debug=True)


