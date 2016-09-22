#!/usr/bin/env python3

import numpy as np
import smtplib
from email.mime.text import MIMEText

NUM_TRIES = 100

DEFAULT_PEOPLE_FILE = "people.txt"
DEFAULT_EXCLUSIONS_FILE = "exclusions.txt"
DEFAULT_MESSAGE_FILE = "message.txt"
DEFAULT_CREDENTIALS_FILE = "credentials.txt"
DEFAULT_OUTPUT_FILE = "output.txt"


def read_people_file(path):
    people = [] # list of (name, email) tuples
    with open(path) as f:
        for line in f:
            bits = line.split(',')
            if len(bits) != 2:
                raise RuntimeError("Each line of the people file must"
                                   "contain a name and an email: " + line)
            if '@' not in bits[1]:
                raise RuntimeError("Not a valid email address: " + line)
            people.append((bits[0].strip(), bits[1].strip()))
    return people


def read_exclusion_file(path, people):
    names = [p[0] for p in people]
    exclusions = [] # list of (subject, object) tuples
    with open(path) as f:
        for line in f:
            bits = line.split(',')
            if len(bits) != 2:
                raise RuntimeError("Each line of the exclusion file must"
                                   "contain two name: " + line)
            subj = bits[0].strip()
            obj = bits[1].strip()
            if subj not in names:
                raise RuntimeError("Unrececognised name: " + subj)
            if obj not in names:
                raise RuntimeError("Unrececognised name: " + obj)
            exclusions.append((subj, obj))
    return exclusions


def read_credentials_file(path):
    with open(path) as f:
        username = f.readline().strip()
        password = f.readline().strip()
    return (username, password)


def read_message_file(path):
    with open(path) as f:
        subject = f.readline().strip()
        body = "".join(f.readlines())
    return (subject, body)


def build_random_graph(people, exclusions):

    num_people = len(people)

    for _ in range(NUM_TRIES):

        # Build a list of potential objects for each subject
        options_list = [[o for o in people if (s is not o and (s[0],o[0]) not in exclusions)] for s in people]
        options = {s: opt for (s, opt) in zip(people, options_list)}

        # Pick someone to start with
        num_options = np.array([len(o) for o in options_list])
        starter = people[np.random.choice(np.where(num_options == num_options.min())[0])]
        subj = starter

        assignments = []
        while len(assignments) < num_people:

            # Make a list of object choices - cannot get starter until the last pick
            objects = list(options[subj])
            if (len(assignments) < (num_people - 1)) and (starter in objects):
                objects.remove(starter)

            # Fail if there are no valid options
            if len(objects) == 0:
                break

            # Pick someone
            obj = objects[np.random.choice(len(objects))]
            assignments.append((subj, obj))

            # Don't let anyone else get this person
            for p in people:
                if obj in options[p]:
                    options[p].remove(obj)

            # Object is subject for next iteration
            subj = obj

        if len(assignments) == num_people:
            return assignments

    raise RuntimeError("Failed to find a valid set of present assignment. "
                       "Sorry about that. Try removing some exclsuions.")


def build_email(assignment, from_address, subject, body):
    msg = MIMEText(body.format(giver=assignment[0][0], receiver=assignment[1][0]))
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = assignment[0][1]
    return msg


def go_go_secret_santa(people_file, exclusions_file,
                       credentials_file, message_file, output_file,
                       write_to_file=False, email_for_real=False):
    people = read_people_file(people_file)
    exclusions = read_exclusion_file(exclusions_file, people)
    subject, body = read_message_file(message_file)
    credentials = read_credentials_file(credentials_file)
    from_address = credentials[0] + "@gmail.com"

    assignments = build_random_graph(people, exclusions)

    with open(output_file, 'w') as f:
        for a in assignments:
            s = a[0][0] + " gets something for " + a[1][0]
            if write_to_file:
                f.write(s + "\n")
            else:
                print(s)

    if email_for_real:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(credentials[0], credentials[1])
    else:
        try:
            server = smtplib.SMTP('localhost', port=1025)
        except ConnectionRefusedError:
            raise ConnectionRefusedError("Could not connect to local test server. Run this in a terminal:"
                                         "python -m smtpd -n -c DebuggingServer localhost:1025")

    for a in assignments:
        msg = build_email(a, from_address, subject, body)
        server.send_message(msg)
    server.quit()

# Run it
if __name__ == "__main__":
    go_go_secret_santa(DEFAULT_PEOPLE_FILE,
                       DEFAULT_EXCLUSIONS_FILE,
                       DEFAULT_CREDENTIALS_FILE,
                       DEFAULT_MESSAGE_FILE,
                       DEFAULT_OUTPUT_FILE)
