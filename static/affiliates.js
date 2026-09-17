/*
  AFFILIATE PRODUCTS: sirf ye file badlo.

  Har product ke liye:
    url    : aapka affiliate link (https:// se shuru). KHALI ho to product nahi dikhega.
    title  : teeno bhasha me naam
    price  : dikhane wali keemat (optional, jaise "₹499 se")
    store  : "Amazon", "Flipkart", "Meesho" wagairah
    image  : optional. Sirf wahi image link daalo jiski store permission deta ho
             (jaise Amazon SiteStripe ka image link). Khali chhod sakte ho.
    pages  : kin pages par dikhe:
             "home", "navratri", "navratri-day", "recipes", "garba",
             "birthday", "anniversary", "wedding", "engagement", "good-morning"

  Naya product jodna: neeche kisi bhi { ... }, block ko copy karke paste karo,
  aur url, title, pages badal do. Har block ke baad comma (,) zaroori hai.
  Product hatana: uska url "" (khali) kar do, ya pura block delete kar do.
*/
window.AFFILIATES = {
  maxPerSlot: 4,
  products: [
    {
      url: "",
      title: { hi: "गरबा के लिए चनिया-चोली", gu: "ગરબા માટે ચણિયા-ચોળી", en: "Chaniya choli for Garba" },
      price: "", store: "Amazon", image: "",
      pages: ["navratri", "navratri-day", "garba"]
    },
    {
      url: "",
      title: { hi: "रंगीन डांडिया स्टिक", gu: "રંગબેરંગી દાંડિયા", en: "Decorated dandiya sticks" },
      price: "", store: "Amazon", image: "",
      pages: ["navratri", "garba"]
    },
    {
      url: "",
      title: { hi: "पूजा थाली सेट", gu: "પૂજા થાળી સેટ", en: "Puja thali set" },
      price: "", store: "Amazon", image: "",
      pages: ["navratri", "navratri-day", "home"]
    },
    {
      url: "",
      title: { hi: "व्रत का सामान: मखाने और सूखे मेवे", gu: "ફરાળી સામાન: મખાણા અને સૂકો મેવો", en: "Fasting essentials: makhana and dry fruits" },
      price: "", store: "Amazon", image: "",
      pages: ["recipes", "navratri-day"]
    },
    {
      url: "",
      title: { hi: "मिट्टी के दीये", gu: "માટીના દીવા", en: "Clay diyas" },
      price: "", store: "Amazon", image: "",
      pages: ["home", "navratri"]
    },
    {
      url: "",
      title: { hi: "बर्थडे डेकोरेशन किट", gu: "બર્થડે ડેકોરેશન કિટ", en: "Birthday decoration kit" },
      price: "", store: "Amazon", image: "",
      pages: ["birthday"]
    },
    {
      url: "",
      title: { hi: "कपल के लिए गिफ़्ट", gu: "કપલ માટે ગિફ્ટ", en: "Gifts for couples" },
      price: "", store: "Amazon", image: "",
      pages: ["anniversary", "wedding", "engagement"]
    },
    {
      url: "",
      title: { hi: "चाय-कॉफ़ी मग", gu: "ચા-કોફી મગ", en: "Tea and coffee mugs" },
      price: "", store: "Amazon", image: "",
      pages: ["good-morning"]
    }
  ]
};
