from pymongo import MongoClient
from tkinter import *
from tkinter.ttk import *
import copy

client = MongoClient('mongodb://192.168.112.103')
db = client['22303']

collection = db['rkuzmin']

preset_team = {
    'name': 'PTZ Team',
    'city': 'Petrozavodsk',
    'coach name': 'Kazakov G. G.',
    'players': [
        {
            'name': 'Voronin M. I.',
            'position': '1'
        },
        {
            'name': 'Saveliev M. L.',
            'position': '2'
        },
        {
            'name': 'Ivanov T. M.',
            'position': '3'
        },
        {
            'name': 'Gusev A. D.',
            'position': '4'
        },
        {
            'name': 'Aksenov N. R.',
            'position': '5'
        },
        {
            'name': 'Petrov D. A.',
            'position': '6'
        },
        {
            'name': 'Ivanov A. E.',
            'position': '7'
        },
        {
            'name': 'Belousov M. M.',
            'position': '8'
        },
        {
            'name': 'Homyakov G. A.',
            'position': '9'
        },
        {
            'name': 'Andreev S. M.',
            'position': '10'
        },
        {
            'name': 'Voronov A. D.',
            'position': '11'
        }
    ],
    'reserve players': [
        'Blohin M. D.',
        'Cherkasov M. M.',
        'Panin T. M.',
        'Kolesnikov A. L.'
    ]
}

preset_game = {
    'date': '20.11.2022',
    'score': '0:2',
    'rules violations': [
        {
            'card': 'yellow',
            'name': 'Andreev S. M.',
            'minute': '12',
            'reason': 'Deliberate hand play'
        }
    ],
    'goals': [
        {
            'name': 'Gusev A. D.',
            'position': '4',
            'minute': '10',
            'pass': 'accurate pass'
        },
        {
            'name': 'Belousov M. M.',
            'position': '8',
            'minute': '14',
            'pass': 'short pass'
        }
    ],
    'penalties': [
        {
            'name': 'Aksenov N. R.',
            'position': '5',
            'minute': '6',
            'pass': 'wall pass'
        }
    ],
    'shots number on goal': [
        {
            'name': 'Belousov M. M.',
            'position': '8',
            'minute': '8',
            'pass': 'accurate pass'
        },
        {
            'name': 'Petrov D. A.',
            'position': '6',
            'minute': '19',
            'pass': 'accurate pass'
        },
        {
            'name': 'Voronov A. D.',
            'position': '11',
            'minute': '16',
            'pass': 'chip pass'
        },
        {
            'name': 'Belousov M. M.',
            'position': '8',
            'minute': '5',
            'pass': 'short pass'
        }
    ]
}

collection.delete_many({})
collection.insert_one(preset_team)
collection.insert_one(preset_game)

pattern_team = {
    'name': '',
    'city': '',
    'coach name': '',
    'players': [
        {
            'name': '',
            'position': ''
        }
    ],
    'reserve players': [
        ''
    ]
}

pattern_game = {
    'date': '',
    'score': '',
    'rules violations': [
        {
            'card': '',
            'name': '',
            'minute': '',
            'reason': ''
        }
    ],
    'goals': [
        {
            'name': '',
            'position': '',
            'minute': '',
            'pass': ''
        }
    ],
    'penalties': [
        {
            'name': '',
            'position': '',
            'minute': '',
            'pass': ''
        }
    ],
    'shots number on goal': [
        {
            'name': '',
            'position': '',
            'minute': '',
            'pass': ''
        }
    ]
}

current_document = copy.deepcopy(pattern_team)

root = Tk()
root.title('DB2 Lab2.1')
root.geometry('900x550')

value_label = Label(text='Enter the key-value (example: players.0.name = Shkut V. V.)')
value_label.place(x=20, y=20)
value_entry = Text()
value_entry.place(x=20, y=50, width=320, height=120)

documents_text = Text()
documents_text.place(x=20, y=180, width=860, height=350)
documents_text.configure(state=DISABLED)


def update_documents_text():
    global current_document
    documents_text.configure(state=NORMAL)
    documents_text.delete('1.0', END)
    documents_text.insert(1.0, current_document)
    documents_text.configure(state=DISABLED)


document_type_selection_combobox = Combobox(values=['Teams', 'Games'], state="readonly")
document_type_selection_combobox.place(x=350, y=50)
document_type_selection_combobox.current(newindex=0)


def switch_document_type(event):
    global current_document
    if document_type_selection_combobox.get() == 'Teams':
        current_document.clear()
        current_document = copy.deepcopy(pattern_team)
    else:
        current_document.clear()
        current_document = copy.deepcopy(pattern_game)
    update_documents_text()


document_type_selection_combobox.bind('<<ComboboxSelected>>', switch_document_type)


def add_value():
    key_value = value_entry.get(1.0, END).split(' = ')
    key = key_value[0].split('.')
    value = key_value[1].replace('\n', '')
    keys_number = len(key)
    global current_document
    match keys_number:
        case 1:
            current_document[key[0]] = value
        case 2:
            try:
                current_document[key[0]][int(key[1])] = value
            except IndexError:
                current_document[key[0]].append('')
                current_document[key[0]][int(key[1])] = value
        case 3:
            try:
                current_document[key[0]][int(key[1])][key[2]] = value
            except IndexError:
                if key[0] == 'players':
                    current_document[key[0]].append({'name': '', 'position': ''})
                    current_document[key[0]][int(key[1])][key[2]] = value
                elif key[0] == 'rules violations':
                    current_document[key[0]].append({'card': '', 'name': '', 'minute': '', 'reason': ''})
                    current_document[key[0]][int(key[1])][key[2]] = value
                else:
                    current_document[key[0]].append({'name': '', 'position': '', 'minute': '', 'pass': ''})
                    current_document[key[0]][int(key[1])][key[2]] = value
    update_documents_text()


add_key_value_button = Button(text='Add value', command=add_value)
add_key_value_button.place(x=350, y=140, width=110, height=30)


def save_document():
    collection.insert_one(current_document)
    show_documents()


save_documents_button = Button(text='Save document', command=save_document)
save_documents_button.place(x=470, y=140, width=110, height=30)


def show_documents():
    documents = ''
    for document in collection.find({}, {'_id': 0}):
        documents += str(document) + '\n\n'
    documents_text.configure(state=NORMAL)
    documents_text.delete('1.0', END)
    documents_text.insert(1.0, documents)
    documents_text.configure(state=DISABLED)


show_documents_button = Button(text='Show documents', command=show_documents)
show_documents_button.place(x=590, y=140, width=110, height=30)

root.mainloop()

client.close()
