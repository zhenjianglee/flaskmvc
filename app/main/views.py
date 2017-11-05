from flask import render_template,redirect,url_for,abort,flash
from flask_login import login_required,current_user
from . import main
from .forms import LGDetailForm,LGEqueryForm
from .. import db
from ..models import Role,User,LG


@main.route('/index')
def index():
    return render_template('index.html')




@main.route('/enquery', methods=['GET', 'POST'])
@login_required
def enquery():

    form = LGEqueryForm()
    if form.validate_on_submit():
        lg = LG.query.filter_by(id=form.lg_no).first()
        if lg is not None:
            form1=LGDetailForm()
            return render_template('main/detail_lg',form=form1)
        flash('lg_no not found.')
    return render_template('main/enquery_lg.html',form=form)


@main.route('/update_lg/<lg_no>')
@login_required
def update_lg(lg_no):
    lg=LG.query.filter_by(no=lg_no).first
    if lg is None:
        flash('the lg not existed')
        return redirect(url_for('.index'))
    form = LGDetailForm(lg=lg)
    if form.validate_on_submit():
        lg.lg_custom_no=form.lg_custom_no.data
        lg.lg_status = 1
        db.session.add(lg)
        flash('lg updated')
        return redirect(url_for('.approve_lg',lg_no=lg.no))
    form.lg_no.data=lg.lg_no
    form.lg_companyname=lg.lg_companyname
    form.lg_custom_no=lg.lg_custom_no
    form.lg_amt = lg.lg_amt
    return render_template('main/update_lg.html',form=form,lg=lg)

@main.route('/detail_lg/<lg_no>')
@login_required
def approve_lg(lg_no):
    lg = LG.query.filter_by(no=lg_no).first
    if lg is None:
        flash('the lg not existed')
        return redirect(url_for('.index'))
    form = LGDetailForm(lg=lg)
    if form.validate_on_submit():
        if lg.lg_status==1:
            lg.lg_status=2
        else:
            lg.lg_status=1

        db.session.add(lg)
        if lg.lg_status==1:
            flash('lg custom_no updated')
        else:
            flash('lg custom_no approved')
        return redirect(url_for('main/enquery_lg'))
    form.lg_no.data=lg.lg_no
    form.lg_companyname=lg.lg_companyname
    form.lg_custom_no=lg.lg_custom_no
    form.lg_amt = lg.lg_amt
    form.lg_status = lg.lg_status
    if lg.lg_status==0:
        form.submit.data='update'
    else:
        form.submit.data='approve'
    return render_template('main/update_lg.html',form=form,lg=lg)










