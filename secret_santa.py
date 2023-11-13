import random
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

from email_sender import EmailSender


@dataclass
class Participant:
    first_name: str
    last_name: str
    email: str

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __hash__(self):
        return hash(self.email)

    def __str__(self):
        return f'{self.first_name} {self.last_name} -> {self.email}'


class SecretSanta:

    def __init__(self, participant_file: str):
        self.participants: List[Participant] = []
        self.non_participants: List[Participant] = []
        self.assignments: Dict[Participant, Participant] = dict()

        # Read the input file
        with open(participant_file, 'r', encoding='utf-8') as file:
            file_lines = file.readlines()

        # Sort the potential participants
        for line in file_lines:
            name, email = line.split(',')
            first_name = name.split()[0]
            last_name = ' '.join(name.split()[1:])
            participant = Participant(first_name, last_name, email.strip())
            if line.startswith('#'):
                participant.first_name = participant.first_name.strip('#')
                self.non_participants.append(participant)
            else:
                self.participants.append(participant)

        self.participants.sort(key=lambda p: p.first_name)
        self.non_participants.sort(key=lambda p: p.first_name)

    def assign_gifts(self):
        shuffled_participants = self.participants.copy()
        random.shuffle(shuffled_participants)

        # Each participant must give gift to the next one
        for gifter, giftee in zip(shuffled_participants, shuffled_participants[1:]):
            self.assignments[gifter] = giftee

        # The last participant must give gift to the first one
        self.assignments[shuffled_participants[-1]] = shuffled_participants[0]

        # Write assignations to file
        with open('assignations.txt', 'w') as file:
            file.write(f'# Generated on {datetime.now()}\n\n')

            for gifter, giftee in self.assignments.items():
                file.write(f'{gifter} -> {giftee}\n')

    def send_emails(self):
        email_sender = EmailSender()
        email_sender.connect()
        for gifter, giftee in self.assignments.items():
            text_message = self.generate_message(gifter, giftee)
            html_message = self.generate_html_message(gifter, giftee)
            email_sender.send_email(gifter.email,
                                    'Secret Santa: Here is your lucky colleague !',
                                    text_message,
                                    html_message)
        email_sender.disconnect()

    @staticmethod
    def generate_message(from_gifter: Participant, to_giftee: Participant):
        return f'🎅 Hello {from_gifter.first_name} !\nThis year, you must give a gift to :\n' \
               f'\n' \
               f'🎁➡  {to_giftee.full_name}  ⬅🎁\n' \
               f'\n' \
               f'Reminder : The max budget for your gift is 25.-CHF\n' \
               f'Reminder 2 : You have to give a gift to {to_giftee.full_name}\n' \
               f'Reminder 3 : Please read reminder 2 again\n' \
               f'🎄🎄 See you soon 🎄🎄\n\n' \
               f'Santa\n\n' \
               f'Please note that this message was generated and sent automatically with a magic script. The secret santa admin did not read it.\n' \
                'To keep your lucky colleague secret, please do not reply to this message.'

    @staticmethod
    def generate_html_message(from_gifter: Participant, to_giftee: Participant):
        return f"""
<html>
    <head></head>
    <body>
        <p>🎅 Hello {from_gifter.first_name} !</p>
        <p>This year, you must give a gift to :</p>
        <br/>
        <p>🎁➡  <strong>{to_giftee.full_name}</strong>  ⬅🎁</p>
        <br/>
        <p>Reminder : The max budget for your gift is 25.-CHF<br/>
        Reminder 2 : You have to give a gift to {to_giftee.full_name}<br/>
        Reminder 3 : Please read reminder 2 again</p>
<p>🎄🎄 See you soon 🎄🎄</p>
<p>Santa</p>
<p><i>Please note that this message was generated and sent automatically with a magic script. The secret santa admin did not read it.<br>
        To keep your lucky colleague secret, please do not reply to this message.</i></p>
</body>
</html>"""

    def print_summary(self):
        print('==  Summary  ==')
        print(f'Input persons: {len(self.participants) + len(self.non_participants)}')
        print(f'Participants: {len(self.participants)}')
        print(f'Non-participants: {len(self.non_participants)}')
        print()

        non_participants_str = '\n'.join([str(non_participant) for non_participant in self.non_participants])
        print(f'Non-participants: \n{non_participants_str}')
        print()
        participants_str = '\n'.join([str(participant) for participant in self.participants])
        print(f'Participants: \n{participants_str}')


if __name__ == '__main__':
    secret_santa = SecretSanta('participants.txt')
    secret_santa.assign_gifts()
    secret_santa.print_summary()
    print('Sending emails...')
    secret_santa.send_emails()
    print('...Done !')
