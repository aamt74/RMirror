<p align="center">
    <img src="images/logo.png">
</p>

<h6 align="center">
    Export all your reMarkable notes to your PC as PDF
</h6>

<h1></h1>

### TOC

- [Description](#description)
    - [Why](#why)
- [Showcase](#showcase)
- [Installation](#compile)
- [Usage](#usage)
- [Contributing](#Contributing)

### Description

RMirror is a Python tool that allows you to export all files from your reMarkable device to your PC in PDF format, maintaining the original folder structure.

### Showcase
<p align="center">
  <img src="images/showcase.gif"/>
</p>

### Installation

1. **Clone the repository**  
   Clone the repository using the following command:  
   ```bash
   git clone https://github.com/rdWei/RMirror
   cd RMirror
   ```
2. Install dependencies
    Ensure Python is installed, then install the required modules with:
    ```pip install -r requirements.txt```
3. Edit the `settings.py` file 
    Open the settings.py file in your favorite text editor and set the password field to your Remarkable password.
    Example:
    ```
    PASSWORD = "9Vlops9T2"
    ```

### Usage
1. **Connect your Remarkable to the computer**  
   - Plug your Remarkable tablet into your computer using a USB cable.  
   - Make sure the **Trash** on the Remarkable is empty.  
   - Enable the **USB web interface** option in `Settings > Storage` on your Remarkable.
2. **Run the script**  
   Execute the following command, replacing `rm_file_destination` with the desired destination path:  
   ```bash
   python3 rmirror.py rm_file_destination
    ```
## Contributing
If you'd like to contribute, you can submit a [pull request](https://github.com/rdWei/RMirror/pulls) with your changes or open an [issue](https://github.com/rdWei/RMirror/issues) to report any problems or feature requests.


