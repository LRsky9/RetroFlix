from flask import render_template, request, redirect, url_for, session, flash, jsonify

from application import app
from application.models import *
from flask_login import current_user, login_required

#terms render
@app.route('/terms_of_use')
def terms_of_use():
    return render_template('terms_of_use.html', title='Terms of Use')

#about us render
@app.route('/about_us')
def about_us():
    return render_template('about_us.html', title='About Us')

#careers render
@app.route('/careers')
def careers():
    return render_template('careers.html', title='Careers')

#contact us render
@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html', title='Contact Us')

#corporate info render
@app.route('/corp_info')
def corp_info():
    return render_template('corp_info.html', title='Corporate Information')

#faqs render
@app.route('/faq')
def faq():
    return render_template('faq.html', title='Frequently Asked Questions')

#help render
@app.route('/help')
def help():
    return render_template('help.html', title='Help')

#legal notices render
@app.route('/legal_notice')
def legal_notice():
    return render_template('legal_notice.html', title='Legal Notice')

#privacy notice render
@app.route('/privacy_notice')
def privacy_notice():
    return render_template('privacy_notice.html', title='Privacy Notice')

#film render
@app.route('/film')
@login_required
def film():
    return render_template('film.html', title='Films')

#series render
@app.route('/series')
@login_required
def series():
    return render_template('series.html', title='Series')

#home render
@app.route('/home')
@login_required
def home():
    user = User.query.get(current_user.id)
    return render_template('home.html', title='Home', user=user)

#account render
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if request.method == 'POST':
            user.email_address = request.form['email_address']
            user.password = request.form['password']
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.dob = request.form['dob']
            user.mailing = request.form['mailing']
            user.creation_date = request.form['creation_date']
            user.last_login = request.form['last_login']
            user.pin = request.form['pin']
            
            db.session.commit()
        return render_template('account.html', user=user)
    else:
        return redirect(url_for('login'))

#index render
@app.route('/index')
def index():
    return render_template("index.html")


#search bar render'
@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query')
    films = Film.query.filter(Film.title.ilike(f'%{query}%')).all()
    actors = Actor.query.filter(Actor.name.ilike(f'%{query}%')).all()  # if you search for full name, you get two results where it matches the first and last name
    genres = Genre.query.filter(Genre.genre.ilike(f'%{query}%')).all()
    tv_series = TVSeries.query.filter(TVSeries.title.ilike(f'%{query}%')).all()
    
    return render_template('search_results.html', films=films, actors=actors, genres=genres, tv_series=tv_series)


@app.route('/film/film_player/<string:name>')
@login_required
def film_player(name):
    film = Film.query.filter_by(title=name).first_or_404()
    video_file = "/videos/" + name.lower().replace(" ", "_") + ".mp4"
    pinCheck = False
    if film.age_rating == "R":
        pinCheck = True
    return render_template('film_player.html', film=film, pinCheck=pinCheck, video=video_file)

@app.route('/series/series_player/<string:name>/<string:episode>')
@login_required
def series_player(name, episode):
    series = TVSeries.query.filter_by(title=name).first_or_404()
        
    if series:
        season_number, episode_number = episode[1:].split('E')
        season_number = int(season_number)
        episode_number = int(episode_number)

        if name == "Friends" and season_number == 1:
            video_file = "/videos/" + name.lower().replace(" ", "_") + "_" + episode + ".mp4"
        else:
            video_file = "/videos/" + name.lower().replace(" ", "_") + ".mp4"
        season = TVSeriesSeason.query.filter_by(tv_series_id=series.id, season_number=season_number).first_or_404()

        if season:
            episode = TVSeriesEpisode.query.filter_by(tv_series_season_id=season.id, episode_number=episode_number).first_or_404()

    return render_template('series_player.html', series=series, season=season, episode=episode, video=video_file)

@app.route('/check_pin', methods=['POST'])
def check_pin():
    film_id = request.args.get('film')
    video = request.args.get('video')

    user = User.query.get(current_user.id)
    user_pin = user.pin
    input_pin = request.form['inputPin']

    film = Film.query.filter_by(id=film_id).first_or_404()
    
    if input_pin == user_pin:
        pinCheck = False
        return render_template('film_player.html', film=film, pinCheck=pinCheck, video=video) 
    else:
        pinCheck = True
        flash('Wrong Pin')
        return render_template('film_player.html', film=film, pinCheck=pinCheck, video=video) 



