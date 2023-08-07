# SmashMentor
## The all in one place to practice!

**IMPORTANT: This project is still in development. It was uploaded as a baseline for future, more complete releases and only provides the most basic of functionalities right now. I hope to make installation more user-friendly in the future and maybe even host it on a public server**

### Installation
**You need to have the following on your system:**
- Python 3.6 or higher
- Python PIP (python package manager)

**Steps**
1. Download the files using an external tool like [DownGit](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/), or cloning the repository with git command from your command line/terminal
2. Install the necessary dependencies
```sh
pip install -r requirements.txt
```
3. Run the web server
```sh
uvicorn main:app 
```
Run using a different port (example using port 5000 below)
```sh
uvicorn main:app --port 5000
```
4. Open a new tab in your web browser and enter the following address
http://localhost:[port]/
(Replace [port] with the port you're using, default is 8000 if you didn't use --port flag)
5. When you're done using, stop the server from the command line with Ctrl+C 

**Note: it is recommended to run the server within a virtual environment if you don't want to affect your system's python installation. For this, you can read guides such as [this one](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)**

