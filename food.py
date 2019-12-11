import datetime

import pandas as pd

filename = "Food_2019.csv"


def create_data(date, place, value):
    try:
        file = open(filename, 'r+')
        can_spend = 190

        data_set = pd.read_csv(filename, index_col=False)

        frame = pd.DataFrame(data_set, columns=['Left', 'Date', 'Place', 'Spent'])
        frame = frame.append({"Date": date, "Place": place, "Spent": value}, ignore_index=True)
        frame['Date'] = pd.to_datetime(frame['Date'])
        frame['Week'] = frame['Date'].dt.weekofyear
        frame['Left'] = frame.groupby('Week').apply(lambda x: can_spend - x['Spent'].cumsum()).reset_index(drop=True)

        # write the data-set to the csv
        frame.to_csv(filename, index=None, header=True)
        file.close()
    except IOError:
        file = open(filename, "w")

        frame = pd.DataFrame(columns=['Left', 'Date', 'Place', 'Spent'])
        frame.to_csv(filename, index=None, header=True)
        file.close()


class Food:
    def __init__(self):
        pass

    def menu(self):
        print("-----------------")
        print("1. Print all entries")
        print("2. Create new entry")
        print("3. Delete entry")
        print("4. Search")
        print("-----------------")

        get_input = input("> ")
        self.get_choice(get_input)

    def get_choice(self, choice):
        while choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "q" and choice != "Q":
            print("Invalid choice!\n")
            choice = input("> ")

        if choice == "1":
            self.print_entries()
        elif choice == "2":
            self.create_new_entry()
        elif choice == "3":
            self.delete_entry()
        elif choice == "4":
            self.search()
        else:
            exit()

    def create_new_entry(self):
        get_date = input("Date: ")
        get_place = input("Place: ")
        get_amount = float(input("Amount: "))
        create_data(get_date, get_place, get_amount)

    def delete_entry(self):
        pass

    def search(self):
        food_csv = pd.read_csv(filename)
        get_input = input("Date: ")
        convert_date = datetime.datetime.strptime(get_input, '%m/%d/%y').strftime("%W")
        print(food_csv.loc[food_csv['Week'].isin([convert_date])])

    def print_entries(self):
        food_csv = pd.read_csv(filename)
        print(food_csv)
        # print(food_csv.groupby(by='Week'))


def main():
    food = Food()
    while True:
        food.menu()
        print()


if __name__ == "__main__":
    main()
