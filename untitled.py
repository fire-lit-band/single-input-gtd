from random import choice
import PySimpleGUI as sg

def get_location(element, event):
    widget = element.widget
    region = widget.identify('region', event.x, event.y)
    if region in ('nothing', 'separator'):
        row, col = None, None
    elif region == 'heading':
        row = -1
        col = int(widget.identify_column(event.x)[1:])
    elif region == 'tree':
        row, col = widget.identify_row(event.y), 0
    elif region == 'cell':
        row = widget.identify_row(event.y)
        col = int(widget.identify_column(event.x)[1:])
    if row in element.IdToKey:
        widget.selection_set(row)
        row = element.IdToKey[row]
    return (row, col)

sg.theme("DarkBlue")
sg.set_options(font=('Courier New', 12))

# Add tree data
treedata = sg.TreeData()
data = [[f'Node {i:0>2d}', f'Data 1 - {i:0>2d}', f'Data 2 - {i:0>2d}'] for i in range(5)]
for i, item in enumerate(data):
    parent = choice(list(treedata.tree_dict.keys()))
    treedata.insert(parent, i, item[0], values=item[1:])
    print(item[1:])
# Get keys for all nodes, except root of tree
keys = list(treedata.tree_dict.keys())
keys.remove('')

right_click_menu = ['&Right', ['Edit', 'Cancel']]

layout = [
    [sg.Button('Select 1~3')],
    [sg.Tree(data=treedata, headings=['Data 1', 'Data 2'], auto_size_columns=False,
        num_rows=10, col0_width=30, col_widths=[15, 15], justification='center',
        show_expanded=True, col0_heading='Node',
        # right_click_menu=right_click_menu,
        pad=(0, 0), key='TREE')],
    [sg.Text('', pad=(0, 0), relief=sg.RELIEF_SUNKEN, expand_x=True, key='STATUS')],
]

window = sg.Window('Tree Element Test', layout, use_default_focus=False, margins=(0, 0), finalize=True)
window['Select 1~3'].block_focus()
tree, status = window['TREE'], window['STATUS']
tree.bind('<Button-1>', ' Select')
event =  '<Button-2>' if sg.running_mac() else '<Button-3>'
tree.bind(event, ' Select')
tree.bind('<Double-Button-1>', ' Double')

# Remove the dash box in Table/Tree element
style_name = window['TREE'].widget['style']+'.Item'
style = sg.ttk.Style()
style.layout(style_name,
    [('Treeitem.padding', {'sticky': 'nswe', 'children':
        [('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
            ('Treeitem.image', {'side': 'left', 'sticky': ''}),
            # ('Treeitem.focus', {'side': 'left', 'sticky': '', 'children': [
            ('Treeitem.text', {'side': 'left', 'sticky': ''}),
            # ]})
        ],
    })]
)

while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    elif event == 'TREE Select':
        # values not yet updated for the selection here
        row, col = get_location(tree, tree.user_bind_event)
        if None in (row, col):
            status.update('Click on nothing or separator !')
            row_data = col_data = None
        elif row < 0:
            status.update(f'Click on heading #{col}')
            row_data = col_data = None
        else:
            row_data = data[row]
            col_data = row_data[col]
            status.update(f'{row_data} - {col_data}')

    elif event in ('TREE Double', 'Edit'):
        status.update(f'EDIT - {row_data} - {col_data}')

    elif event in 'Select 1~3':
        ids = tuple(map(lambda x:tree.KeyToID[x], [1, 2, 3]))
        tree.widget.selection_set(ids)
        status.update('Items with key 1 ~ 3 selected !')


window.close()
