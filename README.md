# random_santa
A program to help organise a "Secret Santa".

Provide it with a list of participants (name and email address), a list of
exclusions (person A will not be asked to get a present for person B) and
credentials for a gmail account.

It will randomly assign each person another for whom to buy a present, and
email all participants with their assignments. The graph of present
assignments will be a ring. It may fail if you have too many exclusions. If
this happens you should learn to get along better with your friends and
family.

### Example:
```
from random_santa import generate_secret_santa
generate_secret_santa("people.txt", "exclusions.txt",
                      "credentials.txt", "output.txt",
                      write_to_file=True, email_for_real=True)
```

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
