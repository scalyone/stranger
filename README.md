# README #

Perform email validation in style using stranger.

### What does stranger do? ###

Manually logging in and trying to capture good vs bad packets with Burp Suite to use in intruder is a thing of the past. On top of that, it just sucks and is annoying because it might not even properly work. Why not just do it the old fashioned way?

What stranger does is takes a file as a parameter containing emails you want validated.
It will read an email address, strip the domain, perform a dig on it for the MX record, and finally attempt to rcpt to the email. On 250 it's good, on 550 it's either bad or maybe you're added to a spam filter.
Lucky for you I print out the 550s so you don't need to stay awake at night wondering why joeshmoe@pepethefrog.com failed to validate.

### Steps ###

* Use the tool on a file that only contains emails separated by newlines.
```python3 stranger.py --file <file>```

* In my example it would be:
```python3 stranger.py --file validate.txt```

* I set a random delay between 4-6 minutes per as an attempt to avoid spam filters
* It will write out valid and invalid emails to separate text files: valid_emails.txt and invalid_emails.txt
* I recommend copying invalid_emails.txt to something and rerunning it on that just in case

### Arguments ###

```plaintext
usage: stranger.py [-h] [--min MIN] [--max MAX] [--file FILE]

Perform email validation. I recommend using the default delay times so your IP is not added to
a spam/block list.

optional arguments:
  -h, --help   show this help message and exit
  --min MIN    Minimum delay time (in seconds) before sending requests. DEFAULT: 240 (4
               minutes)
  --max MAX    Maximum delay time (in seconds) before sending requests. DEFAULT 360 (6
               minutes)
  --file FILE  File containing a list of just emails to validate. [required]
```
