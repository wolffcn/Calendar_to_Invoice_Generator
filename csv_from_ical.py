import icalendar
from datetime import date
import re
import csv
import pandas as pd
from Invoices import client_info as c


today = date.today()
STUDENT_NAMES = c.student_names
RATE_ONE = c.rate_one
RATE_TWO = c.rate_two

question = input("What mont"
                 "h (MM) are you making invoices for? ")


def read_calendar(file_path):
    with open(file_path, 'rb') as e:
        ecal = icalendar.Calendar.from_ical(e.read())
    return ecal


def clean_summary(summary):
    delete_from_summary = ["Combo", "Lunch", "Break", "Open", "Free"]
    summary = summary.strip(',').title()
    summary = re.sub(r'\(.*?\)', '', summary)
    summary = summary.replace("-", " ").replace(",", " ")
    sum_list = summary.split()
    for word in delete_from_summary:
        if word in sum_list:
            sum_list.remove(word)
    return sum_list


def get_event_month(event):
    return event.decoded("dtstart").strftime("%Y-%m")

def filter_events_by_month(events, target_months):
    filtered_events = []
    for event in events:
        event_month = get_event_month(event)
        if event_month in target_months:
            filtered_events.append(event)
    return filtered_events

def extract_student_invoices(events, student_names):
    invoices = []
    for event in events:
        summary = event.get("summary")
        cleaned_summary = clean_summary(summary)
        for name in student_names:
            if name in cleaned_summary:
                index_of_les_len = cleaned_summary.index(name) + 1
                try:
                    lesson_length = int(cleaned_summary[index_of_les_len])
                except (ValueError, IndexError):
                    lesson_length = 0

                charge = round(((lesson_length / 60) * (36 if name in RATE_ONE else 40)), 2)

                invoices.append({
                    'Date': event.decoded("dtstart").strftime("%m/%d/%Y"),
                    'Student': name,
                    'Lesson Length': lesson_length,
                    'Charge': charge
                })
                invoices = sorted(invoices, key=lambda x: x['Date'])

    return invoices

def generate_invoices(ecal, student_names):
    target_months = f"2024-{question}"
    events = [event for event in ecal.walk() if event.name == "VEVENT" and event.get("summary") is not None]
    filtered_events = filter_events_by_month(events, target_months)
    invoices = extract_student_invoices(filtered_events, student_names)
    return invoices

def list_of_totals(invoices, student_names):
    monthly_totals = []
    for name in student_names:
        filtered_invoice = [inv['Charge'] for inv in invoices if inv['Student'] == name]
        total = sum(filtered_invoice)
        monthly_totals.append(total)
    monthly_total = round(sum(monthly_totals), 2)
    return f"The total invoices from {question} is: ${monthly_total}"




def write_invoices_to_csv(invoices, student_names):
    field_names = ['Date', 'Student', 'Lesson Length', 'Charge', 'Total']
    for name in student_names:
        filtered_invoices = [inv for inv in invoices if inv['Student'] == name]
        with open(f'Invoices/{name}-{question}.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(filtered_invoices)

        df = pd.read_csv(f'Invoices/{name}-{question}.csv')
        total = round(df['Charge'].sum(), 2)








