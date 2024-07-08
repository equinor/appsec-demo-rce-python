# AppSec Demo: RCE via legacy dependency in Python
A simple demo showing how using outdated software can expose serious vulnerabilities. 

The demo is supposed to be realistic, but not 100% real. There are some programming choices during the demo that are questionable to say the least, but they are there just for bringing forward discussion points. 

## Preparation
To run this presentation, you will need:
- Docker installed on your machine
- A Snyk account (see [here](https://appsec.equinor.com/snyk/))
- An _Organization_ in Snyk (see [here](https://appsec.equinor.com/snyk/))
  - If time is short, it's better to import this repository in Snyk before the demo
- The Snyk Code extension installed in your IDE

To reduce the risk of being blocked by a firewall or hitting other security measures, both the developer and the attacker machines are simulated using Docker containers, running locally.
Build the docker containers using the `docker-build.sh` scripts (it could take some time). The `docker-run.sh` scripts launch the containers with interactive shells.

The container for the development part already includes Python 3.4. `flask` and `pyyaml` need to be installed manually during the demo. The folder `sharedvolume` will be mounted in `/myapp` in the container. The app will be there.

The container for the attacking part is needed only when creating a listener for the reverse shell. The folder `sharedvolume` will be mounted in `/mystuff` in the container. That's where the script for starting the listener is.

IMPORTANT: make sure to disable the Snyk IDE extension (and possibly other security tools) before starting, otherwise the vulnerability will be revealed right away!


## Running the demo
A presentation to drive the discussion can be found in the `presentation` folder, in both PowerPoint and PDF format. 

### Demo #1 - The Developer
The presentation tells the story of a developer who is asked to implement a simple web application. The application must interact with a legacy piece of software. Open-source libraries can be used, but only outdated versions are compatible with the legacy system. By using outdated libraries, the developer ends up exposing the system to a Remote Code Execution vulnerability.

When hitting the _DEMO #1_ slide, follow these instructions

NOTE: files and folders mentioned in this part are in the `developer_area` folder

1. [optional] Ask some Generative AI system to produce the code for you. If you decide to do this, make sure the produced code uses the vulnerable `yaml.load()` function, and not `yaml.safe_load()` (which would defy the purpose of this demo). I have tested this with Equinor's own chat-bot using this pair of prompts:
  - *Hi, I need to create a simple web application using Python 3.4. It must provide a webpage with a form for entering text. When the form is submitted, the backend must take the text, do stuff with it (to be defined) and return it*
  - *What library can I use to process YAML strings?*
2. Show and go through the code in `app.py` using your favorite IDE
3. Run the docker container for the developer
  - `cd myapp/app`
  - `python app.py` -> error, libraries are missing
  - `pip install flask` 
  - `pip install pyyaml` -> error, Python 3.4 is not supported
4. Investigate the error message and point out that `pip` is trying to install PyYaml version 5.x.y
  - Open a browser to [pypi.org](https://www.pypi.org) and look for `pyyaml`
  - Go through the release history, looking for a version older that 5.x
  - All the versions 4.x are pre-releases, so pick the most recent stable version before 4.x, which is 3.13
  - `pip install pyyaml==3.13`
5. Open the browser at `0.0.0.0:9999` and paste in various examples from the file `yaml_examples.txt`. Everything should work as expected
6. Continue with the presentation

### Demo #2 - The Attacker
So What happened? It turns out PyYaml has a feature for creating objects on the fly while deserializing YAML code. This feature can be used to instantiate objects of the `subprocess.Popen` class, which runs shell commands depending on the input string.

NOTE: files and folders mentioned in this part are in the `attacker_area` folder
1. Show the basic examples from the `yaml_attacks.txt` file
  - start with the "hello world" example. As an attacker, you get no feedback, but the rest of the YAML code is interpreted correctly, so you suspect your code might have been executed. Indeed, if you look at the developer shell,   "Hello World!" is printed on the screen
  - try out a different command, like `env`. Again, it seems to work
2. Time to step up, let's see if we can reach the internet from that machine
  - Open a browser to [webhooks.site](https://webhook.site/)
  - Copy the URL of your webhook into the "webhook" attack string in `yaml_attacks.txt`
  - Attack the web application with that string, and show that your webhook has been hit
  - NOTE: [webhooks.site](https://webhook.site/) might be blocked by company firewalls. And calling the webhook might be blocked by the company firewall as well. If this happens, just move on to the next attack.
3. Now the attacker knows it is possible to run commands and that an internet connection is available. The next step is seting up a reverse shell.
  - Start the attacker container, and in there, start the `/mystuff/wait_for_shell.sh` script (or type it manually, it's just `nv -lvnp 10000`)
  - Check your machine IP address and paste it in the "revshell" attack string in `yaml_attacks.txt`
  - Attack the web application with that string. If you now go back to the attacker container, you should be able to send commands directly into the developer machine
  - Poke around: you can find interesting data using `env` and by looking into the `/confidential` folder. Run a `wget www.google.com` to show you can download stuff from the internet, including malwares
  - [optional] Point out that, while the attack string looks complex, it was not written manually. Go to [revshells.com](https://revshells.com) and show that shell commands are readily available.
  - NOTE: [revshells.com](https://revshells.com) might be blocked by company firewalls.
4. Continue with the presentaton

### Demo #3 - The Hardening

In Equinor, we use Snyk to protect ourselves from these situations. Whenever we start developing a new piece of software, the first thing to do is setting up dependency scanning in Snyk:
1. Monitor the repository via the Snyk web interface
  - Go to [app.snyk.io](https://app.snyk.io) and log in
  - Select your Organization, import this repository, and wait until the import completes
  - Highlight that there is a critical RCE vulnerability in the adopted version of PyYaml
2. Enable the Snyk Code extension in your IDE, and show that the vulnerability is highlighted right away
3. Look into option for fixing the vulnerability
  - PyYaml 4.1b has a fix for this. If you have strict requirements on versions, it may be better to use a beta version rather than a vulnerable one. Maybe
  - Another option is to sanitize the input before deserializing it. For instance look for `!!` in the input string, and if it's found just return nothing
  - If you dig a bit further on the web, you can quickly realize that the solution to all of these problems is to use `yaml.safe_load()`
4. Continue with the presentation until the end

## Disclaimers
- `Python 3.4` has reached end-of-life, and as such it is not allowed in Equinor. If you ever find yourself in a situation like this, the first step would be to contact the Chief Engineer IT
- The code in this repository is BAD, in part for the sake of the demo, in part to keep the demo simple and focused on the RCE vulnerability

# Contributing
Contributions are always welcome! If you find a bug, or you have questions, comments, suggestions, feel free to open an issue.

Pull Requests are also accepted, but we require signed commits. PRs will be reviewed by an admin and merged only after approval.
