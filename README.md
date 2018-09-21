# Hardcore WebScraping

Hardcore solution for when there are too many protections against web scraping

## Context

I am currently working in a part of France where there is not much to do... So I come back to Paris (my home city) every single week end I can. But I have a few issues with this journey: 
* There is a train station, but the tickets are very expensive
* There is no cheaper way to go from my working city to my home city (plane, car, ...)
* I want to take my ticket as close to the departure time as possible (because I want my come back to correlate with local events)
* Lot of people are taking the exact same train with the same problems (Friday around 5:30pm) which means prices vary a lot during the weeks before

## My projet

I decided to do some Data Analysis (for fun and profit) on the variations of the prices on my trajects. The context I have for this project will help me to have a very clear view on the datas. Indeed, the following conditions help me focus on a small part of the total datas available:
* My internship stop in February (I am only interested in datas between now and February)
* The SNCF (french train company) only provides 12 weeks of datas in advance
* This is always the same traject:
  * Friday around 5:30pm work -> home
  * Sunday around 6pm home -> work
 
## Web Scraping: The Big Problem

As you can guess this project is not going to be that easy. Otherwise I would not have called it "Hardcore" but simply Web Scraping and would have made the same thing as 100.000 of other people on the internet.

### Problem 
The problem is that the train companies do not want you to do this. They want to avoid Web Scraping as much as possible, for economic purposes I believe. 

### What Failed

#### API
The SNCF provides a very cool and simple to work with API, but it does not provide any informations on the prices of the trajects... If they try to hide this information for economic reasons it make sense, but it is realy a shame for me.

#### HTTP Request
As I am familiar with Web Scraping I began trying usual technics to get the informations I need sending simple HTTP requests and waiting for the responses. But with no surprise I could not get access to the data by any mean... I could get the webpage but no information was displayed on it. Surprisingly, this is the same for the "view sourcecode" mode, I do not have access to the data displayed on screen int it (weird).

### Other WebSites
I found other websites wich gather the same informations that I need such as the [the train line](https://www.thetrainline.com/). But their Business is to sell you a service on these data on which they have some sort of exclusivity. So as you can imagine, this is very important for them to secure there datas as much as possible and not to be very open with the sharing of these datas.

### What Worked (Hardcore)

I did not stop here, because I really need this informations to save some money. The solution I tried is to simulate a user. There are some cool python libraries called win32api which allows you to do all sort of interesting things for this project. You can simmulate any kind of user interaction with code.
- clicks
- scroll
- CTRL + A
- CTRL + C

Thats all I needed to make this project work. 
