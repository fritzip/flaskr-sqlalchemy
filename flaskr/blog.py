from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from werkzeug.exceptions import abort

from flask_login import login_required

from flaskr.extensions import db
from flaskr.models.post import Post
from flaskr.models.tag import Tag

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    posts = db.session.query(Post).all()
    return render_template("blog/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form.get("body", "")
        tags = request.form.get("tags", "")
        tag_list = []
        for tag in tags.split(","):
            tag = tag.strip()
            if tag:
                tag_list.append(tag)

        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, author_id=current_user.id)
            for tag_name in tag_list:
                tag = Tag.query.filter(Tag.name == tag_name).first()
                if tag is not None:
                    post.tags.append(tag)
                else:
                    post.tags.append(Tag(name=tag_name))
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = db.session.query(Post).filter(Post.id == id).first()
    if post is None:
        abort(404)
    if request.method == "POST":
        if post.author_id != current_user.id:
            abort(403)
        title = request.form["title"]
        body = request.form.get("body", None)
        tags = request.form.get("tags", None)
        if tags is not None:
            tag_list = []
            for tag in tags.split(","):
                tag = tag.strip()
                if tag:
                    tag_list.append(tag)

        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post.title = title
            if body is not None:
                post.body = body
            if tags is not None:
                post.tags = []
                for tag_name in tag_list:
                    tag = Tag.query.filter(Tag.name == tag_name).first()
                    if tag is not None:
                        post.tags.append(tag)
                    else:
                        post.tags.append(Tag(name=tag_name))
            db.session.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    post = db.session.query(Post).filter(Post.id == id).first()
    if post is None:
        abort(404)
    if post.author_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("blog.index"))
