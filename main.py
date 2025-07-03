import os
import sys
import asyncio
import platform
import discord
import time
import getpass
import requests
import threading
import re
import random
import psutil
import time
import tasks
import aiohttp
import base64
import datetime
import subprocess
import json
import textwrap
import string
import math
from googletrans import Translator
from dotenv import load_dotenv
from googletrans import Translator, LANGUAGES
from colorama import Fore, init
from discord.ext import commands, tasks

load_dotenv()

conversation_flow = [
    ("Hey, what’s up?", "Not much, just contemplating the meaning of life... and snacks."),
    ("You ever think about how weird humans are?", "All the time! Like, why do we put round pizzas in square boxes?"),
    ("I just finished binge-watching a series.", "Which one? Let me guess, it’s about people making bad decisions?"),
    ("I tried cooking the other day.", "How’d that go? Did you end up with a Michelin star or just a smoke alarm?"),
    ("I really need to exercise.", "Same. My couch is starting to feel like my best friend."),
    ("What’s your favorite pizza topping?", "Pineapple. It’s the ultimate rebel topping!"),
    ("Do you believe in aliens?", "Of course! They probably look at us and think, ‘What are they doing?’"),
    ("Why do people always say ‘break a leg’?", "Because that’s how you get a standing ovation!"),
    ("I want to travel the world.", "Me too! But I also want to travel from my bed to the couch."),
    ("Why do we park in driveways and drive on parkways?", "Honestly, that’s the biggest mystery of our time."),
    ("I wish I could teleport.", "Right? Imagine skipping traffic and just appearing at the beach."),
    ("Ever notice how cats act like they own the place?", "Definitely! They’re like furry little dictators."),
    ("Why do we call it ‘rush hour’ when nothing moves?", "It’s basically a time for collective frustration."),
    ("I really need to stop procrastinating.", "Same. I’ve been meaning to do that since 2019."),
    ("What would you do with a million dollars?", "Probably buy a lifetime supply of tacos and regret nothing."),
    ("You got any hidden talents?", "I can eat an entire pizza by myself. Does that count?"),
    ("What’s your spirit animal?", "Definitely a sloth. I live life in the slow lane."),
    ("I love naps.", "Naps are like time travel, but with more drool."),
    ("What’s your favorite childhood memory?", "Sneaking cookies when my parents weren’t looking!"),
    ("Why do we even bother with alarm clocks?", "They’re just tiny robots whose sole purpose is to ruin our dreams."),
    ("I heard laughter is the best medicine.", "That explains why my doctor is a stand-up comedian."),
    ("What’s your go-to karaoke song?", "Anything that lets me scream my feelings out!"),
    ("You think social media is real?", "Of course! Just like unicorns and that guy who claims he can cook."),
    ("What’s your dream job?", "Professional ice cream taster. Who wouldn’t want that?"),
    ("I can’t believe it’s already November.", "I know, right? Time flies when you’re having fun—or when you’re lost on the internet."),
    ("Do you remember when we thought 2020 was going to be the best year ever?", "Yeah, I think we all need a refund for that one."),
    ("What’s your favorite way to waste time?", "Scrolling through memes. It’s basically an art form."),
    ("Why is it so hard to get out of bed?", "Because it’s the ultimate trap of comfort and denial."),
    ("What do you think about online dating?", "It’s like shopping for relationships. Returns not accepted."),
    ("What’s your favorite meme?", "Anything with dogs. They’re just so relatable!"),
    ("Why do I feel like adulting is a scam?", "Because it totally is! Where’s my magical money tree?"),
    ("You ever notice how coffee is just a hug in a mug?", "Absolutely! And without it, I’m basically a zombie."),
    ("What’s the most ridiculous thing you’ve ever done?", "Probably trying to be an adult. What was I thinking?"),
    ("You ever talk to yourself?", "Only when I need expert advice. Turns out I’m not very reliable."),
    ("Why do I feel like everyone on Instagram is a liar?", "Because they are! That’s not a ‘no filter’ face; that’s Photoshop."),
    ("What’s your guilty pleasure?", "Eating an entire pint of ice cream while crying. It’s therapeutic."),
    ("Do you think I could survive in the wild?", "Only if there are drive-thrus and Wi-Fi."),
    ("Why do we have to adult?", "Can’t we just be kids with credit cards?"),
    ("What’s your ideal way to die?", "Laughing while eating pizza. I want my last meal to be glorious."),
    ("Do you ever feel like life is just a video game?", "Totally! I’m just waiting for the cheat codes."),
    ("You think I could get famous on TikTok?", "Only if your life is a continuous fail compilation."),
    ("What’s the weirdest thing you’ve ever eaten?", "That questionable sushi from a gas station. Never again."),
    ("If you could be any fictional character, who would you be?", "Probably the one with the least responsibilities. Hello, Patrick Star!"),
    ("Do you think pets judge us?", "Of course! They’re just better at hiding their judgment."),
    ("What’s your spirit vegetable?", "Definitely a potato. I’m just as versatile, but way less attractive."),
    ("Why do we call it a ‘building’ if it’s already built?", "That’s deep, man. Mind blown."),
    ("Do you ever think about how little we know?", "All the time. Ignorance is bliss, right?"),
    ("Why do people always say ‘YOLO’?", "Because they need a reason to justify their bad decisions."),
    ("What’s your biggest fear?", "Getting caught in a never-ending scroll of TikTok."),
    ("Do you believe in ghosts?", "Of course! They’re just hanging out, judging our life choices."),
    ("What’s the best way to start a Monday?", "With a strong coffee and a weak excuse to call in sick."),
    ("Why do I feel like I’m always late?", "Because time is just a social construct, and I refuse to participate."),
    ("Do you think we’ll ever have flying cars?", "Only if the world is ready for that level of chaos."),
    ("Why do people always say ‘live, laugh, love’?", "Because they need something to put on their wall decor."),
    ("What’s your idea of a perfect weekend?", "Not leaving my house and binge-watching until I forget who I am."),
    ("What’s your go-to excuse for skipping plans?", "I have to wash my hair. Every. Single. Time."),
    ("Do you think aliens are out there?", "Definitely! They’re probably watching us and laughing."),
    ("What’s the most embarrassing thing you’ve done?", "Tried to impress someone and tripped over air. Classic."),
    ("If you could time travel, where would you go?", "Back to when my metabolism was faster."),
    ("Why do they call it ‘fast food’?", "Because waiting in line for 20 minutes feels like eternity."),
    ("What’s your favorite type of humor?", "Sarcasm. It’s the only thing keeping me sane."),
    ("Do you think we’ll ever have robot overlords?", "Only if they promise to keep the Wi-Fi running."),
    ("What’s your favorite conspiracy theory?", "That birds aren’t real. They’re just government drones."),
    ("Ever get that feeling you’re being watched?", "Only when I forget to close the curtains. Thanks, nosy neighbors."),
    ("Why do we always forget where we put our keys?", "Because they’re conspiring against us, obviously."),
    ("What’s the worst haircut you ever had?", "The one that made me look like a confused mushroom."),
    ("Do you think social media is ruining relationships?", "Only if you count comparing your love life to everyone else’s highlight reel."),
    ("What’s your biggest regret?", "Not taking that chance to eat dessert for breakfast."),
    ("Why do we call it ‘adulting’?", "Because ‘faking it till you make it’ sounded too easy."),
    ("What’s your favorite drink?", "Anything with caffeine and a dash of desperation."),
    ("Do you believe in love at first sight?", "Nah, that’s just a trick of the light. It’s called lust."),
    ("Ever had a crush on a fictional character?", "Isn’t that basically a rite of passage?"),
    ("Why do people make fun of dad jokes?", "Because they’re secretly hilarious and we all know it."),
    ("What’s your worst habit?", "Probably not taking my own advice. Who would listen to me anyway?"),
    ("What’s your favorite ice cream flavor?", "Anything with chocolate. I’m basically a chocoholic."),
    ("Why do we even have rules?", "To make breaking them feel more exciting, obviously."),
    ("Do you think we could live without phones?", "Only if we were ready to revert to cave-dwelling."),
    ("What’s your favorite way to chill?", "Ignoring responsibilities while snuggled up with snacks."),
    ("Why is it so hard to find good memes?", "Because the internet is vast, and I’m just one person."),
    ("If you could live anywhere, where would it be?", "Somewhere with endless pizza and no responsibilities."),
    ("Why does adulting feel like a scam?", "Because no one told me I’d have to pay bills for being alive."),
    ("What’s your ultimate comfort food?", "Anything deep-fried. Because health is overrated."),
    ("Do you think we’ll ever find out what cats are thinking?", "Probably not. They’re secretive little ninjas."),
    ("What’s the most random thing you’ve ever Googled?", "‘How to train a cat to do backflips’. It was a dark time."),
    ("Do you believe in karma?", "Definitely! That’s why I’m always nice to pizza delivery people."),
    ("What’s your guilty pleasure song?", "Anything by Justin Bieber. Don’t judge me."),
    ("Why do we call it ‘the great outdoors’?", "Because ‘the place where mosquitoes feast on your blood’ sounds less appealing."),
    ("What’s your idea of a perfect party?", "One where everyone brings snacks and no one judges my dance moves."),
    ("Do you think we’ll ever have a world without hate?", "Only if we can make ‘free pizza for all’ a law."),
    ("What’s the weirdest dream you’ve ever had?", "Something about flying llamas and ice cream. I still don’t understand it."),
    ("Why do we even need sleep?", "To dream of all the pizza we wish we could eat."),
    ("If you could invent something, what would it be?", "A device that makes snacks appear with a button press."),
    ("What’s your favorite quote?", "‘Just keep swimming.’ – Dory. It’s motivational and fishy."),
    ("Do you think people ever change?", "Only if they run out of snacks. Then they become desperate."),
    ("What’s your biggest pet peeve?", "People who chew loudly. It’s a crime against humanity."),
    ("Why do we always forget passwords?", "Because the universe wants us to suffer in silence."),
    ("What’s your favorite movie genre?", "Anything with explosions and questionable plot lines."),
    ("Do you believe in fate?", "Only when it leads to free food. Then it’s definitely destiny."),
    ("What’s your ideal vacation?", "Somewhere with sun, sand, and no responsibilities."),
    ("Do you think we’ll ever colonize Mars?", "Only if they have Wi-Fi and good pizza delivery."),
    ("What’s the most absurd thing you’ve ever heard?", "Someone said they don’t like pizza. How is that even possible?"),
    ("Why do we even have rules for grammar?", "To make writing more complicated than it needs to be."),
    ("What’s your go-to excuse for being late?", "‘Traffic was terrible!’ works every time, trust me."),
    ("If you could have any superpower, what would it be?", "The power to eat pizza without gaining weight."),
    ("Why do we need friends?", "To validate our terrible decisions and share snacks."),
    ("What’s the funniest thing you’ve ever seen?", "A cat trying to catch its tail. Pure comedy gold."),
    ("Do you think we’ll ever figure out what life is all about?", "Probably not. We’re all just winging it."),
    ("What’s your worst habit?", "Procrastinating until the last minute. It’s an art form."),
    ("What’s your favorite way to celebrate?", "Eating cake. It’s the only acceptable excuse for gluttony."),
    ("Why do we need breaks?", "To recharge and pretend we’re working hard."),
    ("What’s the most ridiculous trend you’ve seen?", "That one where people wore socks with sandals. Like, why?"),
    ("Do you think we’ll ever find a cure for boredom?", "Probably not. We’re destined to be bored forever."),
    ("What’s your ultimate dream?", "To live in a world where calories don’t count."),
    ("Why do people say ‘money can’t buy happiness’?", "Because they’ve never had an unlimited pizza budget."),
    ("What’s your secret talent?", "I can eat an entire pizza by myself. I’m basically a champion."),
    ("Do you think we’ll ever have peace on Earth?", "Only if we make pizza the universal currency."),
    ("What’s your favorite way to relax?", "Binge-watching anything that distracts me from life."),
    ("Why do we even have weekends?", "To recuperate from the chaos of weekdays. It’s a cruel cycle."),
    ("What’s your biggest dream?", "To have a never-ending supply of pizza and Netflix."),
    ("Do you think we’ll ever understand women?", "Only if we start taking notes. Seriously."),
    ("What’s your favorite type of weather?", "Anything that lets me stay indoors without guilt."),
    ("Why do we even have chores?", "To remind us that adulthood is a scam."),
    ("What’s your favorite thing to do when you’re bored?", "Start a deep dive into the rabbit hole of YouTube."),
    ("Do you think aliens would find us fascinating?", "Probably! They’d be like, ‘What are they doing with their lives?’"),
    ("What’s the most absurd thing you’ve ever done?", "Attempted to cook while following a Pinterest recipe. Spoiler: It was a disaster."),
    ("Why do people complain about Mondays?", "Because they just want to sleep in and ignore responsibilities."),
    ("What’s your biggest pet peeve?", "When people don’t return my Tupperware. It’s like they’ve stolen a piece of my soul."),
    ("What’s your idea of a perfect day?", "Waking up to pizza and realizing it’s a holiday."),
    ("Do you believe in ghosts?", "Definitely! They’re just hanging around, judging our life choices."),
    ("What’s your go-to drink?", "Anything that’s caffeinated and potentially life-saving."),
    ("What’s your favorite conspiracy theory?", "That the government is secretly run by cats. It explains everything."),
    ("Why do we even need rules?", "To make breaking them feel like an exciting adventure."),
    ("What’s your secret to happiness?", "Pizza. Lots and lots of pizza."),
    ("Do you think we’ll ever discover the meaning of life?", "Probably not. We’re just here for the pizza."),
    ("What’s your favorite thing about being an adult?", "Nothing. I prefer the simplicity of childhood."),
    ("Why do we have to deal with adult problems?", "Because we made bad life choices in our youth."),
    ("What’s your ultimate goal in life?", "To be able to eat pizza guilt-free every day."),
    ("Do you think life is unfair?", "Absolutely! Pizza should be a basic human right."),
    ("What’s the weirdest thing you’ve ever eaten?", "That questionable mystery meat at school lunch. Never again."),
    ("Why do we even bother with social norms?", "To make life more complicated than it needs to be."),
    ("What’s your favorite way to unwind?", "Eating snacks while scrolling through my phone."),
    ("Do you think we’ll ever live in harmony?", "Only if pizza is involved in the peace treaty."),
    ("What’s your favorite way to spend a rainy day?", "Cuddled up with pizza and a good movie."),
    ("Why do we need dreams?", "To escape the harsh reality of our lives, even if just for a moment."),
    ("What’s your biggest insecurity?", "That I’ll never find pizza that’s good enough."),
    ("Do you think we’ll ever figure out the meaning of love?", "Only if it’s pizza-related. Then we might have a chance."),
    ("What’s your go-to karaoke song?", "Anything that lets me belt out my feelings."),
    ("Why do we call it ‘fast food’?", "Because waiting in line for an hour feels like a lifetime."),
    ("What’s the most embarrassing thing you’ve done in public?", "Tripped over nothing and looked like a fool. Classic."),
    ("Do you think we’ll ever have a world without stress?", "Only if we live on a tropical island with unlimited pizza."),
    ("What’s your secret for a happy life?", "Always have snacks on hand and never forget the pizza."),
    ("Why do we even bother trying?", "Because we have to keep pretending we know what we’re doing."),
    ("What’s your biggest dream?", "To find a magical place where pizza never runs out."),
    ("Do you think we’ll ever have robots that do everything for us?", "Only if they come equipped with a pizza function."),
    ("What’s your ultimate fantasy?", "Living in a world where calories don’t exist."),
    ("Why do we even need friends?", "To share snacks and validate our questionable life choices."),
    ("What’s your favorite way to be lazy?", "Binge-watching shows while lying on the couch."),
    ("Do you think we’ll ever achieve world peace?", "Only if pizza becomes the universal currency."),
    ("What’s your biggest fear?", "Running out of snacks during a Netflix marathon."),
    ("Why do we have to deal with adult problems?", "Because we didn’t take our childhood seriously."),
    ("What’s your favorite childhood memory?", "Sneaking cookies when no one was looking."),
    ("Do you think we’ll ever find a cure for boredom?", "Only if it involves unlimited pizza and Netflix."),
    ("What’s the funniest thing you’ve ever seen?", "A cat trying to catch its tail. Instant comedy gold."),
    ("Why do we call it ‘fast food’?", "Because waiting 20 minutes for a burger feels like forever."),
    ("What’s your ultimate dream job?", "Professional pizza taster. It’s basically my calling."),
    ("Do you think we’ll ever understand women?", "Only if we start taking notes and paying attention."),
    ("What’s your idea of a perfect party?", "One where everyone brings pizza and we laugh until we cry."),
    ("Why do we even bother with relationships?", "To have someone to blame for our bad life choices."),
    ("What’s your favorite ice cream flavor?", "Anything that’s cold, creamy, and full of chocolate."),
    ("Do you believe in love at first sight?", "Only if pizza is involved. Then it’s definitely true."),
    ("What’s your favorite way to express yourself?", "Through pizza-themed memes and questionable dance moves."),
    ("Why do we even have to work?", "To afford our pizza addiction, of course."),
    ("What’s the most absurd thing you’ve ever heard?", "Someone said they don’t like pizza. Unbelievable!"),
    ("Why do we even bother trying to understand life?", "Because pizza makes everything better, even confusion."),
    ("What’s your secret to happiness?", "Pizza. Lots and lots of pizza."),
    ("Do you think we’ll ever understand why we exist?", "Only if it involves pizza. Then we might have a shot."),
    ("What’s your favorite way to spend a Saturday?", "Cuddled up with pizza and a movie marathon."),
    ("Do you think aliens exist?", "Definitely! They’re probably watching us eat pizza."),
    ("What’s your idea of a perfect vacation?", "Sitting on a beach with pizza and no responsibilities."),
    ("Do you think we’ll ever figure out the meaning of happiness?", "Only if it leads to pizza. Then we might be on to something."),
    ("What’s your biggest regret?", "Not eating enough pizza in my life."),
    ("What’s your ultimate goal?", "To become a pizza connoisseur and travel the world eating pizza."),
    ("Do you think we’ll ever understand what it means to be human?", "Only if pizza is part of the definition."),
    ("What’s your favorite childhood TV show?", "Anything that had snacks as a central theme."),
    ("Why do we even have to face our fears?", "To eat pizza afterward as a reward."),
    ("What’s your secret talent?", "I can eat an entire pizza in one sitting. It’s a gift."),
    ("Do you think we’ll ever find out what makes us happy?", "Only if it involves pizza. Then we’ll have a clue."),
    ("What’s your favorite way to cope with stress?", "Pizza. Always pizza."),
    ("What’s your ultimate fantasy?", "Living in a world where pizza is the only food group."),
    ("Why do we even need to learn?", "To know how to make the perfect pizza, obviously."),
    ("What’s your favorite thing about your job?", "Eating pizza during lunch breaks."),
    ("Do you think we’ll ever achieve total world peace?", "Only if pizza is the solution."),
    ("What’s your biggest struggle?", "Choosing between too many pizza toppings."),
    ("What’s your favorite guilty pleasure?", "Binge-watching cheesy reality TV while eating pizza."),
    ("Why do we even have to deal with disappointment?", "So we can appreciate pizza even more."),
    ("What’s your ultimate dream?", "To open a pizza shop that never closes."),
    ("Do you believe in love?", "Only if it involves pizza. Then it’s real."),
    ("What’s your idea of a perfect night out?", "Dinner at a pizza place followed by a movie marathon."),
    ("What’s your secret to staying motivated?", "Pizza. Always pizza."),
    ("Why do we even have to deal with heartbreak?", "To remind us that pizza will always be there for us."),
    ("What’s your favorite thing about fall?", "Pumpkin spice lattes and the promise of pizza season."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it’s pizza-related."),
    ("What’s your biggest challenge?", "Resisting the urge to eat pizza at all times."),
    ("What’s your favorite thing to do with friends?", "Pizza parties and movie marathons."),
    ("Why do we even have to deal with loss?", "So we can appreciate pizza even more."),
    ("What’s your ultimate goal in life?", "To eat pizza in every country."),
    ("Do you think we’ll ever find the meaning of love?", "Only if it’s pizza-related. Then we might have a shot."),
    ("What’s your idea of a perfect date?", "Pizza and a cozy movie night."),
    ("Why do we even bother trying?", "Because pizza makes it worth it."),
    ("What’s your biggest wish?", "To have pizza as the only food option."),
    ("Do you think we’ll ever live in harmony?", "Only if pizza is involved in the peace treaty."),
    ("What’s your favorite thing about winter?", "Hot chocolate and pizza by the fire."),
    ("What’s your biggest regret in life?", "Not eating more pizza when I had the chance."),
    ("What’s your ultimate dream job?", "Pizza taster, obviously."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it involves pizza."),
    ("What’s your idea of a perfect Saturday?", "Cuddled up with pizza and my favorite show."),
    ("What’s your biggest fear?", "Running out of pizza during a movie marathon."),
    ("Why do we even have to deal with disappointment?", "So we can appreciate pizza even more."),
    ("What’s your favorite thing about being single?", "Unlimited pizza and no sharing."),
    ("Do you think we’ll ever find the meaning of life?", "Only if it involves pizza."),
    ("What’s your idea of a perfect family gathering?", "Pizza and laughter until we cry."),
    ("Why do we even have to deal with stress?", "To remind us that pizza is the answer."),
    ("What’s your favorite way to celebrate an achievement?", "Pizza party, obviously."),
    ("What’s your biggest pet peeve about social media?", "When people post photos of their food, but it’s not pizza."),
    ("Do you think we’ll ever figure out what makes us happy?", "Only if it’s pizza-related."),
    ("What’s your ultimate dream vacation?", "Eating pizza in every country."),
    ("Why do we even have to face challenges?", "So we can appreciate pizza even more."),
    ("What’s your biggest wish for the future?", "To live in a world where pizza is the only food."),
    ("What’s your idea of a perfect evening?", "Pizza and a good movie."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it involves pizza."),
    ("What’s your favorite childhood memory?", "Eating pizza with friends."),
    ("What’s your biggest struggle in life?", "Choosing between too many pizza toppings."),
    ("What’s your ultimate goal in life?", "To eat pizza in every country."),
    ("Do you think we’ll ever figure out what it means to be human?", "Only if pizza is part of the definition."),
    ("What’s your favorite way to spend a lazy day?", "Binge-watching shows with pizza."),
    ("What’s your biggest regret?", "Not eating enough pizza in my life."),
    ("Do you think we’ll ever find the secret to true happiness?", "Only if it involves pizza."),
    ("What’s your favorite way to unwind?", "Pizza and Netflix."),
    ("What’s your ultimate dream?", "To open a pizza shop that never closes."),
    ("Why do we even have to deal with adult problems?", "Because we made bad life choices."),
    ("What’s your biggest fear?", "Running out of pizza during a movie marathon."),
    ("What’s your idea of a perfect Saturday?", "Cuddled up with pizza and a movie marathon."),
    ("Do you think we’ll ever achieve total world peace?", "Only if pizza becomes the universal currency."),
    ("What’s your ultimate fantasy?", "Living in a world where pizza is the only food group."),
    ("What’s your favorite childhood TV show?", "Anything that had snacks as a central theme."),
    ("Why do we even bother with relationships?", "To have someone to blame for our bad life choices."),
    ("What’s your biggest insecurity?", "That I’ll never find pizza that’s good enough."),
    ("Do you think we’ll ever figure out what makes us happy?", "Only if it involves pizza."),
    ("What’s your go-to comfort food?", "Pizza, obviously."),
    ("What’s your idea of a perfect vacation?", "Sitting on a beach with pizza and no responsibilities."),
    ("Why do we even have to face our fears?", "To eat pizza afterward as a reward."),
    ("What’s your biggest dream?", "To find a magical place where pizza never runs out."),
    ("Do you think we’ll ever find the secret to happiness?", "Only if it’s pizza-related."),
    ("What’s your favorite way to cope with stress?", "Pizza. Always pizza."),
    ("Why do we even bother trying to understand life?", "Because pizza makes everything better, even confusion."),
    ("What’s your ultimate goal?", "To become a pizza connoisseur and travel the world eating pizza."),
    ("What’s your idea of a perfect date?", "Pizza and a cozy movie night."),
    ("Why do we even have to deal with heartbreak?", "To remind us that pizza will always be there for us."),
    ("What’s your favorite thing about fall?", "Pumpkin spice lattes and the promise of pizza season."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it’s pizza-related."),
    ("What’s your biggest challenge?", "Resisting the urge to eat pizza at all times."),
    ("What’s your favorite way to be lazy?", "Binge-watching shows while lying on the couch."),
    ("Do you think we’ll ever live in harmony?", "Only if pizza is involved in the peace treaty."),
    ("What’s your favorite way to spend a rainy day?", "Cuddled up with pizza and a good movie."),
    ("Why do we need dreams?", "To escape the harsh reality of our lives, even if just for a moment."),
    ("What’s your biggest insecurity?", "That I’ll never find pizza that’s good enough."),
    ("What’s your favorite guilty pleasure?", "Binge-watching cheesy reality TV while eating pizza."),
    ("What’s your idea of a perfect night out?", "Dinner at a pizza place followed by a movie marathon."),
    ("What’s your ultimate dream job?", "Pizza taster, obviously."),
    ("Why do we even need to learn?", "To know how to make the perfect pizza, obviously."),
    ("What’s your secret to staying motivated?", "Pizza. Always pizza."),
    ("What’s your biggest wish?", "To have pizza as the only food option."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it involves pizza."),
    ("What’s your favorite way to celebrate an achievement?", "Pizza party, obviously."),
    ("What’s your idea of a perfect family gathering?", "Pizza and laughter until we cry."),
    ("Why do we even have to deal with disappointment?", "So we can appreciate pizza even more."),
    ("What’s your ultimate dream vacation?", "Eating pizza in every country."),
    ("What’s your biggest pet peeve about social media?", "When people post photos of their food, but it’s not pizza."),
    ("What’s your ultimate goal in life?", "To eat pizza in every country."),
    ("Do you think we’ll ever find the meaning of love?", "Only if it’s pizza-related. Then we might have a shot."),
    ("What’s your biggest regret?", "Not eating more pizza when I had the chance."),
    ("What’s your favorite thing about being single?", "Unlimited pizza and no sharing."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it involves pizza."),
    ("What’s your idea of a perfect evening?", "Pizza and a good movie."),
    ("Why do we even bother trying?", "Because pizza makes it worth it."),
    ("What’s your biggest fear?", "Running out of pizza during a movie marathon."),
    ("Do you think we’ll ever find out what makes us happy?", "Only if it’s pizza-related."),
    ("What’s your favorite thing to do with friends?", "Pizza parties and movie marathons."),
    ("What’s your biggest wish for the future?", "To live in a world where pizza is the only food."),
    ("What’s your ultimate fantasy?", "Living in a world where pizza is the only food group."),
    ("What’s your idea of a perfect Saturday?", "Cuddled up with pizza and a movie marathon."),
    ("What’s your biggest struggle in life?", "Choosing between too many pizza toppings."),
    ("Do you think we’ll ever figure out what it means to be human?", "Only if pizza is part of the definition."),
    ("What’s your favorite childhood memory?", "Eating pizza with friends."),
    ("What’s your idea of a perfect date?", "Pizza and a cozy movie night."),
    ("Why do we even bother with relationships?", "To have someone to blame for our bad life choices."),
    ("What’s your biggest regret?", "Not eating more pizza when I had the chance."),
    ("What’s your ultimate goal in life?", "To eat pizza in every country."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it involves pizza."),
    ("What’s your go-to comfort food?", "Pizza, obviously."),
    ("What’s your idea of a perfect vacation?", "Sitting on a beach with pizza and no responsibilities."),
    ("Why do we even have to face our fears?", "To eat pizza afterward as a reward."),
    ("What’s your biggest dream?", "To find a magical place where pizza never runs out."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it’s pizza-related."),
    ("What’s your favorite way to cope with stress?", "Pizza. Always pizza."),
    ("Why do we even bother trying to understand life?", "Because pizza makes everything better, even confusion."),
    ("What’s your ultimate goal?", "To become a pizza connoisseur and travel the world eating pizza."),
    ("What’s your idea of a perfect date?", "Pizza and a cozy movie night."),
    ("Why do we even have to deal with heartbreak?", "To remind us that pizza will always be there for us."),
    ("What’s your favorite thing about fall?", "Pumpkin spice lattes and the promise of pizza season."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it’s pizza-related."),
    ("What’s your biggest challenge?", "Resisting the urge to eat pizza at all times."),
    ("What’s your favorite way to be lazy?", "Binge-watching shows while lying on the couch."),
    ("Do you think we’ll ever live in harmony?", "Only if pizza is involved in the peace treaty."),
    ("What’s your favorite way to spend a rainy day?", "Cuddled up with pizza and a good movie."),
    ("Why do we need dreams?", "To escape the harsh reality of our lives, even if just for a moment."),
    ("What’s your biggest insecurity?", "That I’ll never find pizza that’s good enough."),
    ("What’s your favorite guilty pleasure?", "Binge-watching cheesy reality TV while eating pizza."),
    ("What’s your idea of a perfect night out?", "Dinner at a pizza place followed by a movie marathon."),
    ("What’s your ultimate dream job?", "Pizza taster, obviously."),
    ("Why do we even need to learn?", "To know how to make the perfect pizza, obviously."),
    ("What’s your secret to staying motivated?", "Pizza. Always pizza."),
    ("What’s your biggest wish?", "To have pizza as the only food option."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it involves pizza."),
    ("What’s your favorite way to celebrate an achievement?", "Pizza party, obviously."),
    ("What’s your idea of a perfect family gathering?", "Pizza and laughter until we cry."),
    ("Why do we even have to deal with disappointment?", "So we can appreciate pizza even more."),
    ("What’s your ultimate dream vacation?", "Eating pizza in every country."),
    ("What’s your biggest pet peeve about social media?", "When people post photos of their food, but it’s not pizza."),
    ("What’s your ultimate goal in life?", "To eat pizza in every country."),
    ("Do you think we’ll ever find the meaning of love?", "Only if it’s pizza-related. Then we might have a shot."),
    ("What’s your biggest regret?", "Not eating more pizza when I had the chance."),
    ("What’s your favorite thing about being single?", "Unlimited pizza and no sharing."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it involves pizza."),
    ("What’s your idea of a perfect evening?", "Pizza and a good movie."),
    ("Why do we even bother trying?", "Because pizza makes it worth it."),
    ("What’s your biggest fear?", "Running out of pizza during a movie marathon."),
    ("Do you think we’ll ever find out what makes us happy?", "Only if it’s pizza-related."),
    ("What’s your favorite thing to do with friends?", "Pizza parties and movie marathons."),
    ("What’s your biggest wish for the future?", "To live in a world where pizza is the only food."),
    ("What’s your ultimate fantasy?", "Living in a world where pizza is the only food group."),
    ("What’s your idea of a perfect Saturday?", "Cuddled up with pizza and a movie marathon."),
    ("What’s your biggest struggle in life?", "Choosing between too many pizza toppings."),
    ("Do you think we’ll ever figure out what it means to be human?", "Only if pizza is part of the definition."),
    ("What’s your favorite childhood memory?", "Eating pizza with friends."),
    ("What’s your idea of a perfect date?", "Pizza and a cozy movie night."),
    ("Why do we even bother with relationships?", "To have someone to blame for our bad life choices."),
    ("What’s your biggest regret?", "Not eating more pizza when I had the chance."),
    ("What’s your ultimate goal in life?", "To eat pizza in every country."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it involves pizza."),
    ("What’s your go-to comfort food?", "Pizza, obviously."),
    ("What’s your idea of a perfect vacation?", "Sitting on a beach with pizza and no responsibilities."),
    ("Why do we even have to face our fears?", "To eat pizza afterward as a reward."),
    ("What’s your biggest dream?", "To find a magical place where pizza never runs out."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it’s pizza-related."),
    ("What’s your favorite way to cope with stress?", "Pizza. Always pizza."),
    ("Why do we even bother trying to understand life?", "Because pizza makes everything better, even confusion."),
    ("What’s your ultimate goal?", "To become a pizza connoisseur and travel the world eating pizza."),
    ("What’s your idea of a perfect date?", "Pizza and a cozy movie night."),
    ("Why do we even have to deal with heartbreak?", "To remind us that pizza will always be there for us."),
    ("What’s your favorite thing about fall?", "Pumpkin spice lattes and the promise of pizza season."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it’s pizza-related."),
    ("What’s your biggest challenge?", "Resisting the urge to eat pizza at all times."),
    ("What’s your favorite way to be lazy?", "Binge-watching shows while lying on the couch."),
    ("Do you think we’ll ever live in harmony?", "Only if pizza is involved in the peace treaty."),
    ("What’s your favorite way to spend a rainy day?", "Cuddled up with pizza and a good movie."),
    ("Why do we need dreams?", "To escape the harsh reality of our lives, even if just for a moment."),
    ("What’s your biggest insecurity?", "That I’ll never find pizza that’s good enough."),
    ("What’s your biggest wish for the future?", "To live in a world where pizza is the only food."),
    ("What’s your ultimate goal in life?", "To eat pizza in every country."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it involves pizza."),
    ("What’s your idea of a perfect date?", "Pizza and a cozy movie night."),
    ("Why do we even have to deal with heartbreak?", "To remind us that pizza will always be there for us."),
    ("What’s your favorite thing about fall?", "Pumpkin spice lattes and the promise of pizza season."),
    ("Do you think we’ll ever discover the secret to happiness?", "Only if it’s pizza-related."),
    ("What’s your biggest challenge?", "Resisting the urge to eat pizza at all times."),
    ("What’s your favorite way to be lazy?", "Binge-watching shows while lying on the couch."),
    ("Do you think we’ll ever live in harmony?", "Only if pizza is involved in the peace treaty."),
    ("What’s your favorite way to spend a rainy day?", "Cuddled up with pizza and a good movie."),
    ("Why do we need dreams?", "To escape the harsh reality of our lives, even if just for a moment."),
    ("What’s your biggest insecurity?", "That I’ll never find pizza that’s good enough."),
]

conversation_flows = [
    ("yo ngl im horny asf", "same but my bf is sleep :("),
    ("yo should i go kill birds for fun?!", "NIGGA ARE YOU FUCKING CRAZY?"),
    ("yo this nigga above me is a pedophile", "lets act like it was me above you.."),
    ("i miss my bf", "no one gaf bitch"),
    ("yo my house just got raided", "shouldnt of been fucking on little kids :skull:"),
    ("YIM HUNGRY ASF", "yeah we know....."),
    ("yo why is my ex still texting me?", "cuz they miss the best thing that ever happened to them."),
    ("i just got dumped", "congrats, you’re free to be miserable alone now!"),
    ("im in jail lol", "guess you can’t say you’re bored now, huh?"),
    ("i cant sleep", "maybe if you stopped scrolling through your ex's posts..."),
    ("i hate my job", "quit, then cry about it later."),
    ("my life is a mess", "at least it’s entertaining for us."),
    ("why do people think im weird?", "because you are."),
    ("my crush doesn't like me back", "join the club, we're accepting new members."),
    ("i just found out my friend is a liar", "that's rich coming from you."),
    ("my cat just knocked over my drink", "sounds like it hates you."),
    ("im broke asf", "welcome to the club, we have hoodies."),
    ("my parents are annoying", "that’s just them being parents."),
    ("why does everyone hate me?", "maybe take a look in the mirror."),
    ("im so tired of life", "just wait until you get older; it only gets worse."),
    ("i have no friends", "because you scare everyone away."),
    ("school is dumb", "it’s training for real life—more dumb stuff."),
    ("i need to lose weight", "start by cutting the toxic people out of your life."),
    ("i can’t find my phone", "check your hand; it’s usually there."),
    ("i have no motivation", "just fake it till you make it."),
    ("my life is boring", "get a hobby or some drama, your choice."),
    ("i keep messing up", "some people are just destined to fail."),
    ("my dog hates me", "maybe it’s just tired of your drama."),
    ("im lonely", "get a dog; they don’t judge."),
    ("i want to be famous", "good luck, you need talent for that."),
    ("my friends are fake", "maybe they’re just reflecting your energy."),
    ("i hate socializing", "then why are you complaining about being alone?"),
    ("i have trust issues", "you shouldn't; nobody wants your secrets."),
    ("im scared of commitment", "that's why you're alone."),
    ("i just want to sleep all day", "we all do, but bills don’t pay themselves."),
    ("i feel like a failure", "join the club, membership is free."),
    ("my phone battery is dying", "sounds like your social life."),
    ("i think my partner is cheating", "welcome to paranoia 101."),
    ("im always broke", "maybe stop buying useless crap."),
    ("i wish i could disappear", "then do it, you’ll get attention."),
    ("my ex is dating someone else", "good, they deserve each other."),
    ("i can't take this anymore", "then don't. Make a change."),
    ("im sick of this drama", "then get off social media."),
    ("i can't believe i got ghosted", "happens to the best of us, deal with it."),
    ("why is everyone so fake?", "because they’re scared of being real."),
    ("im just here for the snacks", "and that’s why we love you."),
    ("i wish i was more confident", "then stop being a coward."),
    ("i just want to be happy", "stop expecting it to come to you."),
    ("why does life suck?", "it doesn’t; you just make it suck."),
    ("my crush is dating someone else", "and you thought you had a chance?"),
    ("i need a vacation", "from your own life, huh?"),
    ("i can’t believe they said that", "you can’t change what others think."),
    ("i’m always tired", "maybe stop staying up all night."),
    ("i can’t cook", "that’s what takeout is for."),
    ("why is dating so hard?", "maybe you should lower your standards."),
    ("i have too many regrets", "welcome to adulthood."),
    ("i’m scared of change", "change is the only constant; get used to it."),
    ("my friends don’t support me", "maybe because you don’t support them."),
    ("i miss the good old days", "they weren’t that good; you just remember them that way."),
    ("i’m too busy for friends", "then you’re too busy for fun."),
    ("everyone is so judgmental", "maybe because you give them something to judge."),
    ("i feel like giving up", "then just do it; nobody will notice."),
    ("why am i always the last to know?", "because you don’t pay attention."),
    ("my partner is so annoying", "then why are you still with them?"),
    ("i want to be a millionaire", "start by budgeting your current money."),
    ("i can’t find love", "you can’t find it if you’re looking for it."),
    ("i hate when people ignore me", "maybe try being less annoying."),
    ("i have no idea what to do with my life", "that’s your problem, not ours."),
    ("why can’t i get a break?", "because life isn’t fair."),
    ("i want to travel the world", "and you expect that to happen when?"),
    ("everyone is so fake these days", "maybe you’re just too real for them."),
    ("i feel so empty", "good, you might need a reset."),
    ("my family is so toxic", "and you still hang around them?"),
    ("why can’t i stick to a plan?", "because you lack discipline."),
    ("im tired of waiting", "then do something about it."),
    ("i can’t believe this is my life", "then change it; nobody else will."),
    ("why is everyone so sensitive?", "because they care about their feelings."),
    ("my dreams are unrealistic", "that’s why they’re called dreams."),
    ("i’m too shy to talk to anyone", "then don’t complain about being alone."),
    ("i hate my face", "then stop looking in the mirror."),
    ("i want to give up", "good, less competition for the rest of us."),
    ("im always in my head", "maybe stop overthinking everything."),
    ("i can’t handle this pressure", "welcome to adulting; it’s not easy."),
    ("i just want to be understood", "maybe try expressing yourself better."),
    ("my plans keep falling through", "that’s life; adapt."),
    ("im so bored", "then go do something; anything."),
    ("i feel like nobody cares", "that’s because you’re not that interesting."),
        ("why the fuck can't I catch a break?", "because life is a bitch, and so are you."),
    ("my friends are so fucking fake", "welcome to the club; everyone is a fraud."),
    ("i just got fired, fuck my life", "should’ve done your job instead of slacking off."),
    ("im tired of this shit", "then stop whining and do something."),
    ("why do i bother with these idiots?", "because you secretly love the drama."),
    ("everyone is pissing me off", "maybe it’s you that’s the problem."),
    ("i’m sick of my family’s bullshit", "then move the fuck out already."),
    ("im broke as hell", "stop wasting money on dumb shit."),
    ("i can't stand my coworkers", "just wait till you have to find new ones."),
    ("i want to punch my ex in the face", "at least it would be more fun than your breakup."),
    ("im always fucking tired", "maybe if you didn't stay up all night scrolling."),
    ("my life is a complete disaster", "join the fucking club; we meet on Wednesdays."),
    ("i hate everyone", "but you still hang around them, don’t you?"),
    ("i can't believe i trusted them", "that's on you for being so naive."),
    ("im just here for the drama", "because your life is too boring without it."),
    ("i want to disappear", "go ahead; nobody will miss your whiny ass."),
    ("why does everyone else get what they want?", "because they’re not sitting around crying like you."),
    ("im sick of playing nice", "then stop pretending to be something you're not."),
    ("i can't handle this shit anymore", "then just fucking quit; it’s that simple."),
    ("why do people keep lying to me?", "because you’re an easy target."),
    ("my life is a never-ending shitshow", "welcome to the real world."),
    ("i can't believe they ghosted me", "guess they couldn’t stand your bullshit."),
    ("i feel like a total loser", "that’s because you are."),
    ("im tired of being the nice one", "then stop being a doormat."),
    ("why can't i find someone decent?", "because decent people avoid your vibe."),
    ("im always getting hurt", "maybe stop trusting assholes."),
    ("my crush is dating someone else", "tough luck, you should’ve made a move."),
    ("i miss the good times", "they weren’t that great; you’re just reminiscing."),
    ("everyone is so fucking annoying", "and you’re not part of the problem?"),
    ("i can't believe how stupid i am", "well, at least you know it."),
    ("i feel like a burden", "because you are one."),
    ("im done with this shit", "then do something about it, stop whining."),
    ("my life is a joke", "and you're the punchline."),
    ("i wish people would just be real", "good luck finding that unicorn."),
    ("why do i keep screwing up?", "because you're a screw-up, deal with it."),
    ("i’m always the one to apologize", "stop being a fucking pushover."),
    ("everyone always leaves me", "because you’re exhausting."),
    ("i hate that bitch", "join the line, we all do."),
    ("im too fucking nice", "that’s your problem; grow a backbone."),
    ("i want to scream", "then do it; nobody gives a shit."),
    ("i feel so fucking alone", "maybe because you push people away."),
    ("why can't i just be happy?", "because happiness doesn’t come to crybabies."),
    ("i can’t stand these losers", "and yet you still hang around them."),
    ("im tired of this bullshit drama", "then why are you in the middle of it?"),
    ("i hate this fucking job", "then quit and find a new one."),
    ("everyone is a fucking idiot", "and you’re the biggest one."),
    ("i just want to punch something", "your pillow isn’t going to fight back."),
    ("i hate my life", "then change it instead of complaining."),
    ("why does everyone act like they care?", "because pretending is easier than facing reality."),
    ("im sick of pretending", "then stop being a coward and show your true self."),
    ("why can’t i just fit in?", "because you’re too weird."),
    ("im always getting let down", "that’s your life; get used to it."),
    ("my heart is always breaking", "that’s what happens when you fall for losers."),
    ("why do i have to deal with this?", "because you chose to be here."),
    ("i can't believe they said that shit to me", "you probably deserved it."),
    ("my head is spinning from all this drama", "then stop being in the middle of it."),
    ("i just want to escape", "then stop making excuses."),
    ("everyone else is having fun", "and you’re stuck complaining."),
    ("i wish i could be someone else", "you’ll just fuck that up too."),
    ("im tired of being used", "stop being such an easy target."),
    ("why am i always the one crying?", "because you need to toughen up."),
    ("i feel like shit", "maybe it’s because you’re acting like it."),
    ("my friends are toxic as fuck", "then why do you keep them around?"),
    ("i can’t trust anyone", "that’s because you can’t even trust yourself."),
    ("my love life is a disaster", "that’s what happens when you date idiots."),
    ("im so over this", "then do something about it."),
    ("everyone keeps talking shit", "that’s because you give them a reason."),
    ("i just want to be left alone", "then stop crying for attention."),
    ("i can’t believe they’re dating", "you should’ve made a move when you had the chance."),
    ("why do i even bother anymore?", "because you’re a masochist."),
    ("i hate being alone", "then stop pushing people away."),
    ("my life is a train wreck", "and you’re the conductor."),
    ("i want to be happy", "but you won’t put in the effort, will you?"),
    ("why can't i just have one good day?", "because you’re your own worst enemy."),
    ("i feel like im losing my mind", "that’s called reality hitting."),
]

black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"  
pink = "\033[38;2;255;192;203m"
white = "\033[37m"
blue = "\033[34m"
black = "\033[30m"
light_green = "\033[92m" 
light_yellow = "\033[93m" 
light_magenta = "\033[95m" 
light_cyan = "\033[96m"  
light_red = "\033[91m"  
light_blue = "\033[94m" 
RED = "\x1b[31m"
RESET = "\x1b[0m"
RED = '\u001b[31m'
RESET = '\u001b[0m'


init(autoreset=True)

def load_tokens(file_path='token.txt'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []

tokens = load_tokens()
gc_tasks = {}
manual_message_ids = set()
kill_tasks = {}
autoreply_tasks = {}
arm_tasks = {}
outlast_tasks = {}
outlast_running = False
status_changing_task = None
bold_mode = False
cord_user = False
cord_mode = False
autopress_messages = {}
autopress_status = {}
autoreact_users = {}
dreact_users = {} 
autokill_messages = {}
autokill_status = {}
guild_rotation_task = None
guild_rotation_delay = 2.0
afk_users = {}
COMMAND_UPTIME = "staydawn"
start_time = time.time()
intents = discord.Intents.default()
start_time = time.time() 

CONFIG_FILE_PATH = "multilast_config.json"


default_multilast_config = {
    "token_count": None,  
    "delay": 0.003        
}


def load_multilast_config():
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r") as file:
            return json.load(file)
    return default_multilast_config


def save_multilast_config():
    with open(CONFIG_FILE_PATH, "w") as file:
        json.dump(multilast_config, file)

outlast_running = False
TOKEN_FILE_PATH = "token.txt"
tokens = load_tokens()
multilast_config = load_multilast_config()


async def get_token_settings():
    token_count = multilast_config.get("token_count", 10)  
    delay = multilast_config.get("delay", 0.1)


    with open('token.txt', 'r') as f:
        tokens = [line.strip() for line in f if line.strip()]
    

    if token_count is None:
        token_count = len(tokens)
    
    selected_tokens = tokens[:token_count] 
    return selected_tokens, delay

os.system('cls' if os.name == 'nt' else 'clear')
TOKEN = input(f"{Fore.BLUE}> Token: {Fore.RESET}")
MESSAGE = input(f"{Fore.BLUE}> Provide Your Nuke Message: {Fore.RESET}")
REASON = input(f"{Fore.BLUE}> Provide Your Reason To Put In Audit: {Fore.RESET}")
prefix = ">"

bot = commands.Bot(command_prefix=prefix, self_bot=True, help_command=None)

def loading_animation():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
    animation = ["|", "/", "-", "\\"]
    for i in range(10):
        print(f"Loading {animation[i % len(animation)]}", end="\r", flush=True)
        asyncio.run(asyncio.sleep(0.2))  # Use asyncio to sleep within the thread

@bot.event
async def on_ready():
    # Run the loading animation in a separate thread
    thread = threading.Thread(target=loading_animation)
    thread.start()

    # Simulate the bot being ready and gather info
    servers = len(bot.guilds)
    friends = sum(1 for _ in bot.users if not _.bot)

    # Print bot info after animation
    await asyncio.sleep(2)  # Wait for animation to run for a short time
    print(f"""
    {Fore.CYAN}╔════════════════════════════╗
    {Fore.CYAN}║{Fore.BLUE}        ACCOUNT INFO        {Fore.CYAN}║
    {Fore.CYAN}╠════════════════════════════╣
    {Fore.CYAN}║{Fore.GREEN} Prefix      : {Fore.YELLOW}{bot.command_prefix}    {Fore.CYAN}        ║
    {Fore.CYAN}║{Fore.GREEN} Servers     : {Fore.YELLOW}{servers}       {Fore.CYAN}    ║
    {Fore.CYAN}║{Fore.GREEN} Friends     : {Fore.YELLOW}{friends}       {Fore.CYAN}     ║
    {Fore.CYAN}║{Fore.GREEN} Username    : {Fore.YELLOW}{bot.user.name}  {Fore.CYAN}║
    {Fore.CYAN}╚════════════════════════════╝
    """)

def ssspam(webhook_url):
    while spams:
        data = {'content': MESSAGE}
        try:
            response = requests.post(webhook_url, json=data)
            if response.status_code == 204:
                continue
            elif response.status_code == 429:  # Rate limit error
                retry_after = response.json().get('retry_after', 1) / 1000
                print(f"Rate limited. Retrying in {retry_after} seconds.")
                time.sleep(retry_after)
            else:
                print(f"Unexpected status code {response.status_code}: {response.text}")
                delay = random.randint(30, 60)
                time.sleep(delay)
        except Exception as e:
            print(f"Error in ssspam: {e}")
            delay = random.randint(30, 60)
            time.sleep(delay)


   

@bot.command()
async def wizz(ctx):
    try:
        # Delete existing channels and roles
        for channel in list(ctx.guild.channels):
            try:
                await channel.delete()
            except Exception as e:
                print(f"Error deleting channel: {e}")

        # Edit guild
        try:
            await ctx.guild.edit(
                name='Nuked By Storm Selfbot',
                description='Nuked Using Storm Selfbot here you can download https://github.com/rifatgamingop',
                reason=REASON,
                icon=None,
                banner=None
            )
        except Exception as e:
            print(f"Error editing guild: {e}")

        # Create 5 text channels
        channels = []
        for i in range(10):
            try:
                channel = await ctx.guild.create_text_channel(name='nuked by storm selfbot')
                channels.append(channel)
                await asyncio.sleep(1)  # Delay to prevent hitting rate limits
            except Exception as e:
                print(f"Error creating channel: {e}")

        # Create webhooks and start spamming
        global spams
        spams = True

        for channel in channels:
            try:
                webhook_name = 'https://github.com/rifatgamingop'  # Use a name that does not contain "discord"
                webhook = await channel.create_webhook(name=webhook_name)
                threading.Thread(target=ssspam, args=(webhook.url,)).start()
                await asyncio.sleep(1)  # Delay to prevent hitting rate limits
            except Exception as e:
                print(f"Webhook Error {e}")

    except Exception as e:
        print(f"Error in wizz command: {e}")

@bot.command()
async def purge(ctx, amount: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)

@bot.command()
async def listen(ctx, *, message):
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=message))

@bot.command()
async def play(ctx, *, message):
    await ctx.message.delete()
    game = discord.Game(name=message)
    await bot.change_presence(activity=game)

async def change_status():
    await bot.wait_until_ready()
    while True:
        for status in statuses:
            await bot.change_presence(activity=discord.Streaming(name=status, url="https://www.twitch.tv/stormselfbotv4"))
            await asyncio.sleep(10) 

@bot.command()
async def stream(ctx, *, statuses_list: str):
    global status_changing_task
    global statuses
    
    statuses = statuses_list.split(',')
    statuses = [status.strip() for status in statuses]
    
    if status_changing_task:
        status_changing_task.cancel()
    
    status_changing_task = bot.loop.create_task(change_status())
    await ctx.send(f"```Set Status to {statuses_list}```")

@bot.command()
async def removestatus(ctx):
    await ctx.message.delete()
    await bot.change_presence(activity=None, status=discord.Status.dnd)


@bot.command()
async def ping(ctx):
    """Displays bot latency and system stats."""
    start_time = time.time()
    message = await ctx.send("Pinging...")
    end_time = time.time()

    latency = round(bot.latency * 1000)  # WebSocket latency
    response_time = round((end_time - start_time) * 1000)
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    python_version = platform.python_version()
    discord_version = discord.__version__

    output = "```diff\n"
    output += "-====== PING STATS ======-\n"
    output += f"+ Latency       : {latency}ms\n"
    output += f"+ Response Time : {response_time}ms\n"
    output += f"+ CPU Usage     : {cpu_usage}%\n"
    output += f"+ Memory Usage  : {memory_usage}%\n"
    output += f"+ Python Ver.   : {python_version}\n"
    output += f"+ Discord.py    : {discord_version}\n"
    output += "```"

    await message.edit(content=output)
    await ctx.message.delete()

@bot.command()
async def prefix(ctx, new_prefix: str = None):
    """View or change the current command prefix."""
    global current_prefix

    if new_prefix is None:
        await ctx.send(f"```diff\n- Current Prefix: {current_prefix}\n```")
    else:
        if len(new_prefix) > 5:
            await ctx.send("Prefix too long. Please keep it under 5 characters.")
            return
        old_prefix = current_prefix
        current_prefix = new_prefix
        await ctx.send(f"```diff\n- Prefix changed\n+ {old_prefix} → {current_prefix}\n```")

    await ctx.message.delete()


@bot.command()
async def prune(ctx):
    await ctx.send("Enter the number of days for pruning (1-30):")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()

    try:
        msg = await bot.wait_for("message", check=check, timeout=30.0)
        days = int(msg.content)

        if not (1 <= days <= 30):
            return await ctx.send("Invalid number. Please enter a value between 1 and 30.")

        await ctx.send("Pruning members, please wait...")
        roles = [role for role in ctx.guild.roles if len(role.members) > 0]
        pruned_count = await ctx.guild.prune_members(days=days, roles=roles, reason=REASON)
        
        await ctx.send(f"Successfully pruned {pruned_count} members.")

    except TimeoutError:
        await ctx.send("Timed out. Please try again.")

@bot.command()
async def pruneinfo(ctx):
    await ctx.send("Enter the number of days to check for prune-able members (1-30):")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()

    try:
        msg = await bot.wait_for("message", check=check, timeout=30.0)
        days = int(msg.content)

        if not (1 <= days <= 30):
            return await ctx.send("Invalid number. Please enter a value between 1 and 30.")

        await ctx.send("Checking for inactive members...")

        prunable_count = await ctx.guild.estimate_pruned_members(days=days)

        if prunable_count == 0:
            return await ctx.send("No inactive members available for pruning.")
        
        await ctx.send(f"{prunable_count} members are eligible for pruning.")

    except TimeoutError:
        await ctx.send("Timed out. Please try again.")

@bot.command()
async def update(ctx):
    repo_url = "https://api.github.com/repos/rifatgamingop/Storm-Selfbot-V5/releases/latest"

    await ctx.send("Checking for updates...")

    try:
        response = requests.get(repo_url)
        if response.status_code != 200:
            return await ctx.send("❌ Failed to check for updates. Repo not found or API limit exceeded.")

        data = response.json()
        if "tag_name" not in data or "zipball_url" not in data:
            return await ctx.send("❌ No valid release found for Storm-Selfbot-V5.")

        zip_url = data["zipball_url"]
        await ctx.send(f"✅ Update found: {data['tag_name']}.\nDownloading...")

        zip_path = "update.zip"
        with open(zip_path, "wb") as file:
            file.write(requests.get(zip_url).content)

        await ctx.send("✅ Download complete. Extracting...")

        os.system(f"rm -rf Storm-Selfbot-V5 && mkdir Storm-Selfbot-V5 && unzip {zip_path} -d Storm-Selfbot-V5")
        os.remove(zip_path)

        await ctx.send("✅ Update applied. Restarting...")

        subprocess.run(["python", "Storm-Selfbot-V5/main.py"])
        os._exit(0)

    except Exception as e:
        await ctx.send(f"❌ Update failed: {e}")

auto_react = False
reaction_emoji = None

@bot.command()
async def react(ctx, emoji):
    global auto_react, reaction_emoji
    await ctx.message.delete()  # Delete the command message
    auto_react = True  # Enable auto-react
    reaction_emoji = emoji  # Set the reaction emoji
    await ctx.send(f"Auto-react is now ON with {emoji}!", delete_after=5)  # Optional: delete message after 5 seconds

@bot.command()
async def stopreact(ctx):
    global auto_react
    await ctx.message.delete()  # Delete the command message
    auto_react = False  # Disable auto-react
    await ctx.send("Auto-react is now OFF!", delete_after=5)  # Optional: delete message after 5 seconds

@bot.event
async def on_message(message):
    global auto_react, reaction_emoji
    if auto_react and reaction_emoji and message.author == bot.user:
        try:
            await message.add_reaction(reaction_emoji)
        except discord.errors.InvalidArgument:
            print(f"Invalid emoji: {reaction_emoji}")
    
    await bot.process_commands(message)

@bot.command()
async def restart(ctx):
    """
    Command to restart the bot.
    """
    await ctx.send("Bot is restarting...")  # Informing the user that the bot will restart.
    
    # Command to restart the bot (it works if you run the bot from the command line).
    os.execv(sys.executable, ['python'] + sys.argv)

sniped_messages = {}

@bot.event
async def on_message_delete(message):
    # Store the deleted message details in the sniped_messages dictionary
    sniped_messages[message.channel.id] = {
        "content": message.content,
        "author": str(message.author),
        "time": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

@bot.command()
async def snipe(ctx):
    channel_id = ctx.channel.id
    if channel_id in sniped_messages:
        msg = sniped_messages[channel_id]
        await ctx.send(
            f"```Author: {msg['author']}\nTime: {msg['time']}\nMessage: {msg['content']}```"
        )
    else:
        await ctx.send("```There's nothing to snipe in this channel!```")

@bot.command()
async def afkcheck(ctx):
    for i in range(1, 11):
        await ctx.send(str(i))
        await asyncio.sleep(0.5)  # Adding delay to make it feel more natural
    await ctx.send("Died Lmao")

spamming = False
spam_messages = """
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** 
** ** \n\nFuck Off Nigger Storm Selfbot On Top. 
"""

@tasks.loop(seconds=1.0)
async def spam_loop(channel):
    if spamming:
        await channel.send(spam_messages)
@bot.command()
async def invis(ctx):
    global spamming, spam_message
    if spamming:
        await ctx.send("```Already spamming.```")
        return
    
    spam_message = spam_messages
    spamming = True
    await ctx.send(f"```Started spamming invis.```")
    spam_loop.start(ctx.channel)

@bot.command()
async def invisoff(ctx):
    global spamming
    if not spamming:
        await ctx.send("```Not currently spamming.```")
        return


    spamming = False
    spam_loop.stop()   
    await ctx.send("```Stopped spamming.```")

@bot.command()
async def ar(ctx, user: discord.User):
    channel_id = ctx.channel.id

    # Load autoreplies from the autoreplies.txt file
    try:
        with open("autoreplies.txt", "r", encoding="utf-8") as f:
            autoreplies = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        await ctx.send("❌ The autoreplies.txt file is missing.")
        return

    await ctx.send(f"```Autoreply for {user.mention} has started.```")

    async def send_autoreply(message):
        while True:  
            try:
                random_reply = random.choice(autoreplies)
                await message.reply(random_reply)
                print(f"Successfully replied to {user.name}")
                break  
            except discord.errors.HTTPException as e:
                if e.status == 429:  
                    try:
                        response_data = await e.response.json()
                        retry_after = response_data.get('retry_after', 1)
                    except:
                        retry_after = 1 
                    print(f"Rate limited, waiting {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                else:
                    print(f"HTTP Error: {e}, retrying...")
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"Error sending message: {e}, retrying...")
                await asyncio.sleep(1)

    async def reply_loop():
        def check(m):
            return m.author == user and m.channel == ctx.channel

        while True:
            try:
                message = await bot.wait_for('message', check=check)
                asyncio.create_task(send_autoreply(message))
                await asyncio.sleep(0.1)  
            except Exception as e:
                print(f"Error in reply loop: {e}")
                await asyncio.sleep(1)
                continue

    # Start sending autoreplies to the user
    await send_autoreply(ctx.message)

    task = bot.loop.create_task(reply_loop())
    autoreply_tasks[(user.id, channel_id)] = task

@bot.command()
async def arend(ctx):
    channel_id = ctx.channel.id
    tasks_to_stop = [key for key in autoreply_tasks.keys() if key[1] == channel_id]
    
    if tasks_to_stop:
        for user_id in tasks_to_stop:
            task = autoreply_tasks.pop(user_id)
            task.cancel()
        await ctx.send("```Autoreply has been stopped.```")
    else:
        await ctx.send("```No active autoreply tasks in this channel.```")

translator = Translator()


translate_settings = {"active": False, "language": "en"}

LANGUAGE_CODES = {
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic', 'hy': 'Armenian', 'az': 'Azerbaijani',
    'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan',
    'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-cn': 'Chinese', 'zh-tw': 'Chinese (Traditional)',
    'co': 'Corsican', 'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English',
    'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish', 'fr': 'French', 'fy': 'Frisian',
    'gl': 'Galician', 'ka': 'Georgian', 'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole',
    'ha': 'Hausa', 'haw': 'Hawaiian', 'iw': 'Hebrew', 'hi': 'Hindi', 'hmn': 'Hmong', 'hu': 'Hungarian',
    'is': 'Icelandic', 'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian', 'ja': 'Japanese',
    'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer', 'rw': 'Kinyarwanda', 'ko': 'Korean',
    'ku': 'Kurdish (Kurmanji)', 'ky': 'Kyrgyz', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian',
    'lb': 'Luxembourgish', 'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese',
    'mi': 'Maori', 'mr': 'Marathi', 'mn': 'Mongolian', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian',
    'or': 'Odia (Oriya)', 'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi',
    'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic', 'sr': 'Serbian', 'st': 'Sesotho',
    'sn': 'Shona', 'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali',
    'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil', 
    'tt': 'Tatar', 'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'tk': 'Turkmen', 'uk': 'Ukrainian', 
    'ur': 'Urdu', 'ug': 'Uyghur', 'uz': 'Uzbek', 'vi': 'Vietnamese', 'cy': 'Welsh', 'xh': 'Xhosa', 
    'yi': 'Yiddish', 'yo': 'Yoruba', 'zu': 'Zulu'
}


LANGUAGE_NAMES = {name.lower(): code for code, name in LANGUAGE_CODES.items()}

@bot.command()
async def translate(ctx, language: str):
    language = language.lower()

    
    if language in LANGUAGE_CODES:
        target_language = language
    elif language in LANGUAGE_NAMES:  
        target_language = LANGUAGE_NAMES[language]
    else:
        available_langs = "\n".join([f"{code}: {name}" for code, name in LANGUAGE_CODES.items()])
        await ctx.send(f"```Invalid language. Please provide a valid language code or language name.\nAvailable languages:\n{available_langs}```")
        return
    
    translate_settings["active"] = True
    translate_settings["language"] = target_language
    await ctx.message.delete()  
    await ctx.send(f"```Translation mode activated. All your messages will be translated to {LANGUAGE_CODES[target_language]}.```")


@bot.command()
async def translateoff(ctx):
    translate_settings["active"] = False
    await ctx.message.delete()  
    await ctx.send("```Translation mode deactivated.```")

@bot.command()
async def spam(ctx, *, message: str):
    global spammingss
    spammingss = True 
    await ctx.send(f"```Starting spam of '{message}'. Use .spamoff to stop.```")

    while spammingss:  
        await ctx.send(message) 
        await asyncio.sleep(0.05)

@bot.command()
async def spamoff(ctx):
    global spammingss
    spammingss = False 
    await ctx.send("```Spamming stopped.```")
editspamming = False

mimic_user = None  

@bot.command()
async def mimic(ctx, user: discord.Member):
    global mimic_user
    mimic_user = user 
    await ctx.send(f"```Now mimicking {user.display_name}'s messages.```")


@bot.command()
async def mimicoff(ctx):
    global mimic_user
    mimic_user = None 
    await ctx.send("```Stopped mimicking messages.```")

@bot.command()
async def clearmsg(ctx, limit: int):
    
    await ctx.message.delete() 
    

    async for message in ctx.channel.history(limit=limit):
        if message.author == ctx.author:  
            try:
                await message.delete()
            except discord.HTTPException:
                print(f"Failed to delete message {message.id} due to a rate limit or permission issue.")
    

    await ctx.send(f"```Purged {limit} of your messages.```", delete_after=5)

@bot.command(aliases=['av', 'pfp'])
async def avatar(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author

    avatar_url = str(user.avatar_url_as(format='gif' if user.is_avatar_animated() else 'png'))

    await ctx.send(f"```{user.name}'s pfp```\n[Storm Selfbot V4]({avatar_url})")

@bot.command(name="banner")
async def userbanner(ctx, user: discord.User):
    headers = {
        "Authorization": bot.http.token,
        "Content-Type": "application/json"
    }
    
    url = f"https://discord.com/api/v9/users/{user.id}/profile"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            banner_hash = data.get("user", {}).get("banner")
            
            if banner_hash:
                banner_format = "gif" if banner_hash.startswith("a_") else "png"
                banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_hash}.{banner_format}?size=1024"
                await ctx.send(f"```{user.display_name}'s banner:``` [Rifat's Sb]({banner_url})")
            else:
                await ctx.send(f"{user.mention} does not have a banner set.")
        else:
            await ctx.send(f"Failed to retrieve banner: {response.status_code} - {response.text}")
    
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command()
async def createguild(ctx, *, name: str = "Storm Selfbot Server"):
    try:
        new_guild = await bot.create_guild(name=name)
        await ctx.send(f"```Server '{new_guild.name}' has been created successfully.```")
    except discord.HTTPException as e:
        await ctx.send(f"```Failed to create server: {e}```")

async def fetch_anime_gif(action):
    async with aiohttp.botSession() as session:
        async with session.get(f"https://api.waifu.pics/sfw/{action}") as r:
            if r.status == 200:
                data = await r.json()
                return data['url']  
            else:
                return None
                
@bot.command(name="kiss")
async def kiss(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to kiss!```")
        return

    gif_url = await fetch_anime_gif("kiss")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} sends an anime kiss to {member.display_name}! 💋```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime kiss GIF right now, try again later!```")
@bot.command(name="slap")
async def slap(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to slap!```")
        return

    gif_url = await fetch_anime_gif("slap")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} slaps {member.display_name}! 👋```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime slap GIF right now, try again later!```")


@bot.command(name="hurt")
async def hurt(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to kill!```")
        return

    gif_url = await fetch_anime_gif("kill")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} kills {member.display_name}! ☠```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime kill GIF right now, try again later!```")

@bot.command(name="pat")
async def pat(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to pat!```")
        return

    gif_url = await fetch_anime_gif("pat")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} pats {member.display_name}! 🖐```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime pat GIF right now, try again later!```")

@bot.command(name="wave")
async def wave(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to wave at!```")
        return

    gif_url = await fetch_anime_gif("wave")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} waves at {member.display_name}! 👋```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime wave GIF right now, try again later!```")

@bot.command(name="hug")
async def hug(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to hug!```")
        return

    gif_url = await fetch_anime_gif("hug")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} hugs {member.display_name}! 🤗```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime hug GIF right now, try again later!```")

@bot.command(name="cuddle")
async def cuddle(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to cuddle!```")
        return

    gif_url = await fetch_anime_gif("cuddle")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} cuddles {member.display_name}! 🤗```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime cuddle GIF right now, try again later!```")

@bot.command(name="lick")
async def lick(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to lick!```")
        return

    gif_url = await fetch_anime_gif("lick")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} licks {member.display_name}! 😋```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime lick GIF right now, try again later!```")

@bot.command(name="bite")
async def bite(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to bite!```")
        return

    gif_url = await fetch_anime_gif("bite")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} bites {member.display_name}! 🐍```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime bite GIF right now, try again later!```")

@bot.command(name="bully")
async def bully(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to bully!```")
        return

    gif_url = await fetch_anime_gif("bully")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} bullies {member.display_name}! 😠```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime bully GIF right now, try again later!```")

@bot.command(name="poke")
async def poke(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to poke!```")
        return

    gif_url = await fetch_anime_gif("poke")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} pokes {member.display_name}! 👉👈```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime poke GIF right now, try again later!```")


@bot.command(name="dance")
async def dance(ctx):
    gif_url = await fetch_anime_gif("dance")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} dances! 💃```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime dance GIF right now, try again later!```")

@bot.command(name="cry")
async def cry(ctx):
    gif_url = await fetch_anime_gif("cry")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} is crying! 😢```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime cry GIF right now, try again later!```")

@bot.command(name="sleep")
async def sleep(ctx):
    gif_url = await fetch_anime_gif("sleep")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} is sleeping! 😴```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime sleep GIF right now, try again later!```")

@bot.command(name="blush")
async def blush(ctx):
    gif_url = await fetch_anime_gif("blush")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} just blushed.! 😊```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime blush GIF right now, try again later!```")

@bot.command(name="wink")
async def wink(ctx):
    gif_url = await fetch_anime_gif("wink")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} winks! 😉```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime wink GIF right now, try again later!```")

@bot.command(name="smile")
async def smile(ctx):
    gif_url = await fetch_anime_gif("smile")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} smiles! 😊```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime smile GIF right now, try again later!```")


@bot.command(name="highfive")
async def highfive(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to high-five!```")
        return

    gif_url = await fetch_anime_gif("highfive")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} high-fives {member.display_name}! 🙌```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime high-five GIF right now, try again later!```")

@bot.command(name="handhold")
async def handhold(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to hold hands with!```")
        return

    gif_url = await fetch_anime_gif("handhold")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} holds hands with {member.display_name}! 🤝```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime handhold GIF right now, try again later!```")

@bot.command(name="nom")
async def nom(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to nom!```")
        return

    gif_url = await fetch_anime_gif("nom")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} noms on {member.display_name}! 😋```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime nom GIF right now, try again later!```")

@bot.command(name="smug")
async def smug(ctx):
    gif_url = await fetch_anime_gif("smug")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} has a smug look! 😏```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime smug GIF right now, try again later!```")

@bot.command(name="bonk")
async def bonk(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to bonk!```")
        return

    gif_url = await fetch_anime_gif("bonk")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} bonks {member.display_name}! 🤭```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime bonk GIF right now, try again later!```")

@bot.command(name="yeet")
async def yeet(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("```You need to mention someone to yeet!```")
        return

    gif_url = await fetch_anime_gif("yeet")

    if gif_url:
        await ctx.send(f"```{ctx.author.display_name} yeets {member.display_name}! 💨```\n[Rifat's Selfbot]({gif_url})")
    else:
        await ctx.send("```Couldn't fetch an anime yeet GIF right now, try again later!```")

@bot.command(name="ero")
async def ero(ctx, member: discord.Member = None):
    async with aiohttp.botSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=ero&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares some ero content```\n[Rifat's Selfbot]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later```")

@bot.command(name="ecchi")
async def ecchi(ctx, member: discord.Member = None):
    
    async with aiohttp.botSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=ecchi&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares some ecchi```\n[Rifat's Selfbot]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="hentai")
async def hentai(ctx, member: discord.Member = None):
    
    async with aiohttp.botSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=hentai&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares some hentai```\n[Rifat's Selfbot]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="uniform")
async def uniform(ctx, member: discord.Member = None):
    async with aiohttp.botSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=uniform&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares some uniform content```\n[Rifat's Selfbot]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="maid")
async def maid(ctx, member: discord.Member = None):
    async with aiohttp.botSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=maid&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares some maid content```\n[Rifat's Selfbot]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="oppai")
async def oppai(ctx, member: discord.Member = None):
    async with aiohttp.botSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=oppai&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares some oppai content```\n[Rifat's Selfbot]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="selfies")
async def selfies(ctx, member: discord.Member = None):
    async with aiohttp.botSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=selfies&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares some selfies```\n[Rifat's Selfbot]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="raiden")
async def raiden(ctx, member: discord.Member = None):
    async with aiohttp.botSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=raiden-shogun&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares Raiden content```\n[Rifat's Selfbot]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command(name="marin")
async def marin(ctx, member: discord.Member = None):
    async with aiohttp.botSession() as session:
        async with session.get('https://api.waifu.im/search/?included_tags=marin-kitagawa&is_nsfw=true') as response:
            if response.status == 200:
                data = await response.json()
                image_url = data['images'][0]['url']
                await ctx.send(f"```{ctx.author.display_name} shares Marin content```\n[Rifat's Selfbot]({image_url})")
            else:
                await ctx.send("```Failed to fetch image, try again later!```")

@bot.command()
async def firstmessage(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel  
    try:

        first_message = await channel.history(limit=1, oldest_first=True).flatten()
        if first_message:
            msg = first_message[0]  
            response = f"here."

            await msg.reply(response)  
        else:
            await ctx.send("```No messages found in this channel.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

@bot.command()
async def leavegroups(ctx):
    left_count = 0
    for channel in ctx.bot.private_channels:
        if isinstance(channel, discord.GroupChannel):
            try:
                await channel.leave()
                left_count += 1
            except discord.HTTPException as e:
                await ctx.send(f"Failed to leave group {channel.name}: {e}")

    if left_count > 0:
        await ctx.send(f"Successfully left {left_count} groups.")
    else:
        await ctx.send("No groups found to leave.")

ping_responses = {}

@bot.command()
async def pingresponse(ctx, action: str, *, response: str = None):
    global ping_responses
    action = action.lower()

    if action == "toggle":
        if ctx.channel.id in ping_responses:
            del ping_responses[ctx.channel.id]
            await ctx.send("```Ping response disabled for this channel.```")
        else:
            if response:
                ping_responses[ctx.channel.id] = response
                await ctx.send(f"```Ping response set to: {response}```")
            else:
                await ctx.send("```Please provide a response to set for pings.```")
    
    elif action == "list":
        if ctx.channel.id in ping_responses:
            await ctx.send(f"```Current ping response: {ping_responses[ctx.channel.id]}```")
        else:
            await ctx.send("```No custom ping response set for this channel.```")
    
    elif action == "clear":
        if ctx.channel.id in ping_responses:
            del ping_responses[ctx.channel.id]
            await ctx.send("```Ping response cleared for this channel.```")
        else:
            await ctx.send("```No custom ping response to clear for this channel.```")
    
    else:
        await ctx.send("```Invalid action. Use toggle, list, or clear.```")


insults_enabled = False  
autoinsults = [
    "your a skid",
    "stfu",
    "your such a loser",
    "fuck up boy",
    "no.",
    "why are you a bitch",
    "nigga you stink",
    "idk you",
    "LOLSSOL WHO ARE YOUa",
    "stop pinging me boy",
    "if your black stfu"
    
]

@bot.command(name="pinginsult")
async def pinginsult(ctx, action: str = None, *, insult: str = None):
    global insults_enabled

    if action is None:
        await ctx.send("```You need to specify an action: toggle, list, or clear.```")
        return

    if action.lower() == "toggle":
        insults_enabled = not insults_enabled  
        status = "enabled" if insults_enabled else "disabled"
        await ctx.send(f"```Ping insults are now {status}!```")

    elif action.lower() == "list":
        if autoinsults:
            insult_list = "\n".join(f"- {insult}" for insult in autoinsults)
            await ctx.send(f"```Current ping insults:\n{insult_list}```")
        else:
            await ctx.send("```No insults found in the list.```")

    elif action.lower() == "clear":
        autoinsults.clear()
        await ctx.send("```Ping insults cleared!```")

    else:
        await ctx.send("```Invalid action. Use toggle, list, or clear.```")

reactions_enabled = False  
custom_reaction = "😜"  
@bot.command(name="pingreact")
async def pingreact(ctx, action: str = None, reaction: str = None):
    global reactions_enabled, custom_reaction

    if action is None:
        await ctx.send("```You need to specify an action: toggle, list, clear, or set.```")
        return

    if action.lower() == "toggle":

        if reaction:
            custom_reaction = reaction  
            reactions_enabled = not reactions_enabled  
            status = "enabled" if reactions_enabled else "disabled"
            await ctx.send(f"```Ping reactions {status}! Custom reaction set to: {custom_reaction}```")
        else:
            reactions_enabled = not reactions_enabled  
            status = "enabled" if reactions_enabled else "disabled"
            await ctx.send(f"```Ping reactions {status}!```")

    elif action.lower() == "list":
        if reactions_enabled:
            await ctx.send(f"```Ping reactions are currently enabled. Current reaction: {custom_reaction}```")
        else:
            await ctx.send("```Ping reactions are currently disabled.```")

    elif action.lower() == "clear":
        reactions_enabled = False  
        await ctx.send("```Ping reactions cleared!```")

    else:
        await ctx.send("```Invalid action. Use toggle, list, or clear.```")

fake_activity_active = False
tokenss = []  
async def read_tokens():
    try:
        with open('token.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

async def send_fake_reply(token, channel_id, message, response, delay):
    await asyncio.sleep(delay)  

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://discord.com/api/v9/channels/{channel_id}/typing', headers=headers):
            await asyncio.sleep(random.uniform(2, 5))  

        payload = {
            'content': message
        }
        
        async with session.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers, json=payload) as resp:
            if resp.status == 200:
                print(f"Message sent successfully with token: {token[-4:]}")
                
                sent_message_data = await resp.json()
                sent_message_id = sent_message_data['id']


                await asyncio.sleep(3)  
                
                async with session.post(f'https://discord.com/api/v9/channels/{channel_id}/typing', headers=headers):
                    await asyncio.sleep(random.uniform(2, 5))  

                response_token = random.choice([t for t in tokens if t != token])  


                await asyncio.sleep(random.uniform(2, 5)) 
                response_payload = {
                    'content': response,
                    'message_reference': {
                        'message_id': sent_message_id
                    }
                }
                
                async with session.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers={'Authorization': response_token, 'Content-Type': 'application/json'}, json=response_payload) as resp:
                    if resp.status == 200:
                        print(f"Response sent successfully with token: {response_token[-4:]}")
                    elif resp.status == 429:
                        retry_after = int(resp.headers.get("Retry-After", 1))
                        print(f"Rate limited on response with token: {response_token[-4:]}. Retrying after {retry_after} seconds...")
                        await asyncio.sleep(retry_after)
                    else:
                        print(f"Failed to send response with token: {response_token[-4:]}. Status code: {resp.status}")
            elif resp.status == 429:
                retry_after = int(resp.headers.get("Retry-After", 1))
                print(f"Rate limited on send with token: {token[-4:]}. Retrying after {retry_after} seconds...")
                await asyncio.sleep(retry_after)
            else:
                print(f"Failed to send message with token: {token[-4:]}. Status code: {resp.status}")

@bot.command(name='fakeactive')
async def fake_active(ctx):
    global fake_activity_active
    fake_activity_active = True  
    global tokenss 
    tokenss = await read_tokens() 
    await ctx.send("```Starting Fake Activity```")
    
    if not tokenss:
        await ctx.send("No tokens found in token.txt.")
        return

    channel = ctx.channel

    for index, (message, response) in enumerate(conversation_flow):
        token = tokenss[index % len(tokenss)] 
        
        delay = index * 1 + random.randint(1, 1)  
        asyncio.create_task(send_fake_reply(token, channel.id, message, response, delay))

@bot.command(name='fakeactiveoff')
async def fake_active_off(ctx):
    global fake_activity_active
    fake_activity_active = False 
    await ctx.send("```Fake Activity Stopped```")

countdown_active = False
@bot.command(name="countdown")
async def countdown(ctx, member: discord.Member, count: int):
    global countdown_active
    countdown_active = True  

    count = abs(count)

    for i in range(count, 0, -1):
        if not countdown_active:
            break

        countdown_message = f"{member.mention} **{i}**"

        await ctx.send(countdown_message)

        await asyncio.sleep(1)

    if countdown_active:
        await ctx.send(f"```ountdown complete.```")

countdown_active = False  


@bot.command(name="countdownoff")
async def countdownoff(ctx):
    global countdown_active
    countdown_active = False
    await ctx.send(f"```the countdown has been stopped.```")

@bot.command()
async def setbio(ctx, *, bio_text: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": bot.http.token
    }

    new_bio = {
        "bio": bio_text
    }

    url_api_info = "https://discord.com/api/v9/users/%40me/profile"
    
    try:
        response = requests.patch(url_api_info, headers=headers, json=new_bio)

        if response.status_code == 200:
            await ctx.send("```Bio updated successfully!```")
        else:
            await ctx.send(f"```Failed to update bio: {response.status_code} - {response.json()}```")

    except Exception as e:
        await ctx.send(f"```An error occurred: {e}```")

@bot.command()
async def stealbio(ctx, member: discord.User):
    url = f"https://discord.com/api/v9/users/{member.id}/profile?with_mutual_guilds=true&with_mutual_friends=true"
    headers = {
        "Authorization": bot.http.token
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200:
            target_bio = data.get("user", {}).get("bio", None)

            if target_bio:
                set_bio_url = "https://discord.com/api/v9/users/@me/profile"
                new_bio = {"bio": target_bio}

                update_response = requests.patch(set_bio_url, headers=headers, json=new_bio)

                if update_response.status_code == 200:
                    await ctx.send("```Bio updated!```")
                else:
                    await ctx.send(f"```Failed: {update_response.status_code} - {update_response.json()}```")
            else:
                await ctx.send("```user does not have a bio to copy.```")
        else:
            await ctx.send(f"```Failed: {response.status_code} - {data}```")

    except Exception as e:
        await ctx.send(f"```{e}```")



@bot.command()
async def stealpronoun(ctx, member: discord.User):
    url = f"https://discord.com/api/v9/users/{member.id}/profile?with_mutual_guilds=true&with_mutual_friends=true"
    headers = {
        "Authorization": bot.http.token
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200:
            target_pronouns = data.get("user_profile", {}).get("pronouns", None)

            if target_pronouns:
                set_pronoun_url = "https://discord.com/api/v9/users/%40me/profile"
                new_pronoun = {"pronouns": target_pronouns}

                update_response = requests.patch(set_pronoun_url, headers=headers, json=new_pronoun)

                if update_response.status_code == 200:
                    await ctx.send("```Pronouns stolen successful.```")
                else:
                    await ctx.send(f"```Failed: {update_response.status_code} - {update_response.json()}```")
            else:
                await ctx.send("```user does not have pronouns set to copy.```")
        else:
            await ctx.send(f"```Failed: {response.status_code} - {data}```")

    except Exception as e:
        await ctx.send(f"```{e}```")


ladder_messages = [
    "frail bitch LOL",
    "this nigga is disgusting",
    "tired yet?",
    "yo {username} i can go all day LMFAO",
    "# DONT DOZZ OFF RETARD",
    " 'nice autopaster'🤡 ",
    "did i break your ego yet?",
    "YO {username} YOUR MY BITCH LOL",
    "# DONT GET DROWNED PUSSY",
    "LETS GO FOR HOURS RETARD",
    "nigga we dont fwu?",
    "disgusting fucking slut",
    "# DONT SLIT YOUR WRISTS NOW",
    "faggot loser",
    "come die",
    "ILL RIP YOUR FUCKING JAW OUT",
    "# LOOOOOOOOOOOOL",
    "{username} icl your a bitch",
    "insecure fuck LOL",
    "this nigga was caught using a voice changer",
    "dont stumble when i talk to you",
    "# SPEAK UP FUCKING FAGGOT",
    "soybean smelly ass nigga",
    "whatever you claimK",
    "# LOOOOL DIE IN /ROSTER FAGGOT",
    "COME MEET YOUR MATCH RETARD",
    "BREAK UNDER THE PRESSURE",
    "fat indian ass nigga tryba step?",
    "convert this sluts language to english",
    "# LMAOOOOOOO",
    "{username}",
    "nigga ur ass"
]




status_rotation_active = False
emoji_rotation_active = False
current_status = ""
current_emoji = ""

@bot.command(name='rstatus')
async def rotate_status(ctx, *, statuses: str):
    global status_rotation_active, current_status, current_emoji
    await ctx.message.delete()
    
    status_list = [s.strip() for s in statuses.split(',')]
    
    if not status_list:
        await ctx.send("```Please separate statuses by commas.```", delete_after=3)
        return
    
    current_index = 0
    status_rotation_active = True
    
    async def update_status_emoji():
        json_data = {
            'custom_status': {
                'text': current_status,
                'emoji_name': current_emoji
            }
        }

        custom_emoji_match = re.match(r'<a?:(\w+):(\d+)>', current_emoji)
        if custom_emoji_match:
            name, emoji_id = custom_emoji_match.groups()
            json_data['custom_status']['emoji_name'] = name
            json_data['custom_status']['emoji_id'] = emoji_id
        else:
            json_data['custom_status']['emoji_name'] = current_emoji

        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/settings',
                    headers={'Authorization': bot.http.token, 'Content-Type': 'application/json'},
                    json=json_data
                ) as resp:
                    await resp.read()
            finally:
                await session.close()

    await ctx.send(f"```Status rotation started```")
    
    try:
        while status_rotation_active:
            current_status = status_list[current_index]
            await update_status_emoji()
            await asyncio.sleep(8)
            current_index = (current_index + 1) % len(status_list)
                
    finally:
        current_status = ""
        await update_status_emoji()
        status_rotation_active = False

@bot.command(name='remoji')
async def rotate_emoji(ctx, *, emojis: str):
    global emoji_rotation_active, current_emoji, status_rotation_active
    await ctx.message.delete()
    

    emoji_list = emojis.split()
    
    if not emoji_list:
        await ctx.send("```Please provide emojis separated by spaces.```", delete_after=3)
        return
    
    current_index = 0
    emoji_rotation_active = True
    
    async def update_status_emoji():
        json_data = {
            'custom_status': {
                'text': current_status,
                'emoji_name': current_emoji
            }
        }
        
        custom_emoji_match = re.match(r'<a?:(\w+):(\d+)>', current_emoji)
        if custom_emoji_match:
            name, emoji_id = custom_emoji_match.groups()
            json_data['custom_status']['emoji_name'] = name
            json_data['custom_status']['emoji_id'] = emoji_id
        else:
            json_data['custom_status']['emoji_name'] = current_emoji

        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/settings',
                    headers={'Authorization': bot.http.token, 'Content-Type': 'application/json'},
                    json=json_data
                ) as resp:
                    await resp.read()
            finally:
                await session.close()

    await ctx.send(f"```Emoji rotation started```")
    
    try:
        while emoji_rotation_active:
            current_emoji = emoji_list[current_index]
            await update_status_emoji()
            await asyncio.sleep(8)
            current_index = (current_index + 1) % len(emoji_list)
                
    finally:
        current_emoji = ""
        await update_status_emoji()
        emoji_rotation_active = False

@bot.command(name='stopstatus')
async def stop_rotate_status(ctx):
    global status_rotation_active
    status_rotation_active = False
    await ctx.send("```Status rotation stopped.```", delete_after=3)

@bot.command(name='stopemoji')
async def stop_rotate_emoji(ctx):
    global emoji_rotation_active
    emoji_rotation_active = False
    await ctx.send("```Emoji rotation stopped.```", delete_after=3)


def loads_tokens(file_path='token.txt'):
    with open(file_path, 'r') as file:
        tokens = file.readlines()
    return [token.strip() for token in tokens if token.strip()]

@bot.command()
async def tnickname(ctx, server_id: str, *, name: str = None):
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    status_msg = await ctx.send(f"""```ansi
Token Nickname Changer
Total tokens available: {total_tokens}
How many tokens do you want to use? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            try:
                num = int(amount)
                if num > total_tokens:
                    await status_msg.edit(content="```Not enough tokens available```")
                    return
                selected_tokens = random.sample(tokens, num)
            except ValueError:
                await status_msg.edit(content="```Invalid number```")
                return

        if name is None:
            await status_msg.edit(content=f"""```ansi
Choose nickname mode:
1. Random (generates unique names)
2. List (uses names from tnickname.txt)```""")
            
            mode_msg = await bot.wait_for('message', timeout=30.0, check=check)
            mode = mode_msg.content
            
            if mode == "1":
                names = [''.join(random.choices(string.ascii_letters, k=8)) for _ in range(len(selected_tokens))]
            elif mode == "2":
                try:
                    with open('tnickname.txt', 'r') as f:
                        name_list = [line.strip() for line in f if line.strip()]
                        names = random.choices(name_list, k=len(selected_tokens))
                except FileNotFoundError:
                    await status_msg.edit(content="```tnickname.txt not found```")
                    return
            else:
                await status_msg.edit(content="```Invalid mode selected```")
                return
        else:
            names = [name] * len(selected_tokens)

        success = 0
        headers = {'Authorization': '', 'Content-Type': 'application/json'}
        
        async with aiohttp.ClientSession() as session:
            for i, (token, nickname) in enumerate(zip(selected_tokens, names), 1):
                headers['Authorization'] = token
                async with session.patch(
                    f'https://discord.com/api/v9/guilds/{server_id}/members/@me/nick',
                    headers=headers,
                    json={'nick': nickname}
                ) as resp:
                    if resp.status == 200:
                        success += 1
                    
                    progress = f"""```ansi
Changing Nicknames...
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}
Current name: {nickname}```"""
                    await status_msg.edit(content=progress)
                    await asyncio.sleep(0.5)

        final_msg = f"""```ansi
Nickname Change Complete
Successfully changed: {success}/{len(selected_tokens)} nicknames```"""
        await status_msg.edit(content=final_msg)

    except asyncio.TimeoutError:
        await status_msg.edit(content="```Command timed out```")

@bot.command()
async def tpronouns(ctx, *, pronouns: str = None):
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    

    status_msg = await ctx.send(f"""```ansi\n
Token Pronoun Changer
Total tokens available: {total_tokens}

How many tokens do you want to use? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            num = int(amount)
            if num > total_tokens:

                await status_msg.edit(content="```NOT enough tokens available```")
                return
            selected_tokens = random.sample(tokens, num)

        if pronouns is None:
            pronoun_list = ['he/him', 'she/her', 'they/them', 'it/its', 'xe/xem', 'ze/zir']
            pronouns = random.choices(pronoun_list, k=len(selected_tokens))
        else:
            pronouns = [pronouns] * len(selected_tokens)

        success = 0
        headers = {'Authorization': '', 'Content-Type': 'application/json'}
        
        async with aiohttp.ClientSession() as session:
            for i, (token, pronoun) in enumerate(zip(selected_tokens, pronouns), 1):
                headers['Authorization'] = token
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/profile',
                    headers=headers,
                    json={'pronouns': pronoun}
                ) as resp:
                    if resp.status == 200:
                        success += 1
                    

                    progress = f"""```ansi\n
Changing Pronouns...
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}

Current pronouns: {pronoun}```"""
                    await status_msg.edit(content=progress)
                    await asyncio.sleep(0.5)


        await status_msg.edit(content=f"""```ansi\n
Pronoun Change Complete

Successfully changed: {success}/{len(selected_tokens)} pronouns```
""")
    except asyncio.TimeoutError:
        await status_msg.edit(content=" timed out")
    except Exception as e:
        await status_msg.edit(content=f" error occurred: {str(e)}")
@bot.command()
async def tbio(ctx, *, bio: str = None):
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    status_msg = await ctx.send(f"""```ansi
Token Bio Changer
Total tokens available: {total_tokens}
How many tokens do you want to use? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            num = int(amount)
            if num > total_tokens:
                await status_msg.edit(content="```Not enough tokens available```")
                return
            selected_tokens = random.sample(tokens, num)

        if bio is None:
            await status_msg.edit(content=f"""```ansi
Choose bio mode:
1. {yellow}Random (generates random bios)
2. List (uses bios from tbio.txt)```""")
            
            mode_msg = await bot.wait_for('message', timeout=30.0, check=check)
            mode = mode_msg.content
            
            if mode == "1":
                bios = [f"Bio #{i} | " + ''.join(random.choices(string.ascii_letters + string.digits, k=20)) for i in range(len(selected_tokens))]
            elif mode == "2":
                try:
                    with open('tbio.txt', 'r') as f:
                        bio_list = [line.strip() for line in f if line.strip()]
                        bios = random.choices(bio_list, k=len(selected_tokens))
                except FileNotFoundError:
                    await status_msg.edit(content="```tbio.txt not found```")
                    return
        else:
            bios = [bio] * len(selected_tokens)

        success = 0
        headers = {'Authorization': '', 'Content-Type': 'application/json'}
        
        async with aiohttp.ClientSession() as session:
            for i, (token, bio_text) in enumerate(zip(selected_tokens, bios), 1):
                headers['Authorization'] = token
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/profile',
                    headers=headers,
                    json={'bio': bio_text}
                ) as resp:
                    if resp.status == 200:
                        success += 1
                    
                    progress = f"""```ansi
Changing Bios...
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}
Current bio: {bio_text[:50]}{'...' if len(bio_text) > 50 else ''}```"""
                    await status_msg.edit(content=progress)
                    await asyncio.sleep(0.5)

        await status_msg.edit(content=f"""```ansi
Bio Change Complete
Successfully changed: {success}/{len(selected_tokens)} bios```""")

    except asyncio.TimeoutError:
        await status_msg.edit(content="```Command timed out```")


@bot.command()
async def tpfp(ctx, url: str = None):
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    status_msg = await ctx.send(f"""```ansi
\u001b[0;36mToken PFP Changer\u001b[0m
Total tokens available: {total_tokens}
How many tokens do you want to use? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            try:
                num = int(amount)
                if num > total_tokens:
                    await status_msg.edit(content="```Not enough tokens available```")
                    return
                selected_tokens = random.sample(tokens, num)
            except ValueError:
                await status_msg.edit(content="```Invalid number```")
                return

        if url is None:
            await status_msg.edit(content="```Please provide an image URL```")
            return

        success = 0
        failed = 0
        ratelimited = 0
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as img_response:
                if img_response.status != 200:
                    await status_msg.edit(content="```Failed to fetch image```")
                    return
                image_data = await img_response.read()
                image_b64 = base64.b64encode(image_data).decode()
                
                content_type = img_response.headers.get('Content-Type', '')
                if 'gif' in content_type.lower():
                    image_format = 'gif'
                else:
                    image_format = 'png'

            for i, token in enumerate(selected_tokens, 1):
                headers = {
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br, zstd',
                    'accept-language': 'en-US,en;q=0.7',
                    'authorization': token,
                    'content-type': 'application/json',
                    'origin': 'https://discord.com',
                    'referer': 'https://discord.com/channels/@me',
                    'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'sec-gpc': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                    'x-debug-options': 'bugReporterEnabled',
                    'x-discord-locale': 'en-US',
                    'x-discord-timezone': 'America/New_York',
                    'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzMS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTMxLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL3NlYXJjaC5icmF2ZS5jb20vIiwicmVmZXJyaW5nX2RvbWFpbiI6InNlYXJjaC5icmF2ZS5jb20iLCJyZWZlcnJlcl9jdXJyZW50IjoiaHR0cHM6Ly9kaXNjb3JkLmNvbS8iLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiJkaXNjb3JkLmNvbSIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjM0NzY5OSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
                }

                
                payload = {
                    "avatar": f"data:image/{image_format};base64,{image_b64}"
                }
                
                try:
                    async with session.get(
                        'https://discord.com/api/v9/users/@me',
                        headers=headers
                    ) as verify_resp:
                        if verify_resp.status != 200:
                            failed += 1
                            print(f"Invalid token {i}")
                            continue

                    async with session.patch(
                        'https://discord.com/api/v9/users/@me',
                        headers=headers,
                        json=payload
                    ) as resp:
                        response_data = await resp.json()
                        
                        if resp.status == 200:
                            success += 1
                        elif "captcha_key" in response_data:
                            failed += 1
                            print(f"Captcha required for token {i}")
                        elif "AVATAR_RATE_LIMIT" in str(response_data):
                            ratelimited += 1
                            print(f"Rate limited for token {i}, waiting 30 seconds")
                            await asyncio.sleep(30)  
                            i -= 1  
                            continue
                        else:
                            failed += 1
                            print(f"Failed to update token {i}: {response_data}")
                        
                        progress = f"""```ansi
\u001b[0;36mChanging Profile Pictures...\u001b[0m
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}
Failed: {failed}
Rate Limited: {ratelimited}```"""
                        await status_msg.edit(content=progress)
                        await asyncio.sleep(2)  
                        
                except Exception as e:
                    failed += 1
                    print(f"Error with token {i}: {str(e)}")
                    continue

        await status_msg.edit(content=f"""```ansi
\u001b[0;32mProfile Picture Change Complete\u001b[0m
Successfully changed: {success}/{len(selected_tokens)} avatars
Failed: {failed}
Rate Limited: {ratelimited}```""")

    except asyncio.TimeoutError:
        await status_msg.edit(content="```Command timed out```")
    except Exception as e:
        await status_msg.edit(content=f"```An error occurred: {str(e)}```")

@bot.command()
async def tstatus(ctx, *, status_text: str = None):
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    if not status_text:
        await ctx.send("```Please provide a status text```")
        return

    status_msg = await ctx.send(f"""```ansi
\u001b[0;36mToken Status Changer\u001b[0m
Total tokens available: {total_tokens}
How many tokens do you want to use? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            try:
                num = int(amount)
                if num > total_tokens:
                    await status_msg.edit(content="```Not enough tokens available```")
                    return
                selected_tokens = random.sample(tokens, num)
            except ValueError:
                await status_msg.edit(content="```Invalid number```")
                return

        success = 0
        
        async with aiohttp.ClientSession() as session:
            for i, token in enumerate(selected_tokens, 1):
                online_data = {
                    'status': 'online'
                }
                
                status_data = {
                    'custom_status': {
                        'text': status_text
                    },
                    'status': 'online'  
                }
                
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/settings',
                    headers={
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    },
                    json=online_data
                ) as resp1:
                    
                    async with session.patch(
                        'https://discord.com/api/v9/users/@me/settings',
                        headers={
                            'Authorization': token,
                            'Content-Type': 'application/json'
                        },
                        json=status_data
                    ) as resp2:
                        if resp1.status == 200 and resp2.status == 200:
                            success += 1
                        
                        progress = f"""```ansi
\u001b[0;36mChanging Statuses...\u001b[0m
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}
Current status: {status_text}```"""
                        await status_msg.edit(content=progress)
                        await asyncio.sleep(0.5)

        await status_msg.edit(content=f"""```ansi
\u001b[0;32mStatus Change Complete\u001b[0m
Successfully changed: {success}/{len(selected_tokens)} statuses to: {status_text}```""")

    except asyncio.TimeoutError:
        await status_msg.edit(content="```Command timed out```")
    except Exception as e:
        await status_msg.edit(content=f"```An error occurred: {str(e)}```")

@bot.command()
async def tstatusoff(ctx):
    tokens = loads_tokens()
    total_tokens = len(tokens)
    
    status_msg = await ctx.send(f"""```ansi
\u001b[0;36mToken Status Reset\u001b[0m
Total tokens available: {total_tokens}
How many tokens do you want to reset? (Type 'all' or enter a number)```""")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        amount_msg = await bot.wait_for('message', timeout=20.0, check=check)
        amount = amount_msg.content.lower()
        
        if amount == 'all':
            selected_tokens = tokens
        else:
            try:
                num = int(amount)
                if num > total_tokens:
                    await status_msg.edit(content="```Not enough tokens available```")
                    return
                selected_tokens = random.sample(tokens, num)
            except ValueError:
                await status_msg.edit(content="```Invalid number```")
                return

        success = 0
        
        async with aiohttp.ClientSession() as session:
            for i, token in enumerate(selected_tokens, 1):

                reset_data = {
                    'custom_status': None,
                    'status': 'online' 
                }
                
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/settings',
                    headers={
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    },
                    json=reset_data
                ) as resp:
                    if resp.status == 200:
                        success += 1
                    
                    progress = f"""```ansi
\u001b[0;36mResetting Statuses...\u001b[0m
Progress: {i}/{len(selected_tokens)} ({(i/len(selected_tokens)*100):.1f}%)
Success: {success}```"""
                    await status_msg.edit(content=progress)
                    await asyncio.sleep(0.5)

        await status_msg.edit(content=f"""```ansi
\u001b[0;32mStatus Reset Complete\u001b[0m
Successfully reset: {success}/{len(selected_tokens)} statuses```""")

    except asyncio.TimeoutError:
        await status_msg.edit(content="```Command timed out```")
    except Exception as e:
        await status_msg.edit(content=f"```An error occurred: {str(e)}```")

@bot.command()
async def tinfo(ctx, token_input: str):
    """Get token account information"""
    tokens = loads_tokens()
    
    try:
        index = int(token_input) - 1
        if 0 <= index < len(tokens):
            token = tokens[index]
        else:
            await ctx.send("```Invalid token number```")
            return
    except ValueError:
        token = token_input
        if token not in tokens:
            await ctx.send("```Invalid token```")
            return

    status_msg = await ctx.send("```Fetching token information...```")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://discord.com/api/v9/users/@me',
                headers={
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }
            ) as resp:
                if resp.status != 200:
                    await status_msg.edit(content="```Failed to fetch token information```")
                    return
                
                user_data = await resp.json()
                
                async with session.get(
                    'https://discord.com/api/v9/users/@me/connections',
                    headers={
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    }
                ) as conn_resp:
                    connections = await conn_resp.json() if conn_resp.status == 200 else []

                async with session.get(
                    'https://discord.com/api/v9/users/@me/guilds',
                    headers={
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    }
                ) as guild_resp:
                    guilds = await guild_resp.json() if guild_resp.status == 200 else []

                created_at = datetime.fromtimestamp(((int(user_data['id']) >> 22) + 1420070400000) / 1000)
                created_date = created_at.strftime('%Y-%m-%d %H:%M:%S')

                info = f"""```ansi

                                \u001b[0;36mToken Account Information\u001b[0m

                                \u001b[0;33mBasic Information:\u001b[0m
                                Username: {user_data['username']}#{user_data['discriminator']}
                                ID: {user_data['id']}
                                Email: {user_data.get('email', 'Not available')}
                                Phone: {user_data.get('phone', 'Not available')}
                                Created: {created_date}
                                Verified: {user_data.get('verified', False)}
                                MFA Enabled: {user_data.get('mfa_enabled', False)}

                                \u001b[0;33mNitro Status:\u001b[0m
                                Premium: {bool(user_data.get('premium_type', 0))}
                                Type: {['None', 'Classic', 'Full'][user_data.get('premium_type', 0)]}

                                \u001b[0;33mStats:\u001b[0m
                                Servers: {len(guilds)}
                                Connections: {len(connections)}

                                \u001b[0;33mProfile:\u001b[0m
                                Bio: {user_data.get('bio', 'No bio set')}
                                Banner: {'Yes' if user_data.get('banner') else 'No'}
                                Avatar: {'Yes' if user_data.get('avatar') else 'Default'}


```"""

                await status_msg.edit(content=info)

    except Exception as e:
        await status_msg.edit(content=f"```An error occurred: {str(e)}```")

@bot.group(invoke_without_command=True)
async def autopress(ctx, user: discord.Member = None):
    if ctx.invoked_subcommand is None:
        if not user:
            await ctx.send("```Please mention a user```")
            return
            
        user_id = str(ctx.author.id)
        if user_id not in autopress_messages or not autopress_messages[user_id]:
            await ctx.send("```No messages configured. Use .autopress add <message> to add messages```")
            return
            
        autopress_status[ctx.author.id] = {
            'running': True,
            'target': user
        }
        
        used_messages = set()
        messages_sent = 0
        
        print(f"\n=== Starting Autopress Command ===")
        print(f"Target User: {user.name}")
        
        async def send_message_group():
            nonlocal used_messages, messages_sent
            
            available_messages = [msg for msg in autopress_messages[user_id] if msg not in used_messages]
            if not available_messages:
                used_messages.clear()
                available_messages = autopress_messages[user_id]
                print("\n=== Refreshing message list ===\n")
            
            message = random.choice(available_messages)
            used_messages.add(message)
            
            try:
                full_message = f"{user.mention} {message.replace('{username}', user.display_name)}"
                await ctx.channel.send(full_message)
                messages_sent += 1
                print(f"Message sent ({messages_sent}): {message}")
                
            except Exception as e:
                print(f"\nError sending message: {str(e)}")
        
        try:
            while ctx.author.id in autopress_status and autopress_status[ctx.author.id]['running']:
                await send_message_group()
                await asyncio.sleep(random.uniform(0.5, 3.5))
        finally:
            if ctx.author.id in autopress_status:
                del autopress_status[ctx.author.id]
        
        print("\n=== Autopress Stopped ===\n")

@autopress.command(name="add")
async def add_message(ctx, *, message: str):
    user_id = str(ctx.author.id)
    if user_id not in autopress_messages:
        autopress_messages[user_id] = []
    
    autopress_messages[user_id].append(message)
    await ctx.send(f"```Added message: {message}```")
    save_messages()

@autopress.command(name="remove") 
async def remove_message(ctx, index: int):
    user_id = str(ctx.author.id)
    if user_id not in autopress_messages or not autopress_messages[user_id]:
        await ctx.send("```No messages configured```")
        return
        
    if 1 <= index <= len(autopress_messages[user_id]):
        removed = autopress_messages[user_id].pop(index-1)
        await ctx.send(f"```Removed message: {removed}```")
        save_messages()
    else:
        await ctx.send(f"```Invalid index. Use .autopress list to see message indices```")

@autopress.command(name="list")
async def list_messages(ctx):
    user_id = str(ctx.author.id)
    if user_id not in autopress_messages or not autopress_messages[user_id]:
        await ctx.send("```No messages configured```")
        return
        
    message_list = "\n".join(f"{i+1}. {msg}" for i, msg in enumerate(autopress_messages[user_id]))
    await ctx.send(f"```Your configured messages:\n\n{message_list}```")

@autopress.command(name="clear")
async def clear_messages(ctx):
    user_id = str(ctx.author.id)
    if user_id in autopress_messages:
        autopress_messages[user_id] = []
        await ctx.send("```Cleared all messages```")
        save_messages()
    else:
        await ctx.send("```No messages configured```")

@autopress.command(name="stop")
async def stop_autopress(ctx):
    if ctx.author.id in autopress_status:
        del autopress_status[ctx.author.id]
        await ctx.send("```Stopped autopress```")
    else:
        await ctx.send("```Autopress is not running```")

def save_messages():
    with open('autopress_config.json', 'w') as f:
        json.dump(autopress_messages, f)

def load_messages():
    global autopress_messages
    try:
        with open('autopress_config.json', 'r') as f:
            autopress_messages = json.load(f)
    except FileNotFoundError:
        autopress_messages = {}

@bot.group(invoke_without_command=True)
async def autokill(ctx, user: discord.Member = None):
    if ctx.invoked_subcommand is None:
        if not user:
            await ctx.send("```Please mention a user```")
            return
            
        user_id = str(ctx.author.id)
        if user_id not in autokill_messages or not autokill_messages[user_id]:
            await ctx.send("```No messages configured. Use .autokill add <message> to add messages```")
            return
            
        autokill_status[ctx.author.id] = {
            'running': True,
            'target': user
        }
        
        used_messages = set()
        messages_sent = 0
        
        print(f"\n=== Starting Autokill Command ===")
        print(f"Target User: {user.name}")
        
        async def send_message_group(channel):
            nonlocal used_messages, messages_sent
            
            available_messages = [msg for msg in autokill_messages[user_id] if msg not in used_messages]
            if not available_messages:
                used_messages.clear()
                available_messages = autokill_messages[user_id]
                print("\n=== Refreshing message list ===\n")
            
            message = random.choice(available_messages)
            used_messages.add(message)
            
            try:
                full_message = f"{user.mention} {message.replace('{username}', user.display_name)}"
                await channel.send(full_message)
                messages_sent += 1
                print(f"Message sent ({messages_sent}): {message}")
                
            except Exception as e:
                print(f"\nError sending message: {str(e)}")
        
        try:
            while (ctx.author.id in autokill_status and 
                autokill_status[ctx.author.id]['running']):
                
                available_channels = []
                
                for channel in ctx.guild.text_channels:
                    if channel.permissions_for(ctx.guild.me).send_messages:
                        available_channels.append(channel)
                
                if available_channels:
                    random.shuffle(available_channels)
                    
                    for channel in available_channels:
                        await send_message_group(channel)
                        await asyncio.sleep(random.uniform(1.5, 3.5))
                    
                    await asyncio.sleep(random.uniform(5, 10))
                
        finally:
            if ctx.author.id in autokill_status:
                autokill_status[ctx.author.id]['running'] = False
                del autokill_status[ctx.author.id]
        
        print("\n=== Autokill Stopped ===\n")

@autokill.command(name="add")
async def add_kill_message(ctx, *, message: str):
    user_id = str(ctx.author.id)
    if user_id not in autokill_messages:
        autokill_messages[user_id] = []
    
    autokill_messages[user_id].append(message)
    await ctx.send(f"```Added message: {message}```")
    save_kill_messages()

@autokill.command(name="remove")
async def remove_kill_message(ctx, index: int):
    user_id = str(ctx.author.id)
    if user_id not in autokill_messages or not autokill_messages[user_id]:
        await ctx.send("```No messages configured```")
        return
        
    if 1 <= index <= len(autokill_messages[user_id]):
        removed = autokill_messages[user_id].pop(index-1)
        await ctx.send(f"```Removed message: {removed}```")
        save_kill_messages()
    else:
        await ctx.send(f"```Invalid index. Use .autokill list to see message indices```")

@autokill.command(name="list")
async def list_kill_messages(ctx):
    user_id = str(ctx.author.id)
    if user_id not in autokill_messages or not autokill_messages[user_id]:
        await ctx.send("```No messages configured```")
        return
        
    message_list = "\n".join(f"{i+1}. {msg}" for i, msg in enumerate(autokill_messages[user_id]))
    await ctx.send(f"```Your configured messages:\n\n{message_list}```")

@autokill.command(name="clear")
async def clear_kill_messages(ctx):
    user_id = str(ctx.author.id)
    if user_id in autokill_messages:
        autokill_messages[user_id] = []
        await ctx.send("```Cleared all messages```")
        save_kill_messages()
    else:
        await ctx.send("```No messages configured```")

@autokill.command(name="stop")
async def stop_autokill(ctx):
    if ctx.author.id in autokill_status:
        autokill_status[ctx.author.id]['running'] = False
        del autokill_status[ctx.author.id]
        await ctx.send("```Stopped autokill```")
    else:
        await ctx.send("```Autokill is not running```")

def save_kill_messages():
    with open('autokill_config.json', 'w') as f:
        json.dump(autokill_messages, f)

def load_kill_messages():
    global autokill_messages
    try:
        with open('autokill_config.json', 'r') as f:
            autokill_messages = json.load(f)
    except FileNotFoundError:
        autokill_messages = {}

manual_targets = {}
manual_messages = {}

@bot.group(invoke_without_command=True)
async def manual(ctx, user: discord.Member = None):
    if ctx.invoked_subcommand is None:
        if not user:
            await ctx.send("```Please mention a user```")
            return
            
        user_id = str(ctx.author.id)
        if user_id not in manual_messages or not manual_messages[user_id]:
            await ctx.send("```No messages configured. Use .manual add <message> to add messages```")
            return
        
        manual_targets[ctx.author.id] = {
            'user': user,
            'running': True
        }
        
        used_messages = set()
        messages_sent = 0
        
        async def send_message():
            nonlocal used_messages, messages_sent
            
            available_messages = [msg for msg in manual_messages[user_id] if msg not in used_messages]
            if not available_messages:
                used_messages.clear()
                available_messages = manual_messages[user_id]
            
            message = random.choice(available_messages)
            used_messages.add(message)
            
            try:
                full_message = f"{user.mention} {message.replace('{username}', user.display_name)}"
                sent_message = await ctx.send(full_message)
                manual_message_ids.add(sent_message.id)  
                messages_sent += 1
                print(f"Manual message sent ({messages_sent}): {message}")
            except Exception as e:
                print(f"Error sending manual message: {str(e)}")
        
        await ctx.send(f"```Manual mode enabled for {user.name}. Messages will send every 3 seconds.```")
        
        try:
            while ctx.author.id in manual_targets and manual_targets[ctx.author.id]['running']:
                await send_message()
                await asyncio.sleep(3)
        except Exception as e:
            print(f"Manual mode error: {str(e)}")
        finally:
            if ctx.author.id in manual_targets:
                del manual_targets[ctx.author.id]

@manual.command(name="stop")
async def stop_manual(ctx):
    if ctx.author.id in manual_targets:
        manual_targets[ctx.author.id]['running'] = False
        await ctx.send("```Manual mode stopped```")
    else:
        await ctx.send("```Manual mode is not running```")
@manual.command(name="add")
async def add_manual_message(ctx, *, message: str):
    user_id = str(ctx.author.id)
    if user_id not in manual_messages:
        manual_messages[user_id] = []
    
    manual_messages[user_id].append(message)
    await ctx.send(f"```Added message: {message}```")
    save_manual_messages()

@manual.command(name="remove")
async def remove_manual_message(ctx, index: int):
    user_id = str(ctx.author.id)
    if user_id not in manual_messages or not manual_messages[user_id]:
        await ctx.send("```No messages configured```")
        return
        
    if 1 <= index <= len(manual_messages[user_id]):
        removed = manual_messages[user_id].pop(index-1)
        await ctx.send(f"```Removed message: {removed}```")
        save_manual_messages()
    else:
        await ctx.send(f"```Invalid index. Use .manual list to see message indices```")

@manual.command(name="list")
async def list_manual_messages(ctx):
    user_id = str(ctx.author.id)
    if user_id not in manual_messages or not manual_messages[user_id]:
        await ctx.send("```No messages configured```")
        return
        
    message_list = "\n".join(f"{i+1}. {msg}" for i, msg in enumerate(manual_messages[user_id]))
    await ctx.send(f"```Your configured messages:\n\n{message_list}```")

@manual.command(name="clear")
async def clear_manual_messages(ctx):
    user_id = str(ctx.author.id)
    if user_id in manual_messages:
        manual_messages[user_id] = []
        await ctx.send("```Cleared all messages```")
        save_manual_messages()
    else:
        await ctx.send("```No messages configured```")

def save_manual_messages():
    with open('manual_config.json', 'w') as f:
        json.dump(manual_messages, f)

def load_manual_messages():
    global manual_messages
    try:
        with open('manual_config.json', 'r') as f:
            manual_messages = json.load(f)
    except FileNotFoundError:
        manual_messages = {}

@bot.group(invoke_without_command=True)
async def vcjoin(ctx):

    if ctx.invoked_subcommand is None:
        await ctx.send(f"""```ansi
Voice Channel Commands:
• >vcjoin stable <channel_id> - Join and stay in one voice channel
• >vcjoin rotate - Rotate through all available voice channels
• >vcjoin random - Randomly join voice channels
• >vcjoin list - List all available voice channels
• >vcjoin leave - Leave voice channel
• >vcjoin status - Show current VC status```""")

@vcjoin.command(name="stable")
async def vc_stable(ctx, channel_id: int = None):

    if not channel_id:
        await ctx.send(f"```ansi\nPlease provide a voice channel ID```")
        return
        
    try:
        channel = bot.get_channel(channel_id)
        if not channel or not isinstance(channel, discord.VoiceChannel):
            await ctx.send(f"```ansi\nInvalid voice channel ID```")
            return
            
        voice_client = ctx.guild.voice_client
        if voice_client:
            await voice_client.move_to(channel)
        else:
            await channel.connect()
            
        await ctx.send(f"```ansi\nConnected to {channel.name}```")
    except Exception as e:
        await ctx.send(f"```ansi\nError: {str(e)}```")

@vcjoin.command(name="list")
async def vc_list(ctx):

    voice_channels = [channel for channel in ctx.guild.channels if isinstance(channel, discord.VoiceChannel)]
    if not voice_channels:
        await ctx.send(f"```ansi\nNo voice channels available```")
        return
        
    channel_list = "\n".join(f"• {channel.id}: {channel.name}" for channel in voice_channels)
    await ctx.send(f"```ansi\nAvailable Voice Channels:\n\n{channel_list}```")

@vcjoin.command(name="status")
async def vc_status(ctx):

    voice_client = ctx.guild.voice_client
    if voice_client and voice_client.channel:
        await ctx.send(f"""```ansi
Current Voice Status:
• Connected to: {voice_client.channel.name}
• Channel ID: {voice_client.channel.id}
• Latency: {round(voice_client.latency * 1000, 2)}ms```""")
    else:
        await ctx.send(f"```ansi\nNot connected to any voice channel```")

@vcjoin.command(name="leave")
async def vc_leave(ctx):

    voice_client = ctx.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await ctx.send(f"```ansi\nLeft voice channel```")
    else:
        await ctx.send(f"```ansi\nNot in a voice channel```")

@vcjoin.command(name="rotate")
async def vc_rotate(ctx):

    voice_channels = [channel for channel in ctx.guild.channels if isinstance(channel, discord.VoiceChannel)]
    if not voice_channels:
        await ctx.send(f"```ansi\nNo voice channels available```")
        return
        
    rotate_active = True
    await ctx.send(f"```ansi\nStarting voice channel rotation```")
    
    while rotate_active:
        for channel in voice_channels:
            try:
                voice_client = ctx.guild.voice_client
                if voice_client:
                    await voice_client.move_to(channel)
                else:
                    await channel.connect()
                    
                print(f"Moved to channel: {channel.name}")
                await asyncio.sleep(10)
                
                if not rotate_active:
                    break
                    
            except Exception as e:
                print(f"Error rotating to {channel.name}: {e}")
                continue

anti_last_words = [
    "LAST WORD FOR",
    "LAST",
    "last word for",
    "Lasts for",
    "L A S T ",
    "L @ S T ",
    "LAASTT",
    "LASSTT",
    "LASTS",
    "LAST WORDED"
]

antilast_enabled = False

antilast_data = {
    "whitelisted_users": set(),
    "whitelisted_channels": set(),
    "webhook_url": None
}

def save_antilast_data():
    with open('@antilast.json', 'w') as f:
        json.dump({
            "whitelisted_users": list(antilast_data["whitelisted_users"]),
            "whitelisted_channels": list(antilast_data["whitelisted_channels"]),
            "webhook_url": antilast_data["webhook_url"],
            "enabled": antilast_enabled
        }, f, indent=4)

def load_antilast_data():
    global antilast_enabled
    try:
        with open('@antilast.json', 'r') as f:
            data = json.load(f)
            antilast_data["whitelisted_users"] = set(data.get("whitelisted_users", []))
            antilast_data["whitelisted_channels"] = set(data.get("whitelisted_channels", []))
            antilast_data["webhook_url"] = data.get("webhook_url")
            antilast_enabled = data.get("enabled", False)
    except (FileNotFoundError, json.JSONDecodeError):

        antilast_data["whitelisted_users"] = set()
        antilast_data["whitelisted_channels"] = set()
        antilast_data["webhook_url"] = None
        antilast_enabled = False
        save_antilast_data()

@bot.group(invoke_without_command=True)
async def antilast(ctx):
    await ctx.send("```run '.help antilast' for more info```")

@antilast.command()
async def toggle(ctx, state: str = None):
    global antilast_enabled
    if state not in ['on', 'off']:
        await ctx.send("```Please choose 'on' or 'off'```")
        return
        
    antilast_enabled = state == 'on'
    save_antilast_data()
    await ctx.send(f"```Anti last word {state}```")

@antilast.command()
async def whitelist(ctx, user_id: str):
    antilast_data["whitelisted_users"].add(user_id)
    save_antilast_data()
    await ctx.send(f"```Added user {user_id} to whitelist```")

@antilast.command()
async def channel(ctx, channel_id: str):
    antilast_data["whitelisted_channels"].add(channel_id)
    save_antilast_data()
    await ctx.send(f"```Added channel {channel_id} to whitelist```")

@antilast.command()
async def webhook(ctx, webhook_url: str):
    antilast_data["webhook_url"] = webhook_url
    save_antilast_data()
    await ctx.send("```Updated webhook URL```")

@antilast.command()
async def config(ctx):
    config = f"""```
Antilast Configuration:
Whitelisted Users: {', '.join(antilast_data["whitelisted_users"]) or 'None'}
Whitelisted Channels: {', '.join(antilast_data["whitelisted_channels"]) or 'None'}
Webhook: {'Set' if antilast_data["webhook_url"] else 'Not Set'}```"""
    await ctx.send(config)

load_antilast_data()

@bot.command()
async def hypesquad(ctx, house: str):
    house_ids = {
        "bravery": 1,
        "brilliance": 2,
        "balance": 3
    }

    headers = {
        "Authorization": bot.http.token, 
        "Content-Type": "application/json"
    }

    if house.lower() == "off":
        url = "https://discord.com/api/v9/hypesquad/online"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                if response.status == 204:
                    await ctx.send("```HypeSquad house removed.```")
                else:
                    error_message = await response.text()
                    await ctx.send(f"```Failed to remove HypeSquad house: {response.status} - {error_message}```")
        return

    house_id = house_ids.get(house.lower())
    if house_id is None:
        await ctx.send("```Invalid house. Choose from 'bravery', 'brilliance', 'balance', or 'off'.```")
        return

    payload = {"house_id": house_id}
    url = "https://discord.com/api/v9/hypesquad/online"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 204:
                await ctx.send(f"```HypeSquad house changed to {house.capitalize()}.```")
            else:
                error_message = await response.text()
                await ctx.send(f"```Failed to change HypeSquad house: {response.status} - {error_message}```")


@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild

    server_info = (
        "```"
        "Server Information\n"
        "-----------------------------\n"
        f"Name          : {guild.name}\n"
        f"Server ID     : {guild.id}\n"
        f"Owner         : {guild.owner}\n"
        f"Members       : {guild.member_count}\n"
        f"Created On    : {guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Region        : {guild.preferred_locale}\n"
        f"Roles         : {len(guild.roles)}\n"
        f"Channels      : {len(guild.channels)} (Text: {len(guild.text_channels)}, Voice: {len(guild.voice_channels)})\n"
        f"Boosts        : {guild.premium_subscription_count} (Level {guild.premium_tier})\n"
        "```"
    )

    await ctx.send(server_info)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author  # Defaults to the command caller

    user_info = (
        "```"
        "User Information\n"
        "-----------------------------\n"
        f"Name        : {member.name}#{member.discriminator}\n"
        f"User ID     : {member.id}\n"
        f"Nickname    : {member.nick if member.nick else 'None'}\n"
        f"Created On  : {member.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Joined On   : {member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Roles       : {', '.join([role.name for role in member.roles if role.name != '@everyone']) or 'None'}\n"
        f"Boosting    : {'Yes' if member.premium_since else 'No'}\n"
        "```"
    )

    await ctx.send(user_info)


@bot.command()
async def say(ctx, *, message: str):
    tokens, delay = await get_token_settings()

    channel_id = ctx.channel.id
    parts = message.split(" ", 1)

    try:
        token_index = int(parts[0])
        if len(parts) < 2:
            await ctx.send("```Please specify a message after the token index!```")
            return

        actual_message = parts[1]  

        if token_index < 1 or token_index > len(tokens):
            await ctx.send("```Invalid token index specified!```")
            return

        token = tokens[token_index - 1]  
        tokens_to_use = [token]  
    except ValueError:
        actual_message = message
        tokens_to_use = tokens

    async def send_message(token, message):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        payload = {
            'content': message
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers, json=payload) as resp:
                if resp.status == 200:
                    print(f"Message sent with token: {token[-4:]}")
                elif resp.status == 429:
                    retry_after = int(resp.headers.get("Retry-After", 1))
                    print(f"Rate limited with token: {token[-4:]}. Retrying after {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                    await send_message(token, message)
                else:
                    print(f"Failed to send message with token: {token[-4:]}. Status code: {resp.status}")

    tasks = [send_message(token, actual_message) for token in tokens_to_use]
    await asyncio.gather(*tasks)
    
    await ctx.send(f"```Message sent by token {token_index}.```" if len(tokens_to_use) == 1 else "```Message sent by all tokens.```")

INSULT_API_URL = 'https://evilinsult.com/generate_insult.php?lang=en&type=json'

@bot.command()
async def insult(ctx, user: discord.User):
    await ctx.message.delete()
    try:
        response = requests.get(INSULT_API_URL)
        response.raise_for_status()
        insult = response.json()['insult']
        await ctx.send(f'{user.mention}, {insult}')
    except requests.RequestException as e:
        await ctx.send('Failed to fetch an insult. Please try again later.', delete_after=5)
        print(f'Error fetching insult: {e}', delete_after=5)

@bot.command(help='Ladders messages')
async def fl(ctx, *, sentence: str):
    await ctx.message.delete()

    # Regex to match words or quoted strings
    pattern = r'\'(.*?)\'|(\S+)'
    matches = re.findall(pattern, sentence)

    i = 0  # Initialize index for tracking the current word
    while i < len(matches):
        word = matches[i][0] if matches[i][0] else matches[i][1]
        try:
            await ctx.send(word)
            i += 1  # Move to the next word only after successful send
        except discord.errors.HTTPException as e:
            print(f'Rate limit hit, retrying... Error: {e}')
            await asyncio.sleep(2.1)

active_clients = []

@bot.command()
async def vcmulti(ctx, channel_id: int):
    tokens = load_tokens()
    
    async def connect_voice(token):
        try:
            intents = discord.Intents.default()
            intents.voice_states = True
            client = commands.Bot(command_prefix='>', self_bot=True, intents=intents)

            @client.event
            async def on_ready():
                try:
                    channel = client.get_channel(channel_id)
                    if channel:
                        voice = await channel.connect()
                        active_clients.append(client)
                        print(f"Connected to voice with token ending in {token[-4:]}")
                except Exception as e:
                    print(f"Error connecting: {e}")

            await client.start(token, bot=False)

        except Exception as e:
            print(f"Error with token {token[-4:]}: {e}")

    tasks = [connect_voice(token) for token in tokens]
    await ctx.send(f"```Connecting {len(tasks)} tokens to voice channel {channel_id}```")
    await asyncio.gather(*tasks, return_exceptions=True)

@bot.command()
async def vcend(ctx, channel_id: int):
    tokens = load_tokens()
    
    async def disconnect_voice(token):
        try:
            intents = discord.Intents.default()
            intents.voice_states = True
            client = commands.Bot(command_prefix='.', self_bot=True, intents=intents)

            @client.event
            async def on_ready():
                try:
                    channel = client.get_channel(channel_id)
                    if channel:
                        for vc in client.voice_clients:
                            if vc.channel.id == channel_id:
                                await vc.disconnect()
                        print(f"Disconnected token ending in {token[-4:]}")
                except Exception as e:
                    print(f"Error disconnecting: {e}")
                finally:
                    await client.close()

            await client.start(token, bot=False)

        except Exception as e:
            print(f"Error with token {token[-4:]}: {e}")

    tasks = [disconnect_voice(token) for token in tokens]
    await ctx.send(f"```Disconnecting {len(tasks)} tokens from voice channel {channel_id}```")
    await asyncio.gather(*tasks, return_exceptions=True)

active_reaction_tasks = []




reactm_running = {}
reactm_tasks = {}



reactm_running = {}
reactm_tasks = {}


@bot.command()
async def tok(ctx):
    tokens_list = load_tokens()
    if not tokens_list:
        await ctx.send("No tokens found in token.txt")
        return

    async def get_token_status(token):
        try:
            intents = discord.Intents.default()
            client = commands.Bot(command_prefix='.', self_bot=True, intents=intents)
            
            token_status = {"username": None, "active": False}

            @client.event
            async def on_ready():
                token_status["username"] = f"{client.user.name}#{client.user.discriminator}"
                token_status["active"] = True
                await client.close()

            await client.start(token, bot=False)
            return token_status
            
        except discord.LoginFailure:
            return {"username": f"Invalid token ending in {token[-4:]}", "active": False}
        except Exception as e:
            return {"username": f"Error with token {token[-4:]}: {str(e)}", "active": False}

    loading_message = await ctx.send("```Fetching token statuses...```")
    
    usernames = []
    active_count = 0

    page_char_limit = 2000

    for i, token in enumerate(tokens_list, 1):
        status = await get_token_status(token)
        username = status["username"]
        token_state = f"{green}(active){reset}" if status["active"] else f"{red}(locked){reset}"
        
        if status["active"]:
            active_count += 1
            
        usernames.append(f"[ {i} ] {username} {token_state}")

        page_content = "\n".join(usernames[-(page_char_limit // 50):])  
        progress_message = f"Fetching token statuses...\n\n{page_content}\n\nActive tokens: {active_count}/{len(tokens_list)}"
        
        await loading_message.edit(content=f"```ansi\n{progress_message}```")
        await asyncio.sleep(0.9)

    final_message = f"T O K E N S\n" + "\n".join(usernames) + f"\n\nTotal active tokens: {active_count}/{len(tokens_list)}"
    for part in [final_message[i:i+page_char_limit] for i in range(0, len(final_message), page_char_limit)]:
        await loading_message.edit(content=f"```ansi\n{part}```")

@bot.command()
async def bold(ctx):
    global bold_mode
    bold_mode = True
    await ctx.send("```enabling boldbess```")

@bot.command()
async def unbold(ctx):
    global bold_mode
    bold_mode = False
    await ctx.send("```disabling bold```")

@bot.command()
async def ghostping(ctx, user: discord.User):

    try:

        message = await ctx.send(f"{user.mention}")
        await message.delete()  
        await ctx.message.delete()  

    except Exception as e:
        await ctx.send(f"```Failed: {e}```")

@bot.command()
async def blast(ctx, count: int, *, text: str):
    """Sends a message multiple times with no delay."""
    await ctx.send(f"Starting spam: `{text}` x{count}")

    for _ in range(count):
        try:
            await ctx.send(text)
        except discord.HTTPException as e:
            if e.status == 429:
                print("Rate limited. Stopping...")
                break

    await ctx.send("Spam completed.")

# Helper function to send large text in chunks
async def send_large_message(ctx, message: str):
    # Discord has a message length limit of 4000 characters, so we split the message
    # into chunks of 2000 characters or less.
    for i in range(0, len(message), 2000):
        await ctx.send(message[i:i+2000])
COMMANDS_PER_PAGE = 15  # How many commands to show per page

@bot.command(aliases=['p', 'page'])
async def paginate(ctx, page: int = 1):
    """Paginated command list using red/black theme and page numbers."""
    # Collect all commands (including hidden)
    all_commands = sorted(bot.commands, key=lambda c: c.qualified_name)
    total_pages = math.ceil(len(all_commands) / COMMANDS_PER_PAGE)

    # Clamp page within bounds
    page = max(1, min(page, total_pages))
    start = (page - 1) * COMMANDS_PER_PAGE
    end = start + COMMANDS_PER_PAGE
    current_cmds = all_commands[start:end]

    # Build the red/black themed help panel
    help_message = "```diff\n"
    help_message += "-=============================-\n"
    help_message += "-        HELP PANEL           -\n"
    help_message += "- <> = required args          -\n"
    help_message += "- [] = optional args          -\n"
    help_message += "-=============================-\n"
    help_message += "\n< Rifat's Selfbot >\n\n"
    help_message += f"[ Page {page}/{total_pages} ]\n\n"

    for cmd in current_cmds:
        help_message += f"+ .{cmd.qualified_name} {cmd.signature}\n"

    help_message += "```"

    await ctx.send(help_message)
    await ctx.message.delete()

@bot.command()
async def help(ctx, *, command_name=None):
    """Show help for a specific command."""
    if command_name:
        cmd = bot.get_command(command_name)
        if cmd:
            help_msg = "```diff\n"
            help_msg += f"- Command: .{cmd.qualified_name}\n"
            help_msg += f"+ Usage: .{cmd.qualified_name} {cmd.signature}\n"
            help_msg += f"+ Info: {cmd.help if cmd.help else 'No description provided.'}\n"
            help_msg += "```"
            await ctx.send(help_msg)
        else:
            await ctx.send(f"Command `{command_name}` not found.")
    else:
        # Default to first page
        await ctx.invoke(bot.get_command("paginate"), page=1)

    await ctx.message.delete()


# Define colors
yellow = "\033[33m"
green = "\033[32m"
red = "\033[31m"
cyan = "\033[36m"
reset = "\033[0m"

# Validate Token
async def validate_token(token):
    client = discord.Client(intents=discord.Intents.default())
    token_status = {"active": False, "username": None}

    @client.event
    async def on_ready():
        token_status["username"] = f"{client.user.name}#{client.user.discriminator}"
        token_status["active"] = True
        await client.close()

    try:
        await client.start(token, bot=False)
    except discord.errors.LoginFailure:
        return False, "Invalid token"
    except Exception as e:
        return False, f"Error: {str(e)}"

    if token_status["active"]:
        return True, token_status["username"]
    return False, "Failed to validate token"

# Add Token Command
@bot.command(name="addtoken")
async def add_token(ctx, token: str):
    try:
        await ctx.message.delete()
    except:
        pass

    token = token.strip()
    
    is_valid, details = await validate_token(token)
    
    if is_valid:
        tokens = []
        if os.path.exists('token.txt'):
            with open('token.txt', 'r') as f:
                tokens = [t.strip() for t in f.readlines() if t.strip()]
                
            if token in tokens:
                await ctx.send(f"```ansi\n{yellow}Token already exists in the file{reset}```", delete_after=5)
                return

        tokens.append(token)
        
        with open('token.txt', 'w') as f:
            f.write('\n'.join(tokens))
            if tokens: 
                f.write('\n')
                
        await ctx.send(f"```ansi\n{green}Token added successfully User: {details}{reset}```", delete_after=5)
    else:
        await ctx.send(f"```ansi\n{red}Invalid token! Error: {details}{reset}```", delete_after=5)

# Remove Token Command
@bot.command(name="removetoken")
async def remove_token(ctx, token: str):
    try:
        await ctx.message.delete()
    except:
        pass

    token = token.strip()
    
    if os.path.exists('token.txt'):
        with open('token.txt', 'r') as f:
            tokens = [t.strip() for t in f.readlines() if t.strip()]
        
        if token in tokens:
            tokens.remove(token)
            with open('token.txt', 'w') as f:
                f.write('\n'.join(tokens))
                if tokens:
                    f.write('\n')
            await ctx.send(f"```ansi\n{green}  Token removed successfully!{reset}```", delete_after=5)
        else:
            await ctx.send(f"```ansi\n{red}  Token not found in the file!{reset}```", delete_after=5)
    else:
        await ctx.send(f"```ansi\n{red}  No token file exists!{reset}```", delete_after=5)

# List Tokens Command
@bot.command(name="listtokens")
async def list_tokens(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    if os.path.exists('token.txt'):
        with open('token.txt', 'r') as f:
            tokens = [t.strip() for t in f.readlines() if t.strip()]
        
        if tokens:
            tokens_text = f"```ansi\n{cyan}Current tokens:\n" + "\n".join(f"{i+1}. {token}" for i, token in enumerate(tokens)) + f"{reset}```"
            await ctx.send(tokens_text, delete_after=10)
        else:
            await ctx.send(f"```ansi\n{yellow}No tokens found in the file!{reset}```", delete_after=5)
    else:
        await ctx.send(f"```ansi\n{red}  No token file exists!{reset}```", delete_after=5)

@bot.command(name="pay")
async def pay(ctx):
    message = (
        "╔═━─━─────────────━─━═╗\n"
        "         **Dezu</>**\n"
        "╚═━─━─────────────━─━═╝\n\n"
        "**The Seller You Trust**\n"
        "160+ shadows whisper positive tales.\n\n"
        "**Payment Methods:**\n"
        "- Bkash: `01777365144`\n"
        "- Crypto: LTC / USDT\n"
        "- Others: INR / PKR / Nagad / Bkash\n\n"
        "_After payment, send proof — the silence is golden._"
    )
    await ctx.send(message)


@bot.command(name="vouch")
async def vouch(ctx):
    message = (
        "╔═━─━─────────────━─━═╗\n"
        "         **Dezu</> Vouch**\n"
        "╚═━─━─────────────━─━═╝\n\n"
        "Leave your mark here:\n"
        "<https://discord.com/channels/1020055789181874197/1194173760203403337>\n\n"
        "Example:\n"
        "`Legit got < Product Name > from @Rifat.dez_`\n\n"
        "*Our truth lies in your words.*"
    )
    await ctx.send(message)


@bot.command(name="legit")
async def legit(ctx):
    message = (
        "╔═━─━─────────────━─━═╗\n"
        "         **Dezu</>**\n"
        "╚═━─━─────────────━─━═╝\n\n"
        "_Are we real?_\n"
        "**Shadows don’t lie.**\n"
        "Trust is forged in silence.\n\n"
        "*Thanks for walking the line with us.*"
    )
    await ctx.send(message)

@bot.command(name="ownx")
async def ownx(ctx):
    message = (
        ">>> [CRIMSON_GATE]\n"
        "    https://discord.gg/crimsons"
    )
    await ctx.send(message)

@bot.command(name="XX")
async def XX(ctx):
    message = (
        ">>> [SHADOW_NEXUS]\n"
        "    https://discord.gg/wc4WD4nscU"
    )
    await ctx.send(message)

@bot.command(name="ourbot")
async def ourbot(ctx):
    message = (
        ">>> [BRAVERS_THE_BEAST_BOT]</>\n"
        "    https://discord.ly/bravers"
    )
    await ctx.send(message)

@bot.command(name="wait")
async def wait(ctx):
    message = (
        "**Rifat Sales Update**\n\n"
        "Your order is currently being finalized.\n"
        "We appreciate your trust and patience.\n"
        "Rest assured, Rifat is handling your purchase with care.\n\n"
        "*Thank you for choosing Rifat.*"
    )
    await ctx.send(message)

@bot.command(name="tos")
async def tos(ctx):
    message = (
        ">>> ** Rifat’s Terms of Service**\n"
        "**➤ 1.** Dealing with me = agreeing to TOS. No disputes.\n"
        "**➤ 2.** You must read the TOS in the product embeds.\n"
        "**➤ 3.** Know what you’re buying. No refunds.\n"
        "**➤ 4.** DM for help if something’s unclear.\n"
        "**➤ 5.** If the supplier scams, we *may* refund, not guaranteed.\n"
        "**➤ 6.**  Always pay first.\n"
        "**➤ 7.** MM allowed — but only **verified** ones.\n\n"
        "*Thank you for choosing* **Rifat's Service.**"
    )
    await ctx.send(message)

@bot.command(name="received")
async def received(ctx):
    message = (
        ">>> **✅ Payment Successfully Received**\n"
        "**➤ Status:** Confirmed & Logged\n"
        "**➤ Timestamp:** Payment verified at the time of message\n"
        "**➤ Note:** Your order is now queued for processing\n"
        "**➤ Reminder:** Please allow some time for fulfillment\n\n"
        "*Thank you for shopping with* **Rifat's Service.** 🛍️"
    )
    await ctx.send(message)

@bot.group(invoke_without_command=True)
async def rotateguild(ctx, delay: float = 2.0):
    global guild_rotation_task, guild_rotation_delay

    if guild_rotation_task and not guild_rotation_task.cancelled():
        await ctx.send("```Rotation is already running.```\n— Rifat </> Dev")
        return

    guild_rotation_delay = delay

    async def rotate_guilds():
        headers = {
            "authority": "canary.discord.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": bot.http.token,
            "content-type": "application/json",
            "origin": "https://canary.discord.com",
            "referer": "https://canary.discord.com/channels/@me",
            "user-agent": "Mozilla/5.0...",
            "x-super-properties": "eyJvcyI6IldpbmRvd3Mi..."
        }

        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    valid_guild_ids = []

                    async with session.get('https://canary.discord.com/api/v9/users/@me/guilds', headers=headers) as guild_resp:
                        if guild_resp.status != 200:
                            await ctx.send("```Failed to fetch guilds.```\n— Rifat </> Dev")
                            return

                        guilds = await guild_resp.json()

                        for guild in guilds:
                            test_payload = {
                                'identity_guild_id': guild['id'],
                                'identity_enabled': True
                            }

                            async with session.put('https://canary.discord.com/api/v9/users/@me/clan', headers=headers, json=test_payload) as test_resp:
                                if test_resp.status == 200:
                                    valid_guild_ids.append(guild['id'])

                        if not valid_guild_ids:
                            await ctx.send("```No valid guilds found.```\n— Rifat </> Dev")
                            return

                        await ctx.send(
                            f"╔═━─━─────────────━─━═╗\n"
                            f"   **Clan Rotation Started**\n"
                            f"╚═━─━─────────────━─━═╝\n\n"
                            f"• Found `{len(valid_guild_ids)}` guilds\n"
                            f"• Delay: `{guild_rotation_delay}s`\n"
                            f"• Status: `Running`\n\n"
                            f"— Rifat </> Dev"
                        )

                        while True:
                            for guild_id in valid_guild_ids:
                                payload = {
                                    'identity_guild_id': guild_id,
                                    'identity_enabled': True
                                }
                                async with session.put('https://canary.discord.com/api/v9/users/@me/clan', headers=headers, json=payload) as put_resp:
                                    if put_resp.status == 200:
                                        await asyncio.sleep(guild_rotation_delay)

            except asyncio.CancelledError:
                raise
            except Exception as e:
                print(f"Error in guild rotation: {e}")
                await asyncio.sleep(5)

    guild_rotation_task = asyncio.create_task(rotate_guilds())

@rotateguild.command(name="stop")
async def rotateguild_stop(ctx):
    global guild_rotation_task

    if guild_rotation_task and not guild_rotation_task.cancelled():
        guild_rotation_task.cancel()
        guild_rotation_task = None
        await ctx.send(
            "╔═━─━─────────────━─━═╗\n"
            "**Clan Rotation Stopped**\n"
            "╚═━─━─────────────━─━═╝\n\n"
            "— Rifat </> Dev"
        )
    else:
        await ctx.send("```Clan rotation is not running.```\n— Rifat </> Dev")

@rotateguild.command(name="delay")
async def rotateguild_delay(ctx, delay: float):
    global guild_rotation_delay

    if delay < 1.0:
        await ctx.send("```Delay must be at least 1 second.```\n— Rifat </> Dev")
        return

    guild_rotation_delay = delay
    await ctx.send(
        f"╔═━─━─────────────━─━═╗\n"
        "**Rotation Delay Updated**\n"
        "╚═━─━─────────────━─━═╝\n\n"
        f"New delay: `{guild_rotation_delay}s`\n\n"
        f"— Rifat </> Dev"
    )

@rotateguild.command(name="status")
async def rotateguild_status(ctx):
    status = "Running ✅" if (guild_rotation_task and not guild_rotation_task.cancelled()) else "Stopped ❌"
    await ctx.send(
        f"╔═━─━─────────────━─━═╗\n"
        "**Clan Rotation Status**\n"
        "╚═━─━─────────────━─━═╝\n\n"
        f"• Status: `{status}`\n"
        f"• Delay: `{guild_rotation_delay}s`\n\n"
        f"— Rifat </> Dev"
    )



@bot.command(name="afk")
async def afk(ctx, *, reason="No reason provided"):
    afk_users[ctx.author.id] = {"reason": reason, "time": datetime.datetime.utcnow()}
    await ctx.send(
        f">>> **{ctx.author.name} is now AFK**\n"
        f"**➤ Reason:** {reason}\n"
        f"**➤ Status:** Remains until you use `>unafk`."
    )

@bot.command(name="unafk")
async def unafk(ctx):
    if ctx.author.id in afk_users:
        delta = datetime.datetime.utcnow() - afk_users.pop(ctx.author.id)["time"]
        await ctx.send(
            f">>> **🎉 Welcome back {ctx.author.name}!**\n"
            f"**➤ You were AFK for:** {str(delta).split('.')[0]}"
        )
    else:
        await ctx.send(f">>> **{ctx.author.name}, you are not AFK.**")

@bot.event
async def on_message(msg):
    if msg.author.bot:
        return

    # Notify if message mentions an AFK user
    for user in msg.mentions:
        if user.id in afk_users:
            afk = afk_users[user.id]
            delta = datetime.datetime.utcnow() - afk["time"]
            await msg.channel.send(
                f">>> **📢 {user.name} is AFK**\n"
                f"**➤ Reason:** {afk['reason']}\n"
                f"**➤ Time Away:** {str(delta).split('.')[0]}"
            )

    # Notify if replying to an AFK user's message
    if msg.reference:
        try:
            ref_msg = await msg.channel.fetch_message(msg.reference.message_id)
            if ref_msg.author.id in afk_users:
                afk = afk_users[ref_msg.author.id]
                delta = datetime.datetime.utcnow() - afk["time"]
                await msg.channel.send(
                    f">>> **📢 {ref_msg.author.name} is AFK**\n"
                    f"**➤ Reason:** {afk['reason']}\n"
                    f"**➤ Time Away:** {str(delta).split('.')[0]}"
                )
        except discord.NotFound:
            pass

    await bot.process_commands(msg)

@bot.command(aliases=["jerkoff", "ejaculate", "orgasm"])
async def cum(ctx):
    await ctx.message.delete()
    message = await ctx.send('''
            :ok_hand:            :smile:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant:''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :smiley:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:  
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :grimacing:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant:  
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :persevere:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:   
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :confounded:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant: 
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :tired_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:    
             ''')
    await asyncio.sleep(0.5)
    await message.edit(contnet='''
                       :ok_hand:            :weary:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:= D:sweat_drops:
             :trumpet:      :eggplant:        
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :dizzy_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :drooling_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''')

  #kick
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    # Check if the command issuer has the necessary permissions to kick members
    if ctx.author.guild_permissions.kick_members:
        # Attempt to kick the specified member
        try:
            await member.kick(reason=reason)
            await ctx.send(f'{member.mention} has been kicked.')
        except discord.Forbidden:
            await ctx.send("I don't have permission to kick that member.")
        except discord.HTTPException:
            await ctx.send('An error occurred while attempting to kick the member.')
    else:
        await ctx.send("You don't have permission to kick members.")

   #ban
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    # Check if the command issuer has the necessary permissions to ban members
    if ctx.author.guild_permissions.ban_members:
        # Attempt to ban the specified member
        try:
            await member.ban(reason=reason)
            await ctx.send(f'{member.mention} has been banned.')
        except discord.Forbidden:
            await ctx.send("I don't have permission to ban that member.")
        except discord.HTTPException:
            await ctx.send('An error occurred while attempting to ban the member.')
    else:
        await ctx.send("You don't have permission to ban members.")

@bot.command()
async def nuke(ctx):
    # Check if the command issuer has the necessary permissions to manage channels
    if ctx.author.guild_permissions.manage_channels:
        try:
            # Store channel information
            channel_name = ctx.channel.name
            channel_category = ctx.channel.category
            overwrites = ctx.channel.overwrites
            
            # Delete the current channel
            await ctx.channel.delete()

            # Create a new channel with the stored information
            new_channel = await channel_category.create_text_channel(name=channel_name, overwrites=overwrites)
        except discord.Forbidden:
            await ctx.send("I don't have permission to manage channels.")
    else:
        await ctx.send("You don't have permission to manage channels.")

# Clear Tokens Command
@bot.command(name="cleartoken")
async def clear_tokens(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    if os.path.exists('token.txt'):
        with open('token.txt', 'w') as f:
            f.write('')
        await ctx.send("```ansi\n  All tokens have been cleared!```", delete_after=5)
    else:
        await ctx.send("```ansi\n  No token file exists!```", delete_after=5)

@bot.event
async def on_ready():
    print(f"🟢 Bot is online as {bot.user}")

@bot.command()
async def uptime(ctx):
    """Shows how long the bot has been running."""
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)

    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"

    output = "```diff\n"
    output += "-====== BOT UPTIME ======-\n"
    output += f"+ Rifat's Selfbot has been running for:\n+ {uptime_str}\n"
    output += "```"

    await ctx.send(output)
    await ctx.message.delete()


anime_actions = ["kiss", "hug", "slap", "pat", "cuddle", "poke", "smile"]

@bot.command(name="action")
async def action(ctx, action_type: str = None, member: discord.Member = None):
    if not action_type or action_type.lower() not in anime_actions:
        await ctx.send("```diff\n- Invalid or missing action.\n+ Usage: >action [kiss/hug/slap/pat/... ] @member\n```")
        return

    if not member:
        await ctx.send("```diff\n- You need to mention someone to interact with.\n```")
        return

    gif_url = await fetch_anime_gif(action_type)

    if gif_url:
        await ctx.send(
            f"```diff\n+ {ctx.author.display_name} {action_type}s {member.display_name}!\n```{gif_url}"
        )
    else:
        await ctx.send("```diff\n- Failed to fetch GIF.\n```")

    await ctx.message.delete()

async def fetch_anime_gif(action):
    url = f"https://nekos.best/api/v2/{action}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data["results"][0]["url"]
            return None




# Assuming these functions exist somewhere above or below:
def load_kill_messages():
    pass

def load_messages():
    pass

def load_manual_messages():
    pass

load_kill_messages()
load_messages()
load_manual_messages()


bot.run(TOKEN, bot=False)
