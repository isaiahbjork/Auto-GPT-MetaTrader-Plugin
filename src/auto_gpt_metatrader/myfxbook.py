import requests

class myfxbook:

    base_url = 'https://www.myfxbook.com/api/'
    email = None
    password = None
    session = None
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def login(self):
        login = requests.get(self.base_url + 'login.json', params={'email': self.email, 'password': self.password}).json()
        self.session = login['session']
        return login

    def logout(self):
        logout = requests.get(self.base_url + 'logout.json', params={'session': self.session}).json()
        self.session = None
        return logout
    
    def get_my_accounts(self):
        return requests.get(self.base_url + 'get-my-accounts.json', params={'session': self.session}).json()
    
    def get_watched_accounts(self):
        return requests.get(self.base_url + 'get-watched-accounts.json', params={'session': self.session}).json()
    
    def get_open_orders(self, id):
        return requests.get(self.base_url + 'get-open-orders.json', params={'session': self.session, 'id': id}).json()
    
    def get_open_trades(self, id):
        return requests.get(self.base_url + 'get-open-trades.json', params={'session': self.session, 'id': id}).json()
    
    def get_history(self, id):
        return requests.get(self.base_url + 'get-history.json', params={'session': self.session, 'id': id}).json()
    
    def get_daily_gain(self, id, start, end):
        return requests.get(self.base_url + 'get-daily-gain.json', params={'session': self.session, 'id': id, 'start': start, 'end': end}).json()
    
    def get_gain(self, id, start, end):
        return requests.get(self.base_url + 'get-gain.json', params={'session': self.session, 'id': id, 'start': start, 'end': end}).json()
    
    def get_custom_widget(self, id, width, height, bgcolor, chartbgc, gridcolor, linecolor, barcolor, fontcolor, bart, linet, charttitle, titles):
        return requests.get(self.base_url + 'get-custom-widget.json', params={'session': self.session, 'id': id, 'width': width, 'height': height, 'bgcolor': bgcolor, 'chartbgc': chartbgc, 'gridcolor': gridcolor, 'linecolor': linecolor, 'barcolor': barcolor, 'fontcolor': fontcolor, 'bart': bart, 'linet': linet, 'charttitle': charttitle, 'titles': titles}).json()
    
    def get_community_outlook(self):
        return requests.get(self.base_url + 'get-community-outlook.json', params={'session': self.session}).json()
    
    def get_community_outlook_by_country(self, symbol):
        return requests.get(self.base_url + 'get-community-outlook-by-country.json', params={'session': self.session, 'symbol': symbol}).json()
    
    def get_data_daily(self, id, start, end):
        return requests.get(self.base_url + 'get-data-daily.json', params={'session': self.session, 'id': id, 'start': start, 'end': end}).json()