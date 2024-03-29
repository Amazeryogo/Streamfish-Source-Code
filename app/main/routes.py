from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.main.forms import EditProfileForm, EmptyForm, PostForm, SearchForm, \
    MessageForm, EditProfileFormHINDI,EmptyFormHINDI,PostFormHINDI,SearchFormHINDI,MessageFormHINDI, \
    Longboy
from app.models import LP, User, Post, Message, Notification
from app.translate import translate
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    if current_user.hindi != True:
        return render_template('index.html', title=_('Home'),
                            posts=posts.items, next_url=next_url,
                            prev_url=prev_url,dm=current_user.darkmode,index=True)
    else:
        return render_template('Hindi/index.html', title=_('घर'),
                            posts=posts.items, next_url=next_url,
                            prev_url=prev_url,dm=current_user.darkmode)

@bp.route('/post/longpost',methods=['GET', 'POST'])
@login_required
def yu():
    form = Longboy()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        k = LP(lptitle=title,lpbody=body,author=current_user)
        db.session.add(k)
        db.session.commit()
        flash(_('Your long post is now live!'))
        return redirect(url_for('main.explore'))
    return render_template('makelp.html',form=form)

@bp.route('/lp')
def explorelp():
    page = request.args.get('page', 1, type=int)
    posts = LP.query.order_by(LP.lptimestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explorelp', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explorelp', page=posts.prev_num) \
        if posts.has_prev else None  
    return render_template('explore_lp.html', title=_('Longposts'),
                            lps=posts.items, next_url=next_url,
                            prev_url=prev_url,dm=current_user.darkmode)


@bp.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    if current_user.hindi != True:
        form = PostForm()
    else:
        form = PostFormHINDI()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = 'en'
        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None    
    if current_user.hindi != True:
        return render_template('index.html', title=_('Explore') ,
                            posts=posts.items, next_url=next_url,
                            prev_url=prev_url,dm=current_user.darkmode,verified=current_user.verified,form=form,index=False)
    else:
        return render_template('Hindi/index.html',title=_('Explore'),
                            posts=posts.items, next_url=next_url,
                            prev_url=prev_url,dm=current_user.darkmode,verified=current_user.verified,form=form)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    verified = user.verified
    staff = user.Staff
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()
    if current_user.hindi != True:
        return render_template('user.html', user=user, posts=posts.items,
                            next_url=next_url, prev_url=prev_url, form=form,verified=verified,staff=staff,dm=current_user.darkmode)
    else:
        return render_template('Hindi/user.html',user=user, posts=posts.items,
                            next_url=next_url, prev_url=prev_url, form=form,verified=verified,staff=staff,dm=current_user.darkmode)

@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.hindi != True:
        form = EmptyForm()
        return render_template('user_popup.html', user=user, form=form)
    else:
        form = EmptyForm()
        return render_template('user_popup.html', user=user, form=form)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.hindi != True:
        form = EditProfileForm(current_user.username)
    else:
        form = EditProfileFormHINDI(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.darkmode = form.darkmode.data
        current_user.hindi = form.hindi.data
        current_user.email = form.email.data
        db.session.commit()
        if current_user.hindi != True:
            flash(_('Your changes have been saved.'))
        else:
            flash(_('आपका बदलाव सहेज लिया गया है।'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.darkmode.data = current_user.darkmode
        form.hindi.data = current_user.hindi
        form.email.data = current_user.email
    if current_user.hindi != True:
        return render_template('edit_profile.html', title=_('Edit Profile'),
                            form=form,dm=current_user.darkmode,verified=current_user.verified)
    else:
        return render_template('Hindi/edit_profile.html', title=_('Edit Profile'),
                            form=form,dm=current_user.darkmode,verified=current_user.verified)

@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot follow yourself!'))
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        if current_user.hindi != True:
            flash(_('You are now following %(username)s!', username=username))
        else:
            flash(_('अब आप अनुसरण कर रहे हैं %(username)s!', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You can\'t follow this guy!:)!'))
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        if current_user.hindi != True:
            flash(_('You Unfollowed: %(username)s.', username=username))
        else:
            flash(_('आपने इस व्यक्ति को अनफॉलो कर दिया: %(username)s.', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    if current_user.hindi != True:
        form = MessageForm()
    else:
        form = MessageFormHINDI()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    if current_user.hindi != True:
        return render_template('send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)
    else:
        return render_template('Hindi/send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)


@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    if current_user.hindi != True:
        return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url,dm=current_user.darkmode)
    else:
        return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url,dm=current_user.darkmode)


@bp.route('/export_posts')
@login_required
def export_posts():
    if current_user.get_task_in_progress('export_posts'):
        flash(_('An export task is currently in progress'))
    else:
        current_user.launch_task('export_posts', _('Exporting posts...'))
        db.session.commit()
    return redirect(url_for('main.user', username=current_user.username))


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])


@bp.route('/<username>/followers')
@login_required
def followers(username):
    return render_template('followers.html', user=username)


@bp.route('/user/<username>/photo')
def photo(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('photo.html', user=user)

@bp.route('/user/api/<username>')
def api(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_api_info.html', user=user)

@bp.route('/user/api')
def aboutx():
    return render_template('about_api.html')

@bp.route('/discord')
def discord():
    return redirect("https://discord.gg/44RzAtCaVh")

@bp.route('/beta-testing')
def nitro():
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

@bp.route('/404')
def try404():
    return render_template('errors/404.html')

@bp.route('/500')
def try500():
    return render_template('errors/500.html')
