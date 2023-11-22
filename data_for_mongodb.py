class DataMongo:
    def __init__(self):
        self.game = self.exist_game
        self.team = self.exist_teams

    @property
    def exist_game(self):
        game = {'date': '01.01.2023', 'score': '0:2', 'rules violations': {
            'card': 'yellow',
            'name': 'Andreev S. M.',
            'minute': '12',
            'reason': 'Deliberate hand play'
        }, 'goals': [{
            'name': 'Semenov V.M.',
            'position': '4',
            'minute': '19',
            'pass': 'accurate pass'
        }, {
            'name': 'Tervoch K.K.',
            'position': '3',
            'minute': '5',
            'pass': 'short pass'
        }],
                'penalties': {
                    'name': 'Sergeev I.I.',
                    'position': '6',
                    'minute': '6',
                    'pass': 'wall pass'
                }, 'shots_number_goals': [{'name': 'Semenov V.M.',
                                           'position': '4',
                                           'minute': '19',
                                           'pass': 'accurate pass'
                                           }, {
                                              'name': 'Tyrin S.S.',
                                              'position': '10',
                                              'minute': '16',
                                              'pass': 'chip pass'
                                          },
                                          {
                                              'name': 'Tervoch K.K.',
                                              'position': '3',
                                              'minute': '5',
                                              'pass': 'short pass'
                                          }]}
        return game

    @property
    def exist_teams(self):
        reserve_players = ['Chetkov V.V.', 'Kuznetsov V.V.', 'Peshkin V.V.', 'Venchik V.V.', 'Semchik V.V.']
        players = [{'name': 'Petrov V.V.', 'position': '1'},
                   {'name': 'Ivanov V.V.', 'position': '2'},
                   {'name': 'Tervoch K.K.', 'position': '3'},
                   {'name': 'Semenov V.M.', 'position': '4'},
                   {'name': 'Laitenen H.D.', 'position': '5'},
                   {'name': 'Sergeev I.I.', 'position': '6'},
                   {'name': 'Zubkov I.L.', 'position': '7'},
                   {'name': 'Lekander O.N.', 'position': '8'},
                   {'name': 'Gromov V.A.', 'position': '9'},
                   {'name': 'Tyrin S.S.', 'position': '10'},
                   {'name': 'Jorjev K.A.', 'position': '11'}]
        team = {'name': 'Kyshtym', 'city': 'Kyshtym_team', 'coach_name': 'Leva D.S.', 'players': [{'name': 'Petrov V.V.', 'position': '1'},
                                                                                                  {'name': 'Ivanov V.V.', 'position': '2'},
                                                                                                  {'name': 'Tervoch K.K.', 'position': '3'},
                                                                                                  {'name': 'Semenov V.M.', 'position': '4'},
                                                                                                  {'name': 'Laitenen H.D.', 'position': '5'},
                                                                                                  {'name': 'Sergeev I.I.', 'position': '6'},
                                                                                                  {'name': 'Zubkov I.L.', 'position': '7'},
                                                                                                  {'name': 'Lekander O.N.', 'position': '8'},
                                                                                                  {'name': 'Gromov V.A.', 'position': '9'},
                                                                                                  {'name': 'Tyrin S.S.', 'position': '10'},
                                                                                                  {'name': 'Jorjev K.A.', 'position': '11'}],
                'reserve_players': ['Chetkov V.V.', 'Kuznetsov V.V.', 'Peshkin V.V.', 'Venchik V.V.', 'Semchik V.V.']}
        return team
