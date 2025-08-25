# DisStored - Discord Webhook File Storage

A (eventually) standalone executable application that uses Discord webhooks for file storage, just like [Disbox](https://disboxapp.github.io/web/home) Uses the browser to control and upload, rather than CLI or Tkinter.

## Features
- **Web Interface** - Stunning and responsive web UI that you can customize the address and port.
- **Folder Support** - Organize your uploads in folders.
- **Discord Intregration** - Seems obvious, and admittedly is, but still. Uses chunking to upload files >10mb.
- **Drag N' Drop** - Easy as that, or you can click on the box appropriately titled to open Explorer as well.
- **Minimal Local Usage** - Stores the files on Discord's Servers, the only storage you'll be using is the repo, and the files.json that will be *the* largest file.
- **Secure** - I will never be able to gain access to the files hosted, nor will anyone else that isn't on your LAN (besides discord themselves but yk, unless they repack the chunks, it wouldn't matter).

## Quick Start

## 1. Download and Run

1. Clone or download the repo.
2. Set your Discord webhook URL as an evironment variable
   ```set DISCORD_WEBHOOK_URL=put_webhook_url```
3. Run the BAT file or run python directly (if you have .env set, or e-variable).
   ```py app.py```

### 2. Using the Web UI

- **Upload Files**: Drag and drop or click the upload area.
- **Create Folders**: Enter a folder name and click "Set Folder", it will add a new tab underneath the input text field with your folder.
- **Navigate**: The "Extra" button is just that, extra information / misc things that isn't really necessary, such as basic info, source code (which you're looking at), my social connections, and how to use it.

```To use DisStored, first you need to create a server.

   1: Make a server.

   2: Create a webhook by going into the settings and tapping on "Integrations" and creating one.

   3: Copy the webhook url and paste it into the webhook url field in the .env file, which config.py will then pick up and use.

   4: Start the server by running the run.bat file, using "python app.py", or other means of running the server.

   5: A browser tab will open automatically, hence what you're on right now.

   6: Upload files by dragging and dropping them into the upload area or clicking the upload area.

   7: If the uploaded files go above the 10mb standard Discord limit, the file will be broken down into pieces and sent into to the same channel, but still remain intact. You will then be able to download the file by clicking the "Download" button.
```

## How It Works

1. **File Upload**: When you upload a file, it's:
   - Stored locally in "files.json" (base64 encoded)
   - Uploaded to your Discord Webhook
   - *Organized by folders

2. **File Access**: Files can be:
   - Downloaded directly from the UI
   - Downloaded onto other devices, if connected to the same Wi-Fi
   - If small enough, directly downloadable from Discord

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify your Discord webhook URL is correct
3. Ensure you have proper permissions to write files

```If none of those work or you can't figure it out, DM the creator on Discord or Telegram (@hexxedspider on both)!```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.