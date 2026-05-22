from flask import Flask, render_template, request, redirect, Response
from flask_bcrypt import Bcrypt

from config import Config

from models import db
from models.user import User
from models.complaint import Complaint

import csv

app = Flask(__name__)

app.config.from_object(Config)

bcrypt = Bcrypt(app)

db.init_app(app)


# LOGIN
@app.route("/", methods=["GET", "POST"])
def home():

    error = None

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and bcrypt.check_password_hash(
            user.password,
            password
        ):

            return redirect("/dashboard")

        error = "Invalid Email or Password"

    return render_template(
        "auth/login.html",
        error=error
    )


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            return "Email already exists"

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        user = User(
            name=name,
            email=email,
            password=hashed_password,
            role="student"
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/")

    return render_template("auth/register.html")


# STUDENT DASHBOARD
@app.route("/dashboard")
def dashboard():

    total = Complaint.query.count()

    pending = Complaint.query.filter_by(
        status="Pending"
    ).count()

    progress = Complaint.query.filter_by(
        status="In Progress"
    ).count()

    resolved = Complaint.query.filter_by(
        status="Resolved"
    ).count()

    complaints = Complaint.query.order_by(
        Complaint.id.desc()
    ).all()

    return render_template(
        "student/dashboard.html",
        total=total,
        pending=pending,
        progress=progress,
        resolved=resolved,
        complaints=complaints
    )


# SUBMIT COMPLAINT
@app.route("/submit-complaint", methods=["GET", "POST"])
def submit_complaint():

    if request.method == "POST":

        complaint = Complaint(
            category=request.form["category"],
            title=request.form["title"],
            description=request.form["description"]
        )

        db.session.add(complaint)
        db.session.commit()

        return redirect("/dashboard")

    return render_template(
        "student/submit_complaint.html"
    )


# ADMIN DASHBOARD
@app.route("/admin")
def admin_dashboard():

    complaints = Complaint.query.order_by(
        Complaint.id.desc()
    ).all()

    total = Complaint.query.count()

    pending = Complaint.query.filter_by(
        status="Pending"
    ).count()

    progress = Complaint.query.filter_by(
        status="In Progress"
    ).count()

    resolved = Complaint.query.filter_by(
        status="Resolved"
    ).count()

    return render_template(
        "admin/dashboard.html",
        complaints=complaints,
        total=total,
        pending=pending,
        progress=progress,
        resolved=resolved
    )


# UPDATE COMPLAINT
@app.route("/update-complaint/<int:complaint_id>",
           methods=["GET", "POST"])
def update_complaint(complaint_id):

    print("UPDATE ROUTE HIT")

    return f"Complaint ID = {complaint_id}"
def update_complaint(complaint_id):

    print("UPDATE ROUTE HIT")

    print(request.form)

    complaint = Complaint.query.get_or_404(
        complaint_id
    )

    complaint.status = request.form.get(
        "status"
    )

    complaint.assigned_to = request.form.get(
        "assigned_to"
    )

    db.session.commit()

    print("UPDATED SUCCESSFULLY")

    return redirect("/admin")

    complaint = Complaint.query.get_or_404(
        complaint_id
    )

    complaint.status = request.form["status"]

    complaint.assigned_to = request.form[
        "assigned_to"
    ]

    db.session.commit()

    return redirect("/admin")


# STAFF DASHBOARD
@app.route("/staff")
def staff_dashboard():

    complaints = Complaint.query.order_by(
        Complaint.id.desc()
    ).all()

    return render_template(
        "staff/dashboard.html",
        complaints=complaints
    )


# STAFF RESOLVE
@app.route("/resolve/<int:complaint_id>",
           methods=["POST"])
def resolve_complaint(complaint_id):

    complaint = Complaint.query.get_or_404(
        complaint_id
    )

    complaint.status = "Resolved"

    complaint.remarks = request.form[
        "remarks"
    ]

    db.session.commit()

    return redirect("/staff")


# EXPORT CSV
@app.route("/export-csv")
def export_csv():

    complaints = Complaint.query.all()

    def generate():

        data = csv.writer(
            open("/tmp/temp.csv", "w")
        )

        yield "ID,Title,Category,Status,Assigned To\n"

        for c in complaints:

            yield (
                f"{c.id},"
                f"{c.title},"
                f"{c.category},"
                f"{c.status},"
                f"{c.assigned_to}\n"
            )

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment;filename=complaints.csv"
        }
    )


# LOGOUT
@app.route("/logout")
def logout():

    return redirect("/")
@app.route("/test")
def test():
    return "TEST ROUTE WORKING"

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)