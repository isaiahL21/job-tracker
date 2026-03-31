from flask import Flask, render_template, request, redirect, url_for
from database import get_db

app = Flask(__name__)

# ─── DASHBOARD ───────────────────────────────────────────
@app.route('/')
def dashboard():
    conn = get_db()

    cursor1 = conn.cursor(dictionary=True)
    cursor1.execute('SELECT COUNT(*) as count FROM applications')
    total_apps = cursor1.fetchone()['count']
    cursor1.close()

    cursor2 = conn.cursor(dictionary=True)
    cursor2.execute('SELECT status, COUNT(*) as count FROM applications GROUP BY status')
    status_counts = cursor2.fetchall()
    cursor2.close()

    cursor3 = conn.cursor(dictionary=True)
    cursor3.execute('SELECT COUNT(*) as count FROM companies')
    total_companies = cursor3.fetchone()['count']
    cursor3.close()

    conn.close()

    return render_template('dashboard.html',
        total_apps=total_apps,
        status_counts=status_counts,
        total_companies=total_companies
    )

# ─── COMPANIES ───────────────────────────────────────────
@app.route('/companies')
def companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM companies ORDER BY company_name')
    all_companies = cursor.fetchall()
    conn.close()
    return render_template('companies.html', companies=all_companies)

@app.route('/companies/add', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO companies (company_name, industry, website, city, state, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            request.form['company_name'],
            request.form['industry'],
            request.form['website'],
            request.form['city'],
            request.form['state'],
            request.form['notes']
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('companies'))
    return render_template('add_company.html')

@app.route('/companies/edit/<int:id>', methods=['GET', 'POST'])
def edit_company(id):
    conn = get_db()
    if request.method == 'POST':
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE companies
            SET company_name=%s, industry=%s, website=%s, city=%s, state=%s, notes=%s
            WHERE company_id=%s
        ''', (
            request.form['company_name'],
            request.form['industry'],
            request.form['website'],
            request.form['city'],
            request.form['state'],
            request.form['notes'],
            id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('companies'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM companies WHERE company_id = %s', (id,))
    company = cursor.fetchone()
    conn.close()
    return render_template('edit_company.html', company=company)

@app.route('/companies/delete/<int:id>')
def delete_company(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM companies WHERE company_id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('companies'))

# ─── JOBS ────────────────────────────────────────────────
@app.route('/jobs')
def jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT jobs.*, companies.company_name 
        FROM jobs 
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY jobs.job_title
    ''')
    all_jobs = cursor.fetchall()
    conn.close()
    return render_template('jobs.html', jobs=all_jobs)

@app.route('/jobs/add', methods=['GET', 'POST'])
def add_job():
    conn = get_db()
    if request.method == 'POST':
        import json
        requirements = request.form['requirements'].split(',')
        requirements = [r.strip() for r in requirements if r.strip()]
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            request.form['company_id'],
            request.form['job_title'],
            request.form['job_type'],
            request.form['salary_min'] or None,
            request.form['salary_max'] or None,
            request.form['job_url'],
            request.form['date_posted'] or None,
            json.dumps(requirements)
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('jobs'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT company_id, company_name FROM companies ORDER BY company_name')
    companies = cursor.fetchall()
    conn.close()
    return render_template('add_job.html', companies=companies)

@app.route('/jobs/edit/<int:id>', methods=['GET', 'POST'])
def edit_job(id):
    conn = get_db()
    if request.method == 'POST':
        import json
        requirements = request.form['requirements'].split(',')
        requirements = [r.strip() for r in requirements if r.strip()]
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE jobs
            SET company_id=%s, job_title=%s, job_type=%s, salary_min=%s, salary_max=%s,
                job_url=%s, date_posted=%s, requirements=%s
            WHERE job_id=%s
        ''', (
            request.form['company_id'],
            request.form['job_title'],
            request.form['job_type'],
            request.form['salary_min'] or None,
            request.form['salary_max'] or None,
            request.form['job_url'],
            request.form['date_posted'] or None,
            json.dumps(requirements),
            id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('jobs'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM jobs WHERE job_id = %s', (id,))
    job = cursor.fetchone()
    cursor2 = conn.cursor(dictionary=True)
    cursor2.execute('SELECT company_id, company_name FROM companies ORDER BY company_name')
    companies = cursor2.fetchall()
    conn.close()
    import json
    if job['requirements']:
        job['requirements'] = ', '.join(json.loads(job['requirements']))
    return render_template('edit_job.html', job=job, companies=companies)

@app.route('/jobs/delete/<int:id>')
def delete_job(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM jobs WHERE job_id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('jobs'))

# ─── APPLICATIONS ────────────────────────────────────────
@app.route('/applications')
def applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT applications.*, jobs.job_title, companies.company_name
        FROM applications
        JOIN jobs ON applications.job_id = jobs.job_id
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY applications.application_date DESC
    ''')
    all_applications = cursor.fetchall()
    conn.close()
    return render_template('applications.html', applications=all_applications)

@app.route('/applications/add', methods=['GET', 'POST'])
def add_application():
    conn = get_db()
    if request.method == 'POST':
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            request.form['job_id'],
            request.form['application_date'],
            request.form['status'],
            request.form['resume_version'],
            1 if request.form.get('cover_letter_sent') else 0
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('applications'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT jobs.job_id, jobs.job_title, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY companies.company_name
    ''')
    jobs = cursor.fetchall()
    conn.close()
    return render_template('add_application.html', jobs=jobs)

@app.route('/applications/edit/<int:id>', methods=['GET', 'POST'])
def edit_application(id):
    conn = get_db()
    if request.method == 'POST':
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE applications
            SET job_id=%s, application_date=%s, status=%s, resume_version=%s, cover_letter_sent=%s
            WHERE application_id=%s
        ''', (
            request.form['job_id'],
            request.form['application_date'],
            request.form['status'],
            request.form['resume_version'],
            1 if request.form.get('cover_letter_sent') else 0,
            id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('applications'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM applications WHERE application_id = %s', (id,))
    application = cursor.fetchone()
    cursor2 = conn.cursor(dictionary=True)
    cursor2.execute('''
        SELECT jobs.job_id, jobs.job_title, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY companies.company_name
    ''')
    jobs = cursor2.fetchall()
    conn.close()
    return render_template('edit_application.html', application=application, jobs=jobs)

@app.route('/applications/delete/<int:id>')
def delete_application(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM applications WHERE application_id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('applications'))

# ─── CONTACTS ────────────────────────────────────────────
@app.route('/contacts')
def contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT contacts.*, companies.company_name
        FROM contacts
        JOIN companies ON contacts.company_id = companies.company_id
        ORDER BY contacts.contact_name
    ''')
    all_contacts = cursor.fetchall()
    conn.close()
    return render_template('contacts.html', contacts=all_contacts)

@app.route('/contacts/add', methods=['GET', 'POST'])
def add_contact():
    conn = get_db()
    if request.method == 'POST':
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            request.form['company_id'],
            request.form['contact_name'],
            request.form['title'],
            request.form['email'],
            request.form['phone'],
            request.form['linkedin_url'],
            request.form['notes']
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('contacts'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT company_id, company_name FROM companies ORDER BY company_name')
    companies = cursor.fetchall()
    conn.close()
    return render_template('add_contact.html', companies=companies)

@app.route('/contacts/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    conn = get_db()
    if request.method == 'POST':
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE contacts
            SET company_id=%s, contact_name=%s, title=%s, email=%s, phone=%s, linkedin_url=%s, notes=%s
            WHERE contact_id=%s
        ''', (
            request.form['company_id'],
            request.form['contact_name'],
            request.form['title'],
            request.form['email'],
            request.form['phone'],
            request.form['linkedin_url'],
            request.form['notes'],
            id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('contacts'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM contacts WHERE contact_id = %s', (id,))
    contact = cursor.fetchone()
    cursor2 = conn.cursor(dictionary=True)
    cursor2.execute('SELECT company_id, company_name FROM companies ORDER BY company_name')
    companies = cursor2.fetchall()
    conn.close()
    return render_template('edit_contact.html', contact=contact, companies=companies)

@app.route('/contacts/delete/<int:id>')
def delete_contact(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE contact_id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('contacts'))

# ─── JOB MATCH ───────────────────────────────────────────
@app.route('/job-match', methods=['GET', 'POST'])
def job_match():
    results = []
    user_skills = ''
    if request.method == 'POST':
        import json
        user_skills = request.form['skills']
        skill_list = [s.strip().lower() for s in user_skills.split(',') if s.strip()]

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT jobs.*, companies.company_name
            FROM jobs
            JOIN companies ON jobs.company_id = companies.company_id
        ''')
        all_jobs = cursor.fetchall()
        conn.close()

        for job in all_jobs:
            if job['requirements']:
                requirements = [r.lower() for r in json.loads(job['requirements'])]
                matched = [r for r in requirements if r in skill_list]
                missing = [r for r in requirements if r not in skill_list]
                total = len(requirements)
                percent = round((len(matched) / total) * 100) if total > 0 else 0
                results.append({
                    'job_title': job['job_title'],
                    'company_name': job['company_name'],
                    'percent': percent,
                    'matched': matched,
                    'missing': missing,
                    'total': total
                })

        results.sort(key=lambda x: x['percent'], reverse=True)

    return render_template('job_match.html', results=results, user_skills=user_skills)
    
if __name__ == '__main__':
    app.run(debug=True)