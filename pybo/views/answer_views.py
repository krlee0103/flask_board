from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import AnswerForm
from pybo.models import Question, Answer
from pybo.views.auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()
        return redirect('{}#answer_{}'.format(
            url_for('question.detail', question_id=question_id), answer.id))
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('You do not have access to edit')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', form=form)


@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('You do not have access to delete')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))


@bp.route('/vote/<int:answer_id>/')
@login_required
def vote(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user == answer.user:
        flash("You can't 'like' what you wrote")
    else:
        answer.voter.append(g.user)
        db.session.commit()
    return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=answer.question.id), answer.id))

@bp.route('/unvote/<int:answer_id>/')
@login_required
def unvote(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    answer.voter.remove(g.user)
    db.session.commit()
    return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=answer.question.id), answer.id))