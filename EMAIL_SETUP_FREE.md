# Free Email Options for Portfolio

## Option 1: SendGrid (FREE - 100 emails/day)
**Cost: $0/month**

1. Go to https://sendgrid.com/
2. Sign up (no credit card needed)
3. Verify email
4. Settings → Sender Authentication → Single Sender Verification
5. Add dengjohn200@gmail.com and verify
6. Settings → API Keys → Create API Key
7. Copy key to .env file

## Option 2: Formspree (FREE - 50 submissions/month)
**Cost: $0/month - No backend needed**

1. Go to https://formspree.io/
2. Sign up with dengjohn200@gmail.com
3. Create new form
4. Copy form ID (looks like: xpznabcd)
5. Replace form action in HTML:
   ```html
   <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
   ```

## Option 3: EmailJS (FREE - 200 emails/month)
**Cost: $0/month - Client-side only**

1. Go to https://www.emailjs.com/
2. Sign up
3. Add email service (Gmail)
4. Create email template
5. Get Public Key and Service ID
6. Add to your JavaScript

## Option 4: Web3Forms (FREE - Unlimited)
**Cost: $0/month - Simplest**

1. Go to https://web3forms.com/
2. Enter dengjohn200@gmail.com
3. Get Access Key
4. Add to form:
   ```html
   <input type="hidden" name="access_key" value="YOUR_ACCESS_KEY">
   <form action="https://api.web3forms.com/submit" method="POST">
   ```

## Recommendation:
Use **Web3Forms** - completely free, unlimited emails, no signup required.
