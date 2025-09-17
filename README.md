# Ubuntu-Inspired Image Fetcher 📸

*A Python script that embodies the Ubuntu philosophy: "I am because we are"*

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP8-brightgreen)](https://www.python.org/dev/peps/pep-0008/)

## 🌍 Overview

This project is a Python script that connects to the global community of the internet, respectfully fetches shared image resources, and organizes them for later appreciation. It embodies the Ubuntu philosophy of community, respect, sharing, and practicality.

## ✨ Features

- **Multiple URL Support**: Process multiple image URLs in a single session
- **Security Precautions**: Validates URLs and checks for dangerous file types
- **Duplicate Prevention**: Uses content hashing to avoid downloading identical images
- **HTTP Header Verification**: Checks headers for safety and content information
- **Graceful Error Handling**: Respectful error messages that don't crash the program
- **Organized Storage**: Automatically creates a dedicated folder for downloaded images
- **User-Friendly Interface**: Clear progress indicators and summary reports

## 📦 Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/ubuntu-image-fetcher.git
cd ubuntu-image-fetcher
```

2. Ensure you have Python 3.6+ installed

3. Install the required dependencies:
```bash
pip install requests
```

## 🚀 Usage

Run the script from your terminal:

```bash
python ubuntu_image_fetcher.py
```

You'll be prompted to enter image URLs. You can:
- Enter multiple URLs separated by commas
- Enter URLs on separate lines
- Type "done" when you've finished entering URLs

The script will:
1. Validate each URL
2. Check for potential security issues
3. Verify HTTP headers
4. Download images to a "Fetched_Images" directory
5. Skip duplicates based on content hashing
6. Provide a summary of successful downloads

## 🛡️ Security Features

- URL format validation
- Dangerous file type detection (.exe, .bat, .js, etc.)
- Content-Type verification to ensure only images are downloaded
- File size limits (20MB maximum)
- Safe filename sanitization
- HTTP header analysis for security indicators

## 📁 Project Structure

```
ubuntu-image-fetcher/
├── ubuntu_image_fetcher.py  # Main script
├── README.md                # This file
├── Fetched_Images/          # Created automatically (ignored in git)
│   └── downloaded_images    # Your collected images
└── .gitignore              # Git ignore file
```

## 🧩 Code Philosophy

The script implements four key Ubuntu principles:

1. **Community**: Connecting to the global web community to share resources
2. **Respect**: Handling errors gracefully and respecting web protocols
3. **Sharing**: Organizing fetched images for later sharing and appreciation
4. **Practicality**: Creating a tool that serves a real need for digital preservation

## 🤝 Contributing

We welcome contributions that align with the Ubuntu philosophy! Please feel free to:

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Inspired by the Ubuntu philosophy: "I am because we are"

Built with the [Requests](https://docs.python-requests.org/) library for respectful HTTP communication

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section below
2. Open an issue on GitHub
3. Consider how the Ubuntu philosophy might guide a solution

## 🔍 Troubleshooting

**Common issues:**

1. **SSL errors**: Ensure your Python installation has updated certificates
2. **Permission errors**: Check that you have write permissions in the current directory
3. **Network issues**: Verify your internet connection and firewall settings
4. **Large files**: The script limits downloads to 20MB for safety

**Q: The script won't download an image from a site I know has images**
A: Some sites require specific headers or user-agents. The script respects proper web protocols and may not work with sites that have restrictive access policies.

**Q: Why does the script skip some URLs?**
A: The script performs safety checks and will skip URLs that appear dangerous, point to non-image content, or exceed size limits.

---

*In the spirit of Ubuntu: "I am because we are"*