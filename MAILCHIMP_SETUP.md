# Mailchimp Integration Setup

## Step 1: Get Mailchimp API Key

1. Go to https://mailchimp.com/ and log in
2. Click your profile icon → Account & Billing
3. Click "Extras" → "API keys"
4. Click "Create A Key"
5. Copy the API key

## Step 2: Get Server Prefix

Your server prefix is in your Mailchimp URL.
Example: If your URL is `https://us21.admin.mailchimp.com/`, your prefix is `us21`

## Step 3: Get Audience ID

1. In Mailchimp, go to "Audience" → "All contacts"
2. Click "Settings" → "Audience name and defaults"
3. Look for "Audience ID" (looks like: a1b2c3d4e5)
4. Copy the Audience ID

## Step 4: Update .env File

Open `.env` file and replace:

```
MAILCHIMP_API_KEY=paste_your_api_key_here
MAILCHIMP_SERVER_PREFIX=us21
MAILCHIMP_AUDIENCE_ID=paste_your_audience_id_here
```

## Step 5: Restart Server

```
node server.js
```

## How It Works

- When someone subscribes via your website footer
- They're added to your local database
- They're automatically synced to your Mailchimp audience
- You can manage and send campaigns from Mailchimp dashboard

## Testing

1. Subscribe via website footer
2. Check Mailchimp dashboard → Audience → All contacts
3. New subscriber should appear there
