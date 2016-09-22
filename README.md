# random_santa
A program to help organise a "Secret Santa".

Provide it with a list of participants (name and email address), a list of
exclusions (person A will not be asked to get a present for person B), a
template email message to send to each participant (with placeholders for the
names of the giver and receiver), and credentials for a gmail account.

It will randomly assign each person another for whom to buy a present, and
email all participants with their assignments. The graph of present
assignments will be a ring. It may fail if you have too many exclusions. If
this happens you should learn to get along better with your friends and
family.

### Example:
```
from random_santa import go_go_secret_santa
go_go_secret_santa("people.txt", "exclusions.txt", "credentials.txt",
                   "message.txt", "output.txt", write_to_file=True, email_for_real=True)
```
Or just...
```
python random_santa
```
This will use the default file names.

The input files should look like the examples below.

##### people.txt
```
Alice, alice@example.com
Bob, bob@example.com
Charlie, charlie@example.com
Danielle, danielle@example.com
Ethelred, ethelred@example.com
```

##### exclusions.txt
```
Alice, Bob
Bob, Alice
```

##### credentials.txt
```
my.gmail.user.name
MyGM4ilPassW0RD
```
##### message.txt
First line is the subject.
```
Secret Santa Assignment
HO HO HO!

Hi there {giver}. Santa here. I've been asked to help set up the Secret Santa this
year. I've drawn names out of a hat, and determined that you should get a
present for {receiver}.

Merry Christmas!
```
