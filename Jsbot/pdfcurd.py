import csv
import os

def read_csv(file_path):
    records = []
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            records.append(row)
    return records

def write_csv(file_path, records):
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(records)

def add_record(file_path, new_record):
    records = read_csv(file_path)
    records.append(new_record)
    write_csv(file_path, records)
    print("Record added successfully.")

def delete_record(file_path, record_to_delete):
    records = read_csv(file_path)
    if record_to_delete in records:
        records.remove(record_to_delete)
        write_csv(file_path, records)
        print("Record deleted successfully.")
    else:
        print("Record not found.")

def main():
    file_path = 'example.csv'

    # Adding a record
    new_record = ['John Doe', '30', 'john@example.com']
    add_record(file_path, new_record)

    # Displaying the current records
    current_records = read_csv(file_path)
    print("Current Records:")
    for record in current_records:
        print(record)

    # Deleting a record
    record_to_delete = ['Jane Doe', '25', 'jane@example.com']
    delete_record(file_path, record_to_delete)

    # Displaying the updated records
    updated_records = read_csv(file_path)
    print("\nUpdated Records:")
    for record in updated_records:
        print(record)

if __name__ == "__main__":
    main()
