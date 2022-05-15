from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/index/', methods=['GET', 'POST'])
def index():
    history = downloading_history_form_file('in.txt')
    data = request.form
    balance_change = data.getlist('balance_change')
    comment = data.getlist('comment')
    for a in balance_change:
        for b in comment:
            temporary = 'saldo', a, b
            history.append(temporary)
    product_name_purchase = data.getlist('product_name_purchase')
    product_price_purchase = data.getlist('product_price_purchase')
    product_amount_purchase = data.getlist('product_amount_purchase')
    for a in product_name_purchase:
        for b in product_price_purchase:
            for c in product_amount_purchase:
                temporary = 'zakup', a, b, c
                history.append(temporary)
    product_name_sale = data.getlist('product_name_sale')
    product_price_sale = data.getlist('product_price_sale')
    product_amount_sale = data.getlist('product_amount_sale')
    for a in product_name_sale:
        for b in product_price_sale:
            for c in product_amount_sale:
                temporary = 'sprzedaz', a, b, c
                history.append(temporary)
    rewrite_with_updated_history(history, 'in.txt')

    return render_template('index.html')


@app.route('/index/balance/')
def balance():
    balance = working_on_the_data()[0]
    return render_template('balance.html', balance=balance)


@app.route('/index/warehouse/')
def warehouse():
    warehouse = [working_on_the_data()[1]]
    print(warehouse)
    return render_template('warehouse.html', warehouse=warehouse)


@app.route('/index/history/', methods=['GET', 'POST'])
def history():
    history = downloading_history_form_file('in.txt')
    ls = []
    data = request.form
    line_from = data.getlist('line_from')
    line_to = data.getlist('line_to')
    for a in line_from:
        for b in line_to:
            temporary = a, b
            ls += temporary
    if len(ls) > 0:
        if '' in ls:
            ...
        else:
            temp_history = []
            for nr in range(int(ls[0]), int(ls[1]) + 1):
                temp_history.append(history[nr])
            history = temp_history
    else:
        ...
    return render_template('history.html', history=history)


def downloading_history_form_file(file_path):
    history = []
    file = open(file_path, 'r')

    while True:
        line = file.readline().strip()
        if line == "saldo":
            balance_change = file.readline().strip()
            comment = file.readline().strip()
            temp_list = "saldo", balance_change, comment
            history.append(temp_list)
            continue
        elif line == "zakup":
            product_name = file.readline().strip()
            product_price = file.readline().strip()
            number_of_items = file.readline().strip()
            temp_list = "zakup", product_name, product_price, number_of_items
            history.append(temp_list)
        elif line == "sprzedaz":
            product_name = file.readline().strip()
            product_price = file.readline().strip()
            number_of_items = file.readline().strip()
            temp_list = "sprzedaz", product_name, product_price, number_of_items
            history.append(temp_list)
        else:
            if line == "stop" or False:
                break
    return history


def rewrite_with_updated_history(history, file_path):
    file = open(file_path, 'w')
    for idx_1 in history:
        for idx in idx_1:
            file.write(str(idx) + "\n")
    file.write("stop" + '\n')


def working_on_the_data():
    history = downloading_history_form_file('in.txt')
    balance = 0
    warehouse = {}
    names = []
    amounts = []

    for command in history:
        if command[0] == "saldo":
            balance_change = int(command[1])
            if balance + balance_change < 0:
                print("Błąd. Za mało środków na koncie.")
                break
            balance += balance_change
        elif command[0] == "zakup":
            purchase_price = int(command[2]) * int(command[3])
            if balance < purchase_price:
                print("Błąd, nie stać cię na zakup.")
                break
            balance -= purchase_price
            if command[1] not in names:
                names.append(command[1])
                amounts.append(command[3])
            else:
                new_value = int(names.index(command[1])) + int(command[3])
                position = names.index(command[1])
                amounts[position] = int(amounts[position]) + new_value
            for idx in range(len(names)):
                warehouse[names[idx]] = amounts[idx]
        elif command[0] == "sprzedaz":
            sale_price = int(command[2]) * int(command[3])
            balance += sale_price
            for idx in names:
                if command[1] == idx:
                    position = names.index(idx)
                    amounts[position] = int(amounts[position]) - int(command[3])
            for idx_1 in range(len(names)):
                warehouse[names[idx_1]] = amounts[idx_1]
    return balance, warehouse
