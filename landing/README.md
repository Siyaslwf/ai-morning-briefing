# Landing Page

Static, zero-dependency landing page. Deploy in 60 seconds.

## Deploy to Vercel (free, takes 2 minutes)

1. Go to [vercel.com/new](https://vercel.com/new) and sign in with GitHub
2. Import the `ai-morning-briefing` repo
3. **Root directory:** `landing`
4. **Framework preset:** Other
5. Click **Deploy**

Your site goes live at `https://ai-morning-briefing-<hash>.vercel.app` in ~30 seconds.

## Add your custom domain (optional, $10/year)

1. In Vercel project → **Settings** → **Domains**
2. Add your domain (e.g. `morningstack.ai`)
3. Vercel shows you 2 DNS records — paste them into Namecheap → Advanced DNS
4. Wait 5 minutes, you're live on your custom domain with auto HTTPS

## Before going live — replace these placeholders

Open `index.html` and search for `REPLACE_WITH_`:

| Placeholder | Replace with |
|-------------|-------------|
| `REPLACE_WITH_BEEHIIV_SUBSCRIBE_URL` | Your Beehiiv subscribe form action URL (in Beehiiv → Settings → Embed forms) |
| `REPLACE_WITH_STRIPE_LINK_PRO` | A Stripe Payment Link for the $5/mo tier (stripe.com → Payment Links → New) |
| `REPLACE_WITH_STRIPE_LINK_TEAM` | A Stripe Payment Link for the $15/mo tier |
| `hello@morningstack.ai` | Your real contact email |
| `The Morning Stack` (logo + footer) | Your chosen newsletter name |

That's it — no build step, no framework, no JavaScript runtime. Pure HTML/CSS.
