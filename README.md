# Spotify Email Validation Script 📧

This Python script helps you verify the validity of email addresses by checking them against a specific endpoint. It uses proxies to handle requests and can process multiple emails concurrently for efficiency.

## Features 🚀

- **Extracts Emails:** Reads email addresses from a specified text file. 📄
- **Validates Emails:** Checks each email address to determine if it is already registered on a particular service. ✅
- **Proxies Support:** Uses a rotating list of proxies to make requests, helping to manage rate limits and avoid IP bans. 🌐
- **Concurrent Processing:** Utilizes multiple threads to speed up the email validation process. ⚡
- **Saves Results:** Outputs the valid email addresses to a specified file. 💾

## Prerequisites 🛠️

Ensure you have the following Python packages installed:

- `requests`: For making HTTP requests. 🌍
- `colorama`: For colored text output in the terminal. 🌈

You can install these packages using the following command:

```bash
pip install requests colorama
 
