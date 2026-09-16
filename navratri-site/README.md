# Indian Festival Wishes: Navratri 2026 website

Is zip me 2 folder hain:

- **upload-to-github**: puri taiyaar website. Iske ANDAR ki saari files GitHub par upload karni hain.
- **source-code**: agar baad me content ya domain badalna ho to (Python chahiye). Chaho to mujhe (Claude ko) bata dena, main badal ke de dunga.

## Site me kya hai

- 3 bhasha: Hindi (`/`), Gujarati (`/gu/`), English (`/en/`). Upar right me bhasha badalne ka button hai.
- Har bhasha me: Home, Navratri ke 9 din ke alag page, Garba-Dandiya, Vrat ka khana, About, Contact, Privacy Policy, Disclaimer.
- Har din ke page par: Devi ki katha, puja vidhi, rang, bhog, mantra, 3 wishes (copy button ke saath).
- Naam wala card: user apna naam likhta hai, us din ka card banta hai. WhatsApp par link bhej sakta hai, photo download ya share kar sakta hai. Jisko link milta hai use bhejne wale ka naam card par dikhta hai.
- Home page par apne aap "Navratri shuru hone me X din" ya "Aaj din N hai" dikhta hai.
- Ads ke liye jagah pehle se bani hai (approval ke baad hi dikhegi).

## Step 1: Domain aur email

Domain `https://www.indianfestivalwishes.com` saari files me pehle se daal diya gaya hai.
Contact page par `contact@indianfestivalwishes.com` likha hai. Ye email chalu karne ke liye domain provider ki free email forwarding se ise apne Gmail par forward karo.

## Step 2: GitHub Pages par site chalu karo

1. github.com par account banao, **New repository** banao. Repository **Public** honi chahiye (free plan me Pages ke liye).
2. **Add file > Upload files** me `upload-to-github` ke ANDAR ki saari files aur folders (gu, en, static bhi) drag karke daalo. Folder khud (`upload-to-github`) mat daalna, uske andar ka saaman daalna.
3. **Settings > Pages** me jao. Source: **Deploy from a branch**, Branch: **main**, folder: **/(root)**. Save karo.
4. 1-2 minute baad site `https://USERNAME.github.io/REPO-NAME/` par khul jaayegi.

## Step 3: Apna domain jodo

1. **Settings > Pages > Custom domain** me `www.indianfestivalwishes.com` likh ke Save karo.
2. Jahan se domain liya (GoDaddy, Hostinger, Namecheap wagairah), wahan DNS settings me ye records daalo:

| Type | Name/Host | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | USERNAME.github.io |

3. DNS update hone me kuch minute se 24 ghante lag sakte hain. Uske baad Pages settings me **Enforce HTTPS** tick karo.

Ye IPs GitHub ke docs me diye hote hain. Lagane se pehle ek baar GitHub Pages ke "custom domain" docs me check kar lena.

## Step 4: Google me site daalo

1. Google Search Console (search.google.com/search-console) me domain add karke verify karo.
2. **Sitemaps** me `sitemap.xml` submit karo.

## Step 5: AdSense

1. Apply karne se pehle: domain chalu ho, HTTPS ho, aur saare pages khul rahe hon.
2. AdSense me site add karo. Verification ke liye jo `<script>` code mile, use `index.html` (aur chaho to `gu/index.html`, `en/index.html`) ke `<head>` me daal do. Ya **ads.txt** tareeka chuno.
3. **Approval ke baad:**
   - `static/config.js` kholo aur `adsenseClient: ""` me apni ID daalo, jaise `"ca-pub-1234567890123456"`. Isse saare pages par ads chalu ho jaayenge (Auto ads).
   - Agar AdSense me alag ad units banao, to unke slot ID `adSlots` me `top` aur `middle` me daalo.
   - `ads.txt` kholo, line ke aage se `#` hatao aur `pub-0000000000000000` ko apni pub ID se badlo.

## Zaroori baatein

- **Apne ads par khud click mat karna, na dosto se karwana.** Account ban ho jaata hai.
- **Tithi aur rang:** 11 October ko Ghatasthapana aur 20 October ko Dussehra zyadatar panchang me hai, lekin din ke rang alag-alag jagah alag diye jaate hain. Apne panchang se ek baar mila lena. Galti ho to mujhe batao, main badal dunga.
- **Traffic bahut badh jaaye:** GitHub Pages par har mahine lagbhag 100GB bandwidth ki soft limit hai aur ye mukhya roop se commercial kaam ke liye nahi bana. Site viral ho jaaye to wahi files Cloudflare Pages ya Netlify (dono ka free plan hai) par daal sakte ho, code me koi badlav nahi lagega.
- **Dussehra, Diwali, Uttarayan:** isi design me naye festival ke pages jud sakte hain. Isse site ka content badhta rehta hai, jo AdSense aur Google dono ke liye achha hai.
