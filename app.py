from flask import Flask,render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient()
db = client.Playlister
playlists = db.playlists



app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('home.html', msg='Flask is Cool!!')

# playlists = [
#     { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
#     { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' }
# ]


@app.route('/')
def playlists_index():
    """Show all playlists."""
    return render_template('playlists_index.html', playlists=playlists.find())

@app.route('/playlists/new')
def playlists_new():
    return render_template('playlists_new.html', playlist={}, title = 'New Playlist')

@app.route('/playlists', methods=['POST'])
def playlists_submit():
    #print(request.form.to_dict)
    playlist = {
        'title' : request.form.get('title'),
        'description' : request.form.get('description'),
        'videos' : request.form.get('videos').split()
    }
    #playlists.insert_one(playlist)
    playlist_id = playlists.insert_one(playlist).inserted_id
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    playlist = playlists.find_one({'_id' : ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist)

@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')

@app.route('/playlists/<playlist_id', methods=['POST'])
def playlists_update(playlist_id):
    updated_playlist = {
        'title' : request.form.get('title'),
        'description' : request.form.get('description'),
        'videos' : request.form.get('videos').split()
    }
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))
@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    playlist.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')