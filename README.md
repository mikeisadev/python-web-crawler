# PYCrawl - Python Web Crawler
PYCrawl is a web crawler written in Python by Michele Mincone. 

With PYCrawl you can insert the URL of the website that you want to analyze and scan to get relevant information about that website.

This program can scan an entire page building a sitemap inside a Python dictionary to understand and analyze the structure of URLs and how internal and external linking is made.

You can save that data in a JSON file and for each URL additional data is obtained: source of images, links to javascript and css files and server response headers.

Much more data will be added in future versions of this program.

This software can be run inside VS Code with a Python installation (Python 3.12.0) or via the "py" command inside your OS terminal.

Several parameters can be set in both environments to configure how the web crawler should work.

# Getting started
Before using this web crawler you have to be sure that Python and all dependencies are installed on your computer.

This software was written in Python 3.12.0 and it is recommended to install this or latest version.

Then you have to install the following dependencies to make sure that the programm will run smoothly:

- pip install beautifulsoup4 questionary requests validators pydot

Shortly:
- `beautifulsoup4` is used to parse HTML pages
- `questionary` is used to make CLI interface with this program more user friendly and simple to use
- `requests` is used to make HTTP request with a wide range of options to set, like user agents and several other request HTTP headers
- `validators` to get access to a wide range of validators
- `pydot` to generate simple mindmaps

# How to use PYCrawl
To start using PYCrawl install Python on your machine and the above dependencies.

You have to download this program on your pc in a folder.

You can use `git clone` or the download button in this repository.

Then you can run this program on:
- Visual Studio Code running it via Python Debugger with the combination of CTRL + F5 buttons on your keyboard

- CLI (terminal) or command prompts on your OS inserting commands with arguments

Let's see each method together.

## Run this program via Visual Studio Code
After you downloaded this program on your computer open the folder on Visual Studio Code.

Open the file `crawler.py` and press the combination of buttons `CTRL + F5` to run the program with Python Debugger.

**NOTE:** *Make sure that Python and Python Debugger are installed as extensions on your Visual Studio Code IDE.*

After you pressed these buttons, the integrated terminal on VS Code will open. 

The program will ask you to insert the URL to be crawled, so insert this URL following this pattern:

`https://websitename.com` or `http://websitename.com`

Then press enter and you can decide wheter you want to reply to all questions to configure the web crawler.

If you reply `yes` different questions will be asked to you to configure the crawler, otherwise default settings will be used.

At the end of this process the web crawler will start doing its job.

Crawl results will be visible inside the `crawled` folder in this project. The domain name that you inserted will appear with all the crawling job that has been requested.

## Run this program via CLI / Terminal / command prompts
First download this program on your computer.

Then, to run this program via CLI or command prompts, you have to:

- Open your CLI (cmd or command prompts program) on your computer.
- Point the directory to the folder where you downloaded this program, use the `cd` (change directory) command to point to `pycrawler` folder.
- Then use the `py` command to run `crawler.py` file, the starter file of this web crawler
- At this point, insert the url of the website that you want to crawl: `https://websitename.com` or `http://websitename.com`
- The command should be `py crawler.py https://websitename.com`, that's okay but you have to configure parameters to give more instructions to the crawler, follow below

Base command: `py crawler.py https://websitename.com [...parameters]`

The placeholder `[...parameters]` could be one of the following strings in the table below:

| Command(s) | Description | Argument
| --- | --- | --- |
| `--save`, `-s` | Setting this command you'll tell to the crawler to save in HTML format each crawled web page inside "crawled/domain" folder.  | No argument required. |
| `--sitemap`, `--sm`  | This command will generate a sitemap of crawled URLs taking into count the depth of urls.  | No argument required. |
| `--json`, `-js`  | This command will save structured data in JSON format inside "crawled/domain" folder getting al crawling data.  | No argument required. |
| `--user-agent`, `-ua`  | With this command you can set up an user agent. | An user agent to set up. You can find many user agents inside the project folder `pycrawler/data/useragents.py`. You can choose between: moz5-winnt-10, moz5-winnt-61, moz5-mac, opera-38, opera-980, chrome-51, edge-91, safari-604 or any other user agent inside `pycrawler/data/useragents.py` file |
| `--all-headers`, `--res-headers`, `--req-headers`  | With this command you can decide which headers you want to save into the JSON structured data file. | No argument required. |
| `--save-dup-links`, `-sdl` | With this command you can decide if you want to save duplicate links found during the crawling process | No argument required. | 
| `--depth`, `--crawl-depth`, `-cd`  | Setting a number for this parameter, you can decide  the depth where the crawler must go through. If the crawl depth is over scale the program will raise an exception. In other words, if the inserted crawl depth is more than the real scanned depth on the site you'll get an error. | The argument is an `int` (integer)|

# Folder structure

# How it works