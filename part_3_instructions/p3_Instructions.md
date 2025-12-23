# Part 3, Big girl coding: collecting historical Japanese book metadata from the National Diet Library

### What you will learn

By the end of this exercise, you should be able to:

- Recognise when a website exposes **structured data**
- Locate and read **API documentation**
- Send HTTP requests to an API
- Inspect and understand **XML responses**
- Extract structured data from XML using Python
- Store results in a **pandas DataFrame**
- Drink water upside down
- Juggle hamsters    

This is real data used by real researchers. The documentation is real, and not always perfect. You will also be doing all of this in a real [IDE](https://en.wikipedia.org/wiki/Integrated_development_environment): [Pycharm Pro](https://www.jetbrains.com/pycharm/).

---

## Part 1 — Discovering useful data

<span style="color: grey">(5 min - quick website tour)</span> <span style="color: red">Move quickly</span>

1. Go to the **National Diet Library Search** website: [https://ndlsearch.ndl.go.jp/](https://ndlsearch.ndl.go.jp/)  
2. Search for something related to **old Japanese books**.
3. Click on a result and open the **detailed view (詳細)**.

### Questions to think about

- What information is shown for each book?
- Do you see:
    - a title in kanji?
    - a reading (ヨミ)?
    - an author with the same shit?
- Does this look like data that you could use?
- Does it look *precious*? How do *you look* right now? Like this?

![](../data/precious.png)
**Fig 1** Marina looking at NDL metadata

---

## Part 2 — Finding the API

<span style="color: grey">(10 min - find docs, identify SRU)</span> <span style="color: red">Move quickly</span>

Many large libraries expose their data through **APIs**.

1. Search online for:  **“NDL Search API”**
2. Find the official documentation page on the NDL website.
3. You should find references to:
    - OpenSearch
    - SRU
    - OAI-PMH

**Be warned**, there is a **major inconvenience with the NDL website**: it's all in some sort of nonsense language where they took beautiful Chinese and stuffed scribbles and stuff in between the characters. Why would someone do this? It made me very dizzy, but I think I found the following pages of interest:

- [API提供対象データプロバイダ一覧](https://ndlsearch.ndl.go.jp/help/api/provider)
- [API仕様の概要](https://ndlsearch.ndl.go.jp/help/api/specifications)
- [APIのご利用について](https://ndlsearch.ndl.go.jp/help/api)
 
### Questions

- Which one looks the most technical?    
- Which one looks designed for machine access?
- Which one returns **XML**?

You will work with **SRU**.

---

## Part 3 — Understanding SRU at a high level

<span style="color: grey">(5 min - high-level overview)</span> <span style="color: red">Move quickly</span>

SRU stands for **Search/Retrieve via URL**.

An SRU request is:

- a URL    
- with parameters
- that returns XML records

Look for:

- the **base URL**
- example queries
- a list of **searchable fields**

You do not need to understand everything yet.

---

## Part 4 — Making your first SRU request

<span style="color: grey">(5 min - show URL, get XML)</span> <span style="color: red">Move quickly</span>

Use a browser first.

Start with a **very simple query** that searches for Japanese-language material by title.

You should receive:

- a `<searchRetrieveResponse>` element
- a `<numberOfRecords>`
- one or more `<record>` elements

After some fiddling, Daniel got the following to work. In short, I looked for 'old materials' produced prior to 1867, 20 records at a time:

```
https://ndlsearch.ndl.go.jp/api/sru?operation=searchRetrieve&version=1.2&query=mediatype%3Doldmaterials%20AND%20until%3D%221867%22&maximumRecords=20&recordSchema=dcndl
```

The first thing you should read is:

> This XML file does not appear to have any style information associated with it. The document tree is shown below.

That's right: it's a whole new coding language. There's no **style**, but hey, the two of us got plenty of that 😉

---

## Part 5 — Inspecting the XML

<span style="color: grey">(15 min - explain tags, nesting, attributes)</span>

XML is designed to be machine readable. As to whether it is *Marina readable*, that is another story. It helps to 'prettify it', like I've done for one record in [sample_record.xml](sample_record.xml), which you can open in your browser.

XML is comprised of nested **tags**. Let's consider a simple example:

```xml
<root>
	Look, there is <japanologist>Marina</japanologist>.
	<page n="1"/>
</root>
```

As to the tags:
- `<japanologist>` is an **opening tag**, and `</japanologist>` is a **closing tag**, identifying the text therein as that thing.
	- That is to say that this node possess the **text** 'Marina'.
- The `/` in `<page n="1"/>` closes the tag, so this tag is self-contained.
- The `n="1"` in `<page n="1"/>` is an **attribute**. We can use attributes to store structured data within tags.
- Both the `<japanologist>` and `<page>` tags are **nested** within `<root>`. In other words, `<root>` is their **parent**, they are **children** of `<root>`, and the two are **siblings**.
- 'Tag' refers to the labelling process. In terms of reading, we call the `<japanologist>` here an **'element'** or a **'node'**.

Why bother with all this shit? Because this is a way that people and machines use to structure data, it is quick and easy to navigate, and data is *precious*... 

### Questions

Take another look at the 'prettified' NDL entry and ask yourself:

- What data can we use for the IME?
- In what tag is it contained?
- What is the parent-child-sibling relationship between interrelated data?

You do not need to fully understand [namespaces](https://en.wikipedia.org/wiki/XML_namespace) yet.

---

## Part 6 — Parsing XML in Python

<span style="color: grey">(45-60 min - CORE LEARNING)</span>

OK, [time to but your big girl pants on](https://dictionary.cambridge.org/dictionary/english/put-big-girl-pants-on), because now you're going to code by yourself in an IDE. 

### Setup 

- Open the `codeclass` folder as a project in Pycharm
- Create a new file, name it something + `.py` 
- Under `file > settings > Python` create a virtual environment (or 'venv'; see [instructions](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)).
- Now, you need to install some python packages. You can do that with the `+` right below where you set up the venv. This is what you need:
	- beautifulsoup4 
	- lxml 
	- numpy
	- pandas

### Starter idea

Go to [Brave Search](https://search.brave.com) and look up 'how to navigate xml in python'. All the answers will be about the lxml package, which is awesome. However, you should start with something a little simpler, so look up 'how to navigate xml in python with beautifulsoup'. You can look at [the project's documentation](https://beautiful-soup-4.readthedocs.io/en/latest/), but that will be long and filled with info you don't really need at this point, so you should click on something like [the geeksforgeeks.org page](https://www.geeksforgeeks.org/python/parsing-tables-and-xml-with-beautifulsoup/). 

Yup, that looks good, so copy the code from the XML bit. You do of course need to change one thing: you need to give it the correct path to your own XML file, which will probably be `/part_3_instructions/sru_first_20.xml` or `../part_3_instructions/sru_first_20.xml`.

Their code won't work, of course, because it is looking for shit in their practice file:

```python
# This creates a list of <title> nodes
titles = soup.find_all('title')

# This iterrates through that list
for data in titles:
    # This retrieves and prints the text belonging to the current <title> node
    print(data.get_text())
```

What you want is probably two things. First, the `<foaf:Agent>` node identifies an author, and within it is `<foaf:Agent>`, which gives the kanji, and `<<dcndl:transcription>`, which gives the kana:

```xml
<foaf:Agent rdf:about="http://id.ndl.go.jp/auth/entity/00380913"> 
	<foaf:name>鳥居, 清経</foaf:name> 
	<dcndl:transcription>トリイ, キヨツネ</dcndl:transcription>
</foaf:Agent>
```

Next is the book title:

```xml
<dc:title>
	<rdf:Description> 
		<rdf:value>嗚呼勇四人与市 3巻</rdf:value> 
		<dcndl:transcription>アア イサマシ ヨニン ヨイチ</dcndl:transcription> 
	</rdf:Description>
</dc:title> 
```

In other terms,

- You want two for loops, one for authors, one for titles
- For the author for loop, you want to look up each `<foaf:Agent>`
	- Then, for each `<foaf:Agent>`, you want to use the .find() method to find the first `<foaf:name>` and `<dcndl:transcription>`
	- for each of those, you want to .get_text()
	- you should put that in a dictionary, like `{'kanji': a, 'kana': b, 'type': 'author'}`
	- you should add that dictionary to a list
- Do the same for titles, except remember that you also need to loop through the `<rdf:Description>` in the middle.

You can get through this slowly by trying, printing each step up to where something fails, etc. This sort of trial and error is how we learn. If you are in a hurry, however, **this is where you might finally ask an AI to write something for you**.

Do **not** worry if some fields are missing.

---

## Part 7 — From records to a DataFrame

<span style="color: grey">(10 min - quick conversion)</span>

Create a list of dictionaries, then convert it into a pandas DataFrame. Do the typical stuff to evaluate its contents, size, etc.

---

## Part 8 — Scaling up (harvesting)

<span style="color: red">SKIP or do very quickly (5 min mention)</span>

SRU supports:
- `startRecord`
- `maximumRecords`
- total record counts

What that means, is that you can put the *search string* in a `for` or `while` loop, changing the `startRecord` number in each loop. Then, you modify the python code you wrote to open the sample file to instead read the XML retrieved at each search and put that in the for loop.... Then, you can hit 'go' and get *millions* of records while you have a nice long dinner with your mum.

This is just for practice, so be modest, polite, and discrete:
- do not request thousands of records at once
- add a short delay if needed
- see if you can't find a way to pass your requests through TOR.

We'll look together at a sample of this data and think about its use for marinaMoji. If, then, we decide that the NDL is useful, we will file a request with them, then you will mine the whole fucking thing empty.

🦄 WAAAAAAAAAAAAAAAAGH !

---

## Part 9 — Reflection

<span style="color: red">SKIP</span>

Do you think this is cool, Marina? Are you thoroughly impressed by all that you have learned to do? Do you feel powerful? Are you ready to *conquer*? Is this *metal enough* for you? 

Pat yourself on the back, put the baby toys away, and open part 4. 

