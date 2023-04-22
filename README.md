# Auto-GPT MetaTrader Plugin 📈
The AutoGPT MetaTrader Plugin is a software tool that enables traders to connect their MetaTrader 4 or 5 trading platform to Auto-GPT.

[![GitHub Repo stars](https://img.shields.io/github/stars/isaiahbjork/Auto-GPT-MetaTrader-Plugin?style=social)](https://github.com/isaiahbjork/Auto-GPT-MetaTrader-Plugin/stargazers)


## 💡 Key Features:
- 💰 **Place Trades**: .


## 🔧 Installation

Follow these steps to configure the Auto-GPT MetaTrader Plugin:

### 1. Clone the Auto-GPT-MetaTrader-Plugin repository
Clone this repository and navigate to the `Auto-GPT-MetaTrader-Plugin` folder in your terminal:

```bash
git clone https://github.com/riensen/Auto-GPT-MetaTrader-Plugin.git
```

### 2. Install required dependencies
Execute the following command to install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 3. Package the plugin as a Zip file
Compress the `Auto-GPT-MetaTrader-Plugin` folder or [download the repository as a zip file](https://github.com/isaiahbjork/Auto-GPT-MetaTrader-Plugin/archive/refs/heads/master.zip).

### 4. Install Auto-GPT
If you haven't already, clone the [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT) repository, follow its installation instructions, and navigate to the `Auto-GPT` folder.

### 5. Copy the Zip file into the Auto-GPT Plugin folder
Transfer the zip file from step 3 into the `plugins` subfolder within the `Auto-GPT` repo.

### 6. Locate the `.env.template` file
Find the file named `.env.template` in the main `/Auto-GPT` folder.

### 7. Create and rename a copy of the file
Duplicate the `.env.template` file and rename the copy to `.env` inside the `/Auto-GPT` folder.

### 8. Edit the `.env` file
Open the `.env` file in a text editor. Note: Files starting with a dot might be hidden by your operating system.

### 9. Add email configuration settings
Append the following configuration settings to the end of the file:

```ini
################################################################################
### METATRADER
################################################################################
META_API_ACCOUNT_ID=
META_API_TOKEN=
```

- Set `META_API_ACCOUNT_ID` to your [MetaAPI](https://metaapi.cloud) account ID. 
- Set `META_API_TOKEN` to your MetaAPI token.

- Create

### 10. Allowlist Plugin
In your `.env` search for `ALLOWLISTED_PLUGINS` and add this Plugin:

```ini
################################################################################
### ALLOWLISTED PLUGINS
################################################################################
#ALLOWLISTED_PLUGINS - Sets the listed plugins that are allowed (Example: plugin1,plugin2,plugin3)
ALLOWLISTED_PLUGINS=AutoGPTMetaTraderPlugin
```

## 🧪 Test the Auto-GPT MetaTrader Plugin

Experience the plugin's capabilities by testing it for placing trades, managing your account, closing trades, and fetching candlestick data.

###  Test Fetching Candlestick Data

1. **Configure Auto-GPT:**
   Set up Auto-GPT with the following parameters:
   - Name: `TradeGPT`
   - Role: `fetch candlestick data`
   - Goals:
     1. Goal 1: `fetch candlestick data for the 1 hour chart on EURUSD`
     2. Goal 2: `Terminate`

2. **Run Auto-GPT:**
   Launch Auto-GPT, which should use the email plugin to send an email to my-email-plugin-test@trash-mail.com.


3. **Sample response content:**
   

