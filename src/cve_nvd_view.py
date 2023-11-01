import requests
from flask import render_template, request, Response, session, redirect, url_for
from flask.views import MethodView
from flask_login import login_required, current_user, logout_user


class NvdCveView(MethodView):
    decorators = [login_required]  # Requires authentication

    def __init__(self, host_addr):
        self.get_url: str = host_addr

    def get(self):
        print(current_user.is_authenticated)
        if current_user.is_authenticated:
            task = request.args.get('task')
            year = request.args.get('year')
            range = request.args.get('range')
            if task or year or range:
                params = {'year': year, 'range': range}
                print(self.get_url + task)
                response = requests.get(self.get_url + task, params=params, verify=False)
                print(response.status_code)
                if response.status_code == 200:
                    # Relay the HTML content to the client
                    return Response(response.content, content_type='text/html')
                else:
                    # Handle errors, e.g., return an error page
                    return "Failed to retrieve HTML content from Service 1", 500
            return render_template('fetch_pages.html')
        else:
            render_template('login.html')

    def before_request(self):
        if session.get('_permanent') and session['_permanent'] and 'user_id' not in session:
            # Session has expired
            logout_user()
            return redirect(url_for('login'))  # Redirect to the login page

