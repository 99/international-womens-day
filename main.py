"""International Women's Day"""
import os

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask import send_from_directory
from data import speakers_data, talks, track_names, session_times, missing_data_talks, order_of_sessions, schedule_color

app = Flask(__name__)

# Required t,l.o use Flask sessions and the debug toolbar
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "abcdef")


# Make Jinja2 to raise an error instead of failing sliently
app.jinja_env.undefined = "StrictUndefined"


@app.route("/logo.png")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static", "imgs", "assests"),
                               "iwd-square-small.jpg", mimetype="image/png")


@app.route("/schedule.png")
def schedule_img():
    return send_from_directory(os.path.join(app.root_path, "static", "imgs", "assests"),
                               "speakers.jpg", mimetype="image/png")

@app.route("/")
def index():
    """Homepage"""

    return render_template("homepage.html")


@app.route("/speakers")
def speakers():
    """Speaker Page"""
    print "*"*80
    # import pdb; pdb.set_trace()
    print speakers_data

    return render_template("speakers.html", 
                            speaker_data=speakers_data)


@app.route("/schedule")
def schedule():
    """Schedule Page"""

    if missing_data_talks:
        print "*"*80
        print "The following talks are don't have a track & time:"
        print missing_data_talks
        print "*"*80

    range_session_times = range(len(session_times))
    


    return render_template("schedule.html",
                            talks=talks,
                            track_names=track_names,
                            session_times=session_times,
                            order_of_sessions=order_of_sessions,
                            range_session_times=range_session_times,
                            schedule_color=schedule_color,
                            )



############################################################################
# Error Pages
# @app.errorhandler(404)
# def page_not_found(error):
#     """404 Page Not Found handling"""

#     return render_template('/errors/404.html'), 404


# @app.errorhandler(500)
# def internal_error(error):
#     # db.session.rollback()
#     """500 Error handling """

#     return render_template('/errors/500.html'), 500



if __name__ == "__main__":

    app.debug = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)