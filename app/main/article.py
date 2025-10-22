from flask import Blueprint, render_template

bp = Blueprint('article', __name__, url_prefix='/article')

@bp.route('/', methods=['GET', 'POST'])
def index():
    title = 'bohan wenzhang1'
    return render_template('main/article.html', title=title)