from flask import Flask, render_template, request, redirect, send_file
from extractors.rmt import extract_rmt_jobs
from extractors.wwr import extract_wework_jobs
from file import save_to_file

app= Flask(__name__)

db={}
@app.route("/")
def home():
  return render_template("home.html")

@app.route("/jobscrapper")
def jobscrapper():
  return render_template("jobscrapper.html")

@app.route("/animal")
def animal():
  return render_template("animal.html")


@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/jobscrapper")
  if keyword in db:
    jobs = db[keyword]
  else:
    rmt = extract_rmt_jobs(keyword)
    wwr = extract_wework_jobs(keyword)
    jobs = rmt + wwr
    db[keyword] = jobs
  return render_template("search.html", keyword=keyword,jobs=jobs)

@app.route("/export")
def export():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/jobscrapper")
  if keyword not in db:
    return redirect(f"/search?keyword={keyword}")
  save_to_file(keyword, db[keyword])
  return send_file(f"{keyword}.csv", as_attachment=True)

