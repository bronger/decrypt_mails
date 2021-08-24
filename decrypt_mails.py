#!/usr/bin/env python3

import pickle, os, argparse, logging
from pathlib import Path
import email, email.policy
from xdg import xdg_cache_home


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")


parser = argparse.ArgumentParser(description="Decrypt mail files in place.")
parser.add_argument("maildir", type=Path, help="root path of the mail archive")
args = parser.parse_args()
mail_root = args.maildir.resolve()


configuration_path = xdg_cache_home()/"decrypt_mails.pickle"
try:
    already_seen = set(pickle.load(open(configuration_path, "rb")))
except FileNotFoundError:
    already_seen = set()


def process_message(message):
    return message

def archive_mail(filepath):
    destination = mail_root/".decrypt_mails_backup"/filepath.relative_to(mail_root)
    assert not destination.exists()
    destination.parent.mkdir(parents=True, exist_ok=True)
    logging.info(f"Move {filepath} ==> {destination}")
    os.rename(filepath, destination)

for root, __, filenames in os.walk(mail_root):
    root = Path(root)
    for filename in filenames:
        filepath = root/filename
        if filepath not in already_seen:
            try:
                with open(filepath, "rb") as email_file:
                    message = email.message_from_binary_file(email_file)
            except FileNotFoundError:
                logging.warning(f"path {filepath} could not be found.  Broken symbolic link?")
            else:
                if message.keys():
                    new_message = process_message(message)
                    if new_message is not message:
                        archive_mail(filepath)
                        logging.info(f"writing new {filepath}")
                        with open(filepath, "wb") as email_file:
                            email_file.write(new_message.as_bytes())
                else:
                    logging.debug(f"Ignoring {filepath} because it does not seem to be an email")
            already_seen.add(filepath)


pickle.dump(already_seen, open(configuration_path, "wb"))
