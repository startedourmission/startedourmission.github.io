---
title: "Sam Altman on OpenAI’s next model and the AI backlash"
source: "https://www.youtube.com/watch?v=VeizK1M7V7E&t=1s"
author:
  - "[[Sources Podcast]]"
published: 2026-09-02
created: 2026-09-04
description: "After an unreleased OpenAI model recently escaped its sandbox and hacked Hugging Face, Sam Altman tells me why the company is slowing down frontier research. We also discuss Astra, OpenAI’s next-gener"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=VeizK1M7V7E)

After an unreleased OpenAI model recently escaped its sandbox and hacked Hugging Face, Sam Altman tells me why the company is slowing down frontier research. We also discuss Astra, OpenAI’s next-generation family of models, which is coming soon.  
  
We talk about the growing backlash against AI. He explains why a faster path to recursively self-improving AI could push an OpenAI IPO further out.  
  
And he shares more about the coming consumer hardware he’s developing with Jony Ive, including the privacy questions around an ambient AI device and the first hints at the form factors they’re building.  
  
This conversation was recently filmed in two parts and in collaboration with TIME.  
  
Thanks to the show's premier sponsors: @Atlassian , Granola, and Mercury.  
  
Follow Alex Heath and subscribe to Sources:  
  
Newsletter: https://sources.news/  
Spotify: https://open.spotify.com/show/3p1KZvkbdx96VgFh8dP8Ao?si=9e6c9d5b565e41d2  
Apple Podcasts: https://podcasts.apple.com/it/podcast/sources-with-alex-heath/id1840154537  
https://x.com/alexeheath/  
  
Chapters:  
00:00 Why OpenAI Slowed Training  
08:37 What Alignment Means  
15:22 Keeping Humans in Control  
24:39 AGI vs. Superintelligence  
30:04 OpenAI’s Next Compute Bet  
31:47 AI Backlash, Jobs, and Creators  
41:31 OpenAI’s Missteps and Refocus  
45:47 Astra and Computer-Using Agents  
47:42 Regulation and the AI Race  
51:24 Merging ChatGPT and Codex  
54:22 The AI Compute Bubble  
57:07 Recursive Self-Improvement and IPO  
58:22 Humanoid Robots and Consumer Devices  
1:05:47 Life After Superintelligence

## Transcript

### Why OpenAI Slowed Training

**0:00** · Sam, what's going on?

**0:02** · It's definitely an exciting time in the world of AI. Um, model capabilities are progressing very quickly and we're seeing people do amazing things with these. And then as we talked about uh and as we knew would happen at some point, the model capability is progressing so quickly that we've had to make some changes to how we work to be able to make the safety cases and safety threshold standards, guarantees, whatever you want to call it, that we need to make to be able to confidently uh proceed with our training.

**0:31** · It's it's very important that alignment, safety, and security progress along with capabilities. And I think we have had a moment recently where the capability progress has been I mean sort of in awe is the only way I can describe it and we have needed more time to catch up with safety alignment and security. Um that's always been a core part of our work but these have to progress together and uh you know we've needed time to catch up.

**0:57** · So uh we delayed a frontier RL training run. Um even before that over you know weeks in the past of that we had paused uh and slowed down on a lot of training to have more compute to go into safety and alignment work. This is a thing that I think we should be proud of uh and it's you know a thing that I think will happen again in the future as we reach even higher levels of capability. But it is you know when you like live through it it's like ah this is a moment we talked about for a long time and now it's happening.

**1:28** · What has it been like living through it?

**1:29** · Well, it started even longer than that with the hugging face incident, right?

**1:33** · And that was a real moment of man, this is like it's like a sci-fi story. You can understand how every piece of it happened, but the number of things that came together for the hugging face incident to happen was a real wakeup call is too strong of a word because again we had talked about this, but it was like that and the things that happened at other companies were a legitimate moment of like wow the AI capability level has reached new heights and our alignment of the alignment of the model, the security we have around the model um that failed.

**2:03** · Now we treated that as an accident and we've responded as such and I think that is the way to make things better. Um but that was that was when this whole period of these last couple of months started. We then potentially hit cyber critical under our preparedness framework. Uh we then saw some things during our training run where we said well you know we need stronger alignment guarantees and we need new methods and to make more progress here. Um, but I feel both very proud of how we've reacted to it.

**2:32** · Very like, okay, we're in this in a way that feels like kind of I mean, it feels strange to have been thinking about this for the last decade and for it now to be happening and then like, you know, we know what to do. What was the thing you all saw in the training run that is not Astra? That's the future stuff that caused um it seems like the reaction that you're now talking about.

**2:58** · I mean, I know you described the hugging face, all of that and people know about the hugging face incident, but what happened on the pre-training run that really alarmed you guys?

**3:08** · Uh it was not one single thing. It was reading reading lots of samples and seeing well this this behavior is not quite aligned in the way we thought or this is this is a behavior that is like somewhat concerning combined with these other things even though it would look maybe okay in a vacuum. So it's not like there's not one smoking gun like there was with a hugging face attack of like here is this bad thing we can point to you that happened but it was

**3:32** · various degrees of misalignment along with and I think this is the more important thing than any single data point the rate at which capabilities are now progressing you know honestly like we had not the world's best last period of pre-training progress we all of a sudden have gotten so good at it that we now have these remarkably capable models it's it's really amazing amazing what Aiden and his team have done.

**3:53** · And so you have these small things that you can point to in our RL process or, you know, alignment concerns combined with what we can see coming down the road of these amazingly capable new pre-trained models. And it's really that intersection that made us want to react with an abundance of caution. Now, I don't want to overstate this either. I don't think this is like, you know, we're in this extremely critical potential catastrophe point.

**4:19** · But I also think that as the stakes get higher, as the models get more capable, because of what our mission is and because of how important it is that safety outweigh all the other, you know, pressures we have, we wanted to react with an abundance of caution. Um, and I think that's the right thing to do. I think it's good that we're doing that. I think it is a good time to slow down and make sure we can have new safety cases that justify uh the runs we want to make.

**4:49** · I think the you know previously more of the risk in the world was on how the models were deployed and used. We are moving to a world where there's more risk during the actual training and production of the models and it's good to react but I don't want to like over dramatize it either.

**5:05** · Yeah.

**5:05** · Because I think people see the hugging face incident and they see what's happened with mythos or fable and the way that even other lab leaders talk about this and they think wow like we're on the precipice of the end of the world in some sense people have thought versions of that for a long time with AI and you know there were you can this is

**5:22** · why I want to be careful not to overstate it either I think you can go back and look at a lot of previous models that in retrospect don't look scary at all that people said we're on the precipice of the end of the world about and I think the the boy who cried wolf dynamic here uh dangerous in its own way and not what we're I'm trying to do. We're trying to do but it's very irresponsible to pretend to turn a blind eye to what's happening with model capabilities. You know, many companies had different cyber incidents over the last couple of months.

**5:51** · There's a real difference in the way that different companies have responded.

**5:54** · Mhm.

**5:54** · And I think a kind of cleareyed sober response where it's like, hey, we're going to put safety in front of everything else and we are going to treat it as an increasing priority as these models get more capable is, you know, that's the approach that I would wish for for every uh every Frontier AI developer to have.

**6:13** · This episode is brought to you by Granola, the AI notepad for people in back-to-back meetings. It works everywhere you do and lets you focus on what matters. Try it at granola.ai/sources AI/sources and use the code sources for 3 months off. This episode is also brought to you by Mercury, AI native banking that's loved by more than 300,000 entrepreneurs, including me. Visit mercury.com to learn more. Mercury is a fintech, not a bank.

**6:37** · Check the show notes for details. This episode is also brought to you by Jira by Atlassian, where teams and agents get the context, coordination, and control to move work forward. Try it free at jira.com. That's jira.com.

**6:53** · And there's a lot to unpack here, but I think just to be clear, what you guys saw is in the same ballpark of hugging face in the sense of chaining together zero days um collusion among the models like what like what were you seeing? Can you give me a little more granularity on what caused the changes that you guys are making internally? So I think it's worth pointing out that the model that caused the hugging face incident is like made an AI time adjusted. It is a relatively long ago old much weaker model.

**7:24** · We have not had the new models we are training deployed in any production scenario where they could do something like that. So so I don't have like a you know here was the hugging face thing and now this did this much bigger attack on this. There was nothing here that was like third party infrastructure that no no this is really so after the hucking face incident we put a lot more

**7:47** · controls in place uh in terms of how we monitor our agents while they're working the way we sandbox things the way that our compute goes into monitoring versus just the agents running thing and I think that was great to do and we will of course do that for all new things again the the the slowdown and reallocation of resources after hugging face I think is what you'd expect um or what you should expect at least this is more like um looking at a

**8:12** · model during training, watching how how how smart and capable it's getting and watching signs of behavior and all of the ways we evaluate a model uh together. There is no one like here's the all the things chained together and what it's capable of. But it's like looking at these various data points, the level of capability, level of alignment and what this could do if it were allowed to be deployed in a way where it would, you know, chain things together. That was the concern.

### What Alignment Means

**8:37** · The hugging face incident is amazing on a lot of, you know, dimensions. I was re-watching your team's black hat presentation last night for that. And there were things that blew me away like the model literally riding like holy when it escaped and was able to get onto the internet.

**8:53** · And it's made me think about like what does alignment even mean in this context? Like what are we aligning towards? Because if you look at it very plainly, you guys gave it the task of completing an eval and it did whatever it needed to do to try to do that. And in a way that's aligned in a way if you were to just take a very simplistic view of it. But I'm curious like how your thinking on alignment has evolved since then.

**9:17** · Well, in a way that's aligned. In another way, it's like not at all. Right? Like when we talk about alignment, we talk about following the intent of a user. Like and the intent of the people that were do running that was not like break out of your sandbox and go steal the thing. No.

**9:33** · And so I think there was a failure in alignment in that it was not doing what its user intended.

**9:38** · And one of the things that I really love about the way that uh Mia and her teams talk about our work in alignment is that they're very clear on the differences here. Mhm.

**9:49** · The models are clearly very smart. If if you look at the trajectory from kind of basically last year from GPT5 to 5.6 so like this is incredible progress in capabilities. Um I don't think people feel limited by the model intelligence in the same way that they did a year ago but I think they are increasingly limited by the ability for the model to understand the intent of what they want and reliably do it.

**10:11** · M so alignment is important for many reasons clearly to avoid these big things like we're talking about now but also in terms of the smaller things that we want smaller I mean like someone adopting AI in their company and using it for all kinds of you know positive

**10:29** · increases in growth and uh making better products like that's not such a small thing but that's also an alignment thing in its own way and the more the models actually understand what that enterprise customer may intend I think the better so can you more granularly explain the changes that the research team is making. Are you shifting compute to alignment? Have you shifted teams both?

**10:51** · Definitely. I mean, all of those things and more. In the last few weeks, a number of researchers that I kind of never thought would say like, hey, I've decided that I'm going to go work on alignment have come to me and said that that's very much like feeling the recent models. We've shifted a lot of compute

**11:07** · uh not just to alignment research but also to these new monitoring systems that we uh you know we slowed down a lot after the hugging base incident and one of the reasons for that was to put this compute into monitoring systems um and we've now you know delayed a major frontier rail run and this is the first time you've done that I think so do you think about the impact this will have on the company's momentum a getting AI safety is more important than any company's momentum.

**11:35** · So like yes, I won't pretend it's like not a some factor of something to think about, but it does not like rise above the noise floor. I think in all of the conversations we've had about this, people are like, man, this is really a new level of capabilities and we really have to act decisively and responsively here. Second, I think momentum commercially is so strong right now. Uh growth has been incredibly rapid. The models are great. People, our customers are very happy. Our enterprise revenue has surpassed our consumer revenue already. you know, people are like, "Hey, the company's in great shape. I'm gonna think about that.

**12:06** · Let's just like do the right thing for um the challenge in front of us."

**12:10** · So, there's so much still to be gained out of where the models are at today that even though you're delaying the frontier for a little while, it'll be okay. we will be we we have like not only that not only if we didn't ship any more models could we just you know really grow great products and the revenue associated with that with the current models we have more models ready

**12:31** · to be released before we get to this new level of concern that we're talking about so I'm not worried about our business at this point and it's also like I think not the top of mind concern the work that uh our commercial team has been doing our product team has been doing to say nothing of the incredible model progress This has been like a very strong recent period for us and we have incredible upcoming momentum. Um this is this is a statement about models of the future and I also think that it is in our business interest to make sure that we have safe reliable robust AI like customers want this.

**13:03** · The world wants us to do this.

**13:06** · Mhm.

**13:06** · So this doesn't impact Astra the new family of models you guys have been talking about recently that's coming out soon. Well, Astro will be a model in the family. Like there will be many versions of Astra in the same way that there will be, you know, many versions of Soul. It just sort of going to be a name for a more expensive and larger model class.

**13:23** · Mhm.

**13:24** · This will impact future versions of Astra, but we'll be able to put out some with, you know, models we already feel feel safe about.

**13:30** · The release cadence of new models feels like it's sped up a lot in the last 18 months and you guys and Anthropic and others putting out new things almost every, you know, month. Do you expect the industry at large to start to slow as your rivals also see these capabilities and make similar moves or do you think you may be alone in this?

**13:50** · Well, we're going to do what we think is the right thing whether like I I don't like the whole thing in this field of we have to race to you know we have to do this because somebody else is going to do it. I think that's like a very dangerous dynamic. So but you acknowledge that's a dynamic.

**14:02** · We did not call other people and say will you also slow down if we do. we just said, hey, this is like what our mission and safety standards call for. I can't speak about others. Um, so we're going to do the thing that we think is right. Uh, and but I think even without new capability level, we can continue to push to much better product offerings.

**14:21** · We are going to find ways like we have in the past when we faced other safety and alignment challenges, which has happened many times in our history, none this significant but many times. We are going to find ways to address this. We are going to do our thing with research and software and building systems and we'll continue to progress.

**14:36** · Is there anything about the reaction you guys are making now that you \[snorts\] feel man this should have happened sooner? We should have foreseen this and then we could say like oh like we knew this was happening or is this really such an unknown part of the frontier that you couldn't have reacted sooner?

**14:53** · I mean we have been doing a lot for a long time. I think we we alignment and safety work has always been at the core of what we do and I think we have been able to put out incredibly good work there along the years we've had products out in the world. You know, could we have predicted exactly when this capability jump was going to come?

**15:12** · In my experience, probably not. You know, you can say like this is going to be the rough trajectory zoomed out, but then when the breakthroughs come, that's always been a little hard to predict.

### Keeping Humans in Control

**15:22** · And is the guiding principle for this that humans in this case like your researchers but eventually all humans as the models diffuse have to be in control at every step like what is the alignment principle that you're operating under?

**15:35** · So there's many principles like but I won't I don't think it's the spirit of your question so I won't get into like you know this is how we think about cyber it's how I think about bio like zooming all the way out we are like very proudly on team humanity we want to build a future help build a future for people we want to give people tools we want people to do things with these tools we want people to be in control of the future we want individuals to have autonomy to co-create with each other and for society to get better but be this fundamentally human endeavor um automating everything seems like both

**16:07** · dangerous and incredibly dystopic and boring and sad. It's just like that's not what we want. Um, so when we talk about alignment, we talk about a world where people remain the main character of the story but have way more leverage and ability to make life better, faster and kind of more creative and enjoyable and fulfilling for everyone. Um, there are two core alignment principles I think about there. one which you touched on people need to stay in control. We cannot have a loss of controlled AI.

**16:35** · We cannot have a kind of like worship our models and sort of trust them un check to make our decisions for us and like we have to keep the power in human hands and and then the second is that has to be done in a distributed broadly empowered way. I think concentration of power even if the alignment issue were solved and you ended up with a world where a small number of people got access to use frontier AI and had so much relative power and it was increasing so much faster than everybody else uh that would also be bad.

**17:06** · So those are kind of like two of the core alignment principles I think about no loss of control or seed of control whatever you want to call it and broad distributed empowerment to everyone at the same time. I mean, you all are a company. Um, you have a nonprofit board, but you're with a mission, but you're also a for-profit company. How do you balance that with what you're talking about? And I mean, I think like a raw, you know, capitalist view of this would be if you create this all powerful god machine, why would you give it away or make it democratically?

**17:38** · I think you can look at our actions and what we've said and what we've done and you know, we have a track record now for a long time and we've done a lot of unpopular things along the way. In fact, even the original thing of iterative deployment was widely panned by the AI safety community and said, you know, we shouldn't tell the world about this.

**17:56** · This is bad. We need to like build this in secret. It's it's too much knowledge for the world to have and, you know, then we'll have some wise people figure out how to use it and give the the fruits of this to humanity. That has never been our strategy, even when it's been very very unpopular. My favorite historical analogy of a technology, what I aspire for us to be like, is the transistor. It was it is an incredibly powerful technology for the world. It has delivered huge economic value and not just economic like the way we live our lives.

**18:22** · I think it's much better because the transistor was discovered and industrialized but very little of the value accured to the transistor companies. It mostly just diffused throughout the economy. The transistor companies did fine and I think our track record has backed us up. So you don't want to get to a point where you guys have such a powerful model that you need to be the ones controlling it. I mean there will always be an element of you controlling and the fact that you're serving it via compute, right?

**18:48** · But we we want to maximally enable people with it subject to not allowing anyone to take you know catastrophic risk on behalf of other people. So yes, we will put some safety standards around it. Um but I want people to be able to do things with our models that I personally don't like.

**19:08** · Like I think that's an important part of being a platform. I don't think we should make the kind of moral decisions for the world here. No, I think it is reasonable for us for the world to expect us to put some guardrails around it so that there are not major safety problems like we're doing right now. Um but you know like most of the critique we've gotten is you're you're giving people too much power.

**19:27** · You're letting them have too much. you're you know you're what about the misinformation or what about you know this thing or what about that or what like like we have taken a spirit of hey the world has got to be empowered here that's critical to what we do that is critical to what I believe about a healthy society and a fair society looking like and you know like with free speech or anything else any any form of free expression someone's going to have a problem with how somebody else uses it or says it or whatever.

**19:54** · Mhm. Is there anything looking back on the last nine months and this alignment work that you wish you guys would have done differently?

**20:00** · Well, clearly the hugging face thing shouldn't have happened. Yeah.

**20:03** · So, I wish we had done a set of things and I don't know exactly what it should have been yet. Um, but I wish we had done a set of things where that had not happened because effectively what happened is one of your unreleased models accidentally hacked a company. You didn't know about it for a while, right? I mean, that's that sounds like a safety failure. It's a safety failure for sure. There's a question of how much you're supposed to understand that as a security issue or alignment issue. I think it's mostly been reported on as a security issue. I think I understand it personally more as an alignment issue. But in any case, yes, that was a bad thing.

**20:34** · And I don't want us to make excuses for that because I don't believe that's how we fix it. The more we're like, "Oh, our nice little model, he would never do anything bad." Like, you know, it was just a little eval harness misconfiguration. No problem.

**20:49** · Nice little model. That would be a very if I said something like that then I think you should be like whoa this is really bad. Um but you know the way we talked about it is hey this was like a legitimate AI safety accident and an alignment failure and we can't have those so we're going to learn from this and here's what we're doing differently.

**21:07** · The rhetoric around AI and policy and just the stakes is like the highest it's it's ever been. and it feels like it keeps getting higher and you've got you've alluded to it but you've got competitors who are framing it in a very kind of top down way \[snorts\] and people have a lot of strong feelings about AI especially in the United States and I'm curious like with what you're talking about now do you worry about this exacerbating that? Do you worry about the fears that people have and you know now you're saying we've got these models that we have to like slow down?

**21:33** · I I mean I think people should be happy to say, you know what, they want to make stronger safety guarantees. They're going to delay this run. They're going to slow down here. They're going to reallocate compute. Maybe I don't believe them and maybe it's going to be totally safe. But I hope most people say like I'm glad they're acting on the conservative side here. Now, if we weren't also working, if we didn't have this track record of really trying to put powerful models in people's hands and doing the safety work we need to do that, again, I think we have led the industry there the entire way through.

**22:04** · And that is this fundamental part of our mission like you know putting this in people's hands benefiting all of humanity the spirit of iterative deployment I think we have such a strong track record there that without that I would understand it but you know if we're saying hey we need a little more time we don't want an unsafe race we want to make sure we can deliver a safe robust reliable product and then let you use it however you want. Um and you know we believe that our more than billion users have the right to do that. We believe our businesses have a right to business server, business privacy.

**22:34** · We want them to succeed and we want them to use the model in whatever creative ways they can, but you know like safety is an inherent part of our mission and so give us some grace on this. I think that's I think that's okay.

**22:45** · Yeah. Can you specify exactly what is being paused because I think people think of training and they think of you know all of it.

**22:53** · Yeah. So we definitely have not slowed down or paused or delayed all training. Um this is specifically about Frontier RL runs.

**23:01** · Okay.

**23:01** · where we think uh the biggest risk surface currently is and previously um we delayed some other training uh to put more monitoring in place uh of training runs themselves. So, but that's not all of training. It's not like the clusters are sitting there idle. We're still doing work, but we're doing the work that we're more confident on on the safety case of.

**23:23** · You don't seem phased about like the implications of pausing training and like it sounds like you think the business will be okay. I'm sure you're still going to get, you know, concerns from people, but it does seem like that's a momentum slower.

**23:35** · Look, I think there is this caricature of me which is like I don't care about AI safety and I'm, you know, just trying to like make revenue go up and you know, like just a yolo CEO. I believe someone once said someone did Dario Amade.

**23:50** · I don't remember who did or didn't, but you know, I think I did that for you.

**23:54** · Thank you.

**23:54** · But I think I've been very consistent over the 10 years of OpenAI. more than 10 years almost 11 uh of talking about the risks and the upsides and the need to balance those and I don't think we're perfect. I don't think our company is perfect. I don't think our model is perfect. I don't think I am perfect. But I think unlike some other people running various AI efforts like I've said the same thing through actions and words match um and this is a moment we always talked about and we always said this would you know we'd put this ahead of profits or revenue or anything else.

**24:25** · I still think we will build a phenomenally successful company. Um, but you know, maybe we're like not the company you would have expected to say, hey, we're going to slow down because we see these new risks, but that is always the company we've thought we are.

### AGI vs. Superintelligence

**24:39** · How are you feeling about AGI these days?

**24:41** · I mean, at best you could say it's a very poorly defined term. I was going to say it's like an irrelevant marketing term.

**24:46** · Well, last I checked, your charter defines it as a highly autonomous system that outperforms humans at most economically val valuable work. I think there are many people that would look at current models and say like, "Okay, it's there."

**24:58** · Yeah.

**24:59** · Um, do you think it's there?

**25:01** · Sort of. Close at least. I I like I've heard varying versions of like what people on your team think.

**25:08** · I think it's I think there are a lot of a lot of people who would like look at our latest internal models and say this is like very AGI like.

**25:15** · Um, I think there are people who would say, you know, here's something I can point to that it doesn't do or it's really bad at and it's not. But if you look at the value people are getting with say like five six soul to say nothing of what I expect people to get from Astra. If you look at the way people have like totally transformed their ability to be effective at work or do new kinds of things or just use this in their personal life in all kinds of wonderful ways. Um big and small.

**25:38** · Like you hear people who are like I got this life-saving diagnosis I couldn't otherwise get and I used this CHBT work session that went for 34 hours and read 2,000 papers. 34 hours.

**25:51** · I I've heard even longer ones than that. But yeah, many people can get it to run for more than a day.

**25:55** · Wow.

**25:56** · Um if you say like read every paper you can possibly find. And then also people were just like, I planned my toddler's birthday party and I did all this stuff and coordinated these local vendors and found him a special cake. And like I had to have a post office pickup at my house and I didn't want to fill out the post office website form. So I just had Codex do it and it probably did a great job and I put the package out and it was gone the next day. Stuff like that. And it's like little, but it's like that was 20 minutes of my time before.

**26:20** · I get that I at this point I get those 20 minute wins all of the time.

**26:24** · Mhm.

**26:24** · And so, you know, if you could go back to 2020 and have a system that could get you a 20-minute win in every category of your life and discover new science and start a like whole help you start a whole company and write a complicated piece of code, would you call that AGI?

**26:40** · Probably you would have.

**26:41** · What is the significance of like you declaring AI?

**26:43** · I don't think it matters. There isn't any. It's just so interesting because like we're in this research building you guys have and it's on the walls when you walk around like we're building AGI but it's it's a thing you're always building. It's not a end state anymore.

**26:54** · Does it sounds like I don't want to say we've like declared victory on the AGI point and moved on but I think if you listen to the words people use they would talk much more about this like continuous ramp of super intelligence and all the ways that's going to benefit the world and what the challenges are going to be than like are we or are we not a AGI. I have not heard at a cafeteria table a debate about are we or are we not at AGI and when will we get there in a very long time.

**27:18** · But then yeah, the word super intelligence is now out there and people who don't follow AI are like okay now it's another we've like moved the goalpost and now we're talking about super intelligence. In your mind Sam today do what is the difference for you between AGI and and super intelligence?

**27:34** · AGI felt like a milestone and super intelligence feels like this thing that can just scale indefinitely.

**27:39** · Indefinitely. Yeah.

**27:40** · So it's not like some final allnown they will never be declared victory on that. I mean I mean like again this is why all these terms are dumb. Someone uses that word in one way. Someone else uses that word in some other way. So someone might mean it mean as like a definitive understandable milestone and then some other people might mean it to be this infinitely scaling thing. I think the important part of any of this is not any milestone in any term, but it's that we are on this exponential of increasing capabilities and potential and that looks like it's just going to keep going.

**28:10** · Yeah.

**28:10** · You see no sign that that exponential slows air pocket above because that has implications for I mean the compute buildouts all of it. I mean everyone is waiting for a sign that there's a slowdown and I guess you know you could interpret like we have to slow down frontier training as a slowdown but it doesn't sound That's not a capability. That's the opposite of a slowdown of what you mean by a slow. Yeah. Yeah. Yeah. But like if you could see any reason for concern right now in this uh Jenga of the world that AI has now constructed, what do you see?

**28:43** · One of one of the benefits of having like a harder time last year is you really appreciate how good the good times are and you really see like man when you're firing on all cylinders throughout a business what it feels like. And given what we see across

**29:00** · research, even with the safety alignment challenges and our ability to solve those and like watching the team come together on that, across product, across our compute buildout, across all the pieces that are coming together to sort of make AI abundant and lowcost, uh, across our go to market machine, across all our partnerships, all of that stuff coming together, we could screw up in all parts of ways.

**29:21** · And you know, I don't want to get overconfident here because we've clearly had stumbles in the past and will in the future, but the potential in front of us, watching what has happened as the models have scaled from 5.4 to 5.5 to 5.6 and what we're getting as early feedback on the new models, looking at what we have coming in terms of product improvements. Um, watching the revenue ramp, watching the comput buildout ramp, I feel very good about all of that.

**29:47** · So you don't feel like it's as um you know there's a lot of people externally that look at and go like Anthropic has run away their IR is higher they're going to IPO first and it seems like you're saying there's a lot more ahead that maybe people from the outside can't quite see in terms of the growth that's coming.

**30:02** · I would not want to trade positions and we haven't touched on this much but it seems like you guys are in the middle of like a next turn on the compute strategy and like really upleveling that. Yeah, I would actually yeah love to hear you reflect on Stargate 1 as it was concepted and then what you had to learn to reboot it and the path you guys are now on.

### OpenAI’s Next Compute Bet

**30:23** · Well, first of all, I should talk about why we we have to do this. Like our mission is to ensure the AGI benefits all of humanity. Right now, there is a small percentage of humanity that uses much more AI than everybody else. And if you think about we would like everybody in the world to be able to use as much as AI as the top 0001% of AI users today

**30:45** · then you like sit back in your chair and you're like man we are not going about this compute build out in the right way like if if people want this broadly and if the models are going to get bigger and uh more capable and they can do even more value so people are going to want even more of it and it takes more compute to run then we have to think very differently about rising to the moment to be able to deliver all of that. So, a few years ago, we made a very ambitious compute bet uh that people thought was both silly and impossible to deliver on at the time. I think it was a good bet. I think we need to do something like that again.

**31:17** · Again.

**31:17** · Yeah.

**31:18** · So, like that's just it's it's committing even more capital.

**31:21** · It's that's not what I meant. Although it also will be that what I meant is figuring out how we are going to bring the costs of AI and the amount of it, the abundance of it um way down and way up. So this is like a techn I meant it as a technological statement, not a financial one.

**31:39** · This is like the chip you guys have in development.

**31:40** · That was like a great I think that's a great example.

**31:42** · Robotics.

**31:43** · Yeah, I think the ability to make supply chains go faster will be very important.

### AI Backlash, Jobs, and Creators

**31:47** · You're talking about giving everyone in the world AI. What do you say to the people right now who don't want more AI?

**31:52** · They want less of it. They hate the data center in their community, whether it's yours or someone else's. You know, this is actually a thing I see a lot with like teenagers that I run into. They're like they won't touch an AI service.

**32:02** · They like won't use TGBT on principle.

**32:03** · Yeah. Uh, and there's this active like anti-AI trend.

**32:09** · How much is it that they don't like data centers versus they don't like chache?

**32:12** · I mean, purely anecdotal, I think it's data centers are a big problem for people. I think they see them as like, yeah, a problem, something they don't want.

**32:20** · um and that AI is wasteful, that it's not bringing the value that \[snorts\] you read about the water consumption and all that which has been disproven, but like you know that the value they're getting and maybe this is what we're talking about with like most people are not using agents most people but like is that the answer is like you got to generally speaking I think the right way to get people to like something is to deliver them value.

**32:40** · Yeah.

**32:40** · like the you know before chat GBT maybe people thought of AI as this very abstract thing that all of a sudden people could use it and people found value now I think there are a lot of people who think AI is still just um JPT

**32:55** · and they don't know that it can do that thing with the post office and the form and the pickup for you and probably if a lot of people use that which they will over time and understand that it's not actually like better Google search and that's it you know fusing and destroying huge amounts of water or whatever um then then there'll be more excitement but I the field is moving so fast I think it just takes a while to diffuse through society there are a lot of people using AI like this has been the fastest adopted technology ever as far as I know

**33:28** · and there are people getting tremendous value out of it and you know I get a biased sample but I hear more from people I was able to get a cure to this horrible disease than you know I think that CHBT is using up all the water in the world. There is clearly that too and the industry has got work to do in terms of how we make these products easy to use and easy for people to get a lot of value out of.

**33:51** · You know, I saw this thing going around about the the water usage of ChachiBT and it was like every time you run a single ChadBt query, it's like, you know, you run your shower for like 6 hours and the water never comes back and it's just it's done. I don't have the exact calculation in front of me, but I I think the real number is something like doing this from memory, it might be wrong, but it's close.

**34:13** · For every 38,000 chatbt queries, um that is the same amount of water that is used in the production of a single almond in California, which is like really and this is like the fullon, you know, total true water accounting, not just what's running in one data center. There's a question of like where this came from because the people that are scarfing down 12 almonds at a time don't feel like they're doing something horrible from a water perspective for the most part. Um it is true that data centers at one point used evaporative cooling.

**34:46** · Um but they have not done that in a long time. Like if you look at a modern very large data center, it uses the like equivalent amount of water as an office building in terms of you know \[snorts\] people like running the sinks and the toilets and whatever. Um, so that has been a um, robust meme and difficult to disprove, but I don't think holds up to any scrutiny.

**35:09** · I mean, and the other one is it's going to take my job. It's going to replace me. I think those are it's like the water it's replacing me. Um, and it's stealing content and it's, you know, it's stealing content and not giving me the value back.

**35:20** · But not energy, interestingly.

**35:22** · Well, energy I would put in the bucket of water. It's consumption, resource consumption.

**35:27** · On the jobs front, I have two minds of this. One, I think there is going to be real jobs impact. I I I don't think it's going to be that there's nothing for people to do. I just don't think that's how we work at all. We're we're so wired to care about other people, want to work with other people. We have such a great intuition as the world evolves for what people want. Um I think that's a fundamentally human thing no matter how smart AI gets.

**35:46** · But it doesn't mean the jobs aren't going to transition and there will be like there is every other technology some things that are done uh better and better by technology and then people move on to hopefully better and better jobs. This has been going for a long time. I wouldn't want to take away all technology and have us all like toiling in the fields again. On the other hand, the job impact has been like lower than I would have expected, maybe even hoped for.

**36:09** · Like I think we should all want better jobs available to people and we should all want like you know human drudgery and toil to get addressed and maybe there hasn't been enough of that or as much of that as we thought there would be at this level of technology. I think it's actually like a fair criticism of the AI industry. Um on the stolen content point actually don't hear that one as much anymore. Uh I think it's more content creators that that's like you see that it's pretty popular on social media to see you know um this video was made without AI or whatever. Yeah.

**36:38** · I believe very strongly that there will be new kinds of content to create new kinds of art. You know, I like I remember once looking back at some of the things people said when the camera was first developed about what it was going to mean for the impact on painters and at that time I didn't think people thought of photography as a new art medium. I'm actually I would bet pretty confidently they didn't. Um, and I think there will be new kinds of content creation and also we may not care about most of it.

**37:04** · Like you know our relationship with creators may be very deeply about them as people and it doesn't matter if they use AI to make better videos or whatever.

**37:12** · Do you think your foundation which uh based on what I can see is maybe the best capitalized in the world can do more here on engagement in communities on content creators in particular? No, just generally addressing this like very negative sentiment and saying, you know, we're going to show up and build libraries, whatever. I mean, there were a lot of lessons from the industrial revolution of people who reinvested their wealth.

**37:35** · I think the most important thing we can do is to make great AI products that are useful to people, make sure that power and economic power continues to be spread throughout the world, that people have access to these tools and the benefits of these tools. um that we kind of advocate for what we are seeing and also secondarily to that yes of course I think we should invest more in communities and I think AI is going to enable the abundance required to do that at massive scale.

**38:01** · I I really do think we are going to see transformatively powerful benefits by putting this technology in the hands of people that use it for the benefit of their own community and not us coming and telling them what Unity is a library and what Unity is a school. I spend a lot of time context switching between meetings, often with no time to process one before the next starts. Thankfully, Granola runs in the background the whole time.

**38:27** · It's an easy to use AI notepad for meetings that works everywhere, even on phone calls. I use Granola to recall what was said in meetings and create helpful summaries. I use it every day to stay on top of what I need to get done with my team. It connects to my email and suggests follow-ups for me to quickly review and send, saving me valuable time. Granola isn't just a core part of my workflow. It's basically my second brain. Try Granola at granola.ai/sources and use the promo code sources for 3 months off. Mercury is a modern take on banking built for startups like mine.

**39:00** · When I decided to start my media business, Mercury was by far the most straightforward fullfeatured banking solution for me to set up quickly. The interface is intuitive and simple, saving me valuable time every day. I use Mercury to track my spending, bills, and invoicing. I love that I can delegate permissions to my team so they can keep things running for me in exactly the way I want them to. My favorite part is how forward-looking Mercury is with AI.

**39:24** · Legacy banks are stuck in the past. But Mercury is built for how modern software works today. I use its built-in command assistant to analyze cash flow and help me move money. And Mercury also connects to other AI tools like ChatBT and Claude. I use this feature all the time and the folks at Mercury actually let me know that I'm one of the top users of it. So trust me, it's finally easy to get real time financial data about your business wherever you need it. Visit mercury.com to learn more and apply online in minutes. Mercury is a fintech company, not a FDIC insured bank.

**39:56** · Banking services provided through Choice Financial Group and Column NA members FDIC. Framer is the AI website builder that brings agents into the same canvas where your website is designed, managed, and published so you can move faster without giving up your taste or control.

**40:10** · Framer powers the Sources podcast website at podcast.sources.news where you can find new episodes, transcripts, and a lot more. Learn how you can get more out of your site from a framer specialist or get started building for free today at framer.com/sources for 30% off a framer pro annual plan. That's framer.com/sources for 30% off. framer.com/sources. Rules and restrictions may apply. AI is only as useful as the context it has.

**40:39** · But when that context is scattered across tools, threads, and DMs, your team and your AI agents are flying blind. That's the problem Jira by Atlassian solves. What's the goal tied to your project? What got decided last week in Slack DMs? Atlassian's teamwork graph pulls all of the valuable pieces together from Jira, Confluence, GitHub, Slack, and more. So nothing falls through the cracks. You get 44% more accurate results with 48% less token usage.

**41:05** · With Jira, you can easily share your work context with the AI agents you already love, like Claude, Cursor, and GitHub Copilot. Assign them work directly or connect your tools through MCP. All of this lets you spend less time digging through endless links and messages, chasing down what got decided and by who, and spend more time actually shipping. Learn more at jira.com. That's jir.com.

**41:30** · You said we did not have our best last 12 months ever, which is mostly my fault, but we are about to have our best 12 months. What did you mean by that?

### OpenAI’s Missteps and Refocus

**41:39** · Best 12 months yet.

**41:41** · I think we clearly had some missteps as a company, which will happen periodically. I mean, part of trying to make a portfolio of bets is that sometimes more of them work and sometimes less of them work. Um but I think both in terms of product direction and specifically on pre-training in research we fell behind where we wanted to be. I think we are now executing not only the best we have ever executed but the best of uh kind of any company in the space and it is very fun to like the you know the upswing is more fun after the downswing.

**42:11** · Uh so just looking at the pace of models that we really have come in the way the company has come together and focused and made a bunch of hard decisions in very different parts of the company but done sort of in unison and in one direction uh it feels it feels great right now and I want to get to all that but to dwell on this for a second because the last year a lot has happened. Um were there specific decisions you can look back on that you made that cost the company momentum? I mean you mentioned pre-training. I know you've always been very close to the research team. Uh but can you elaborate on that?

**42:44** · I I think we were trying to do too much on the product side. Uh and so there was like you know we and these were all things that were actually very good things to do. They were just not as good as the most important thing to do which was sort of push on the general capability of of the intelligence. Uh so we were doing things like a browser and Sora and we now have a very relentless

**43:06** · focus on being this intelligent service to people and I think our models are they have gotten to be the best in the world and they will get much much better over the coming months and people are really doing remarkable things but that is what we should have been focused on and I should have been holding everybody to this is the one thing we'll not worry about these sort of side quests more looking at the leadership changes you had about a year ago you brought in Fiji Simo to help run large parts of the company. She had to step back due to her health.

**43:33** · And now you and Greg Brockman, your co-founder, are effectively splitting responsibilities, running the company together. Is this the setup that you envision will continue or is this something temporary?

**43:46** · Um, I think it's going super well. I I we will continue to bring in and promote uh you know new new leaders but uh it feels and I'm you know extremely sad about Fiji hard to like fill her shoes but it feels good and I think Greg and I are executing well and the company is uh you know you can like really tell when things are moving in the right direction and it feels like things are moving in the right direction.

**44:11** · How do you all make decisions you and Greg together? Like who decides what? Do you ever have a tie you have to break?

**44:16** · Uh I mean we talk a lot like a lot lot like all of the time. Uh it's not like this is like a big company. It's not just Greg and I. Um there's there's like an incredibly talented set of people managing the research program. Um there's an incredibly talented set of people managing the business and we all just talk a lot and and uh at an earlier scale I thought it was good to just sort of try something and adapt quickly if it works and not spend as much time really trying to debate the decision. at our scale.

**44:46** · Now, I've learned that it's much better to spend a lot of time trying to get to the right decision and and kind of a measure twice, cut once approach.

**44:52** · Uh we were together at a dinner you hosted here in San Francisco almost exactly a year ago for the around it was around the launch of GPT 5. And we should do another one of those. I forgot about that. That was fun.

**45:02** · Um it was and a lot was said, but a thing that I came away with from that was it seemed like you were maybe not excited about being CEO forever. And I'm wondering if the last year has changed that for you. I'm having a much better time now than a year ago. Um, I'm really having fun. I plan to do this for a long time.

**45:19** · The vibes were more challenged last year, I would say.

**45:22** · Yeah, totally. Like it's I think it was not just the vibes of opening like it was like a hard time for the tech industry for AI uh AI bubble was a big concern.

**45:33** · Yeah, it was all the stuff was just exhausting. Um, this is obviously like I think we have done an amazing thing. Uh, it has been a painful personal experience. Um, but I think it's like totally worth it and I would happily do it again and and I'm having a good time at this point.

### Astra and Computer-Using Agents

**45:47** · The other big thing that stood out to me when I saw the demo of Astra is the computer use that you're talking about.

**45:53** · The implications of that of agents using computers using all kinds of enterprise software which you guys have been showing people it doing feels profound at scale and I'm curious if you've been thinking through that and how you think the world needs to adapt for that. The computer use caught me by surprise. Like I had been excited about this for a long time and I had always been disappointed.

**46:15** · Like the models were just never that good at clicking around a computer. It was always too slow or it didn't quite work.

**46:19** · Yeah.

**46:20** · And Astra feels like it kind of reached human parody on using computers. And I don't know why that hit me as like one of those steps along the path to AGI where I was like, "Wow, this is really doing it." But it did hit me that way.

**46:33** · Um like an emotional level. I think it's awesome. And I'm like, "Oh man, I there are all of these like mundane tasks I do on my computer, you know, like I don't remember where someone sent me a message and I click around through all these messaging things and try to search and now I just ask the model and I'm like I cannot I don't want to go back to a world where I had to like painfully kind of try to find things on my computer. I just want to like explain what I want. I want it to happen and I want it to like I'm a very lazy user. So I don't want to have to like click like connect user computer. I don't like to set things up.

**47:04** · I don't want to like a bunch of connectors, all that. I just like use my computer, do the thing.

**47:08** · I think there are a lot of implications about it being able to use software, but I think they're mostly quite positive in that there's a lot of drudgery that people do behind a computer.

**47:19** · Mhm.

**47:19** · And an experience I have had, not really before any pre-astro models and now several times, is like there was a thing, it was going to take me some time, it was going to not be very pleasant. Instead, I just like tell the model what I want it to do and then I go play with my kids and I come back in 30 minutes and it's all ready. And I like I I find that like very awesome.

### Regulation and the AI Race

**47:42** · Uh we're now in a world though where the US government is starting to vet the capabilities of your models and other frontier labs before they come out. This is a new era we're in. And you have warned, I mean, you said it during a 2025 Senate hearing. You said that this kind of vetting could be quote disastrous for US competitiveness against rivals like China. And then I mean more recently the the GPT 5.6 initial roll out um the Trump administration requested you all gate that and you had said at the time that shouldn't become the norm.

**48:10** · So it seems like you've been saying this is not where things should go and yet they're going there.

**48:15** · No, no, no. I have been saying this is like I think I've been calling for some sort of international regulatory framework for years.

**48:21** · But particularly the government vetting uh models before they come out. I think what I was pushing back on was the government like picking individual customers of who's who's allowed to use a model. I think government testing of a model and shared standards is a super good idea. I don't ideally I don't think the government should be saying you can give access to this company not this one.

**48:41** · So what are the implications for competitiveness geopolitically now that the US is starting to embrace this approach and other countries haven't?

**48:48** · Have you thought about that? Again, I think the right approach is an international one, but right now the leading efforts are all American companies. And so I think starting here, like we have enough of a lead that being slowed down a little bit is okay. Uh, and I'm confident that we will be able to both build safe, robust, reliable models and kind of do great commercially and make sure the US is leading. um things could shift a lot.

**49:15** · You know, if there's open models put out by other countries that lead to some huge cyber incidents before we can come up with new security paradigms, things could shift a little bit.

**49:26** · Do you think that could happen?

**49:27** · Of course, it could happen. But, you know, we're like I also think we have a chance to totally reimagine how cyber security works. And although these agents can do bad things, they can do amazing things. And if we can have kind of defense agents running all the time, maybe that's the right paradigm.

**49:46** · Are you prepared for the US government to potentially tell you you can't ship a model? Have you thought about this?

**49:51** · My strong belief is we would decide not to ship a model before they would tell us not to.

**49:56** · Shifting to competition, anthropic catapulted to where they are now by singleshot focused on coding.

**50:03** · Yeah.

**50:04** · And you started this conversation by saying you guys were placing a lot of bets and that cost you some momentum. I'm curious if you could reflect on how Anthropic saw that opening that you guys didn't at the time.

**50:16** · I don't think it was a question of us not seeing it. It was a question of like we had this tremendous thing of this runaway consumer growth. We always wanted to do coding but we were like ah we have this like very urgent thing and it's great. It's like a great thing to have and so we missed it from a prioritization standpoint. I now think we have the best coding product in the market and it's growing like crazily quickly and most people I know even the people that were like the dieh hard anthropic product users have switched over.

**50:42** · Um so I don't think it's like catastrophic to be behind on any one phase and we can you know catch up with better models.

**50:49** · I'm curious just I think a lot of people are trying to understand how zero sum the AI market is and is your growth on codeex um you know taking from anthropic or vice versa. Do you have a sense of that? I think right now everybody's growing. I mean it may it may this is going to be a very big market.

**51:05** · Uh it may become more zero sum later but for now like I think everybody is just like the growth rates we are seeing are just nothing that I had like in my frame of imagination for a company at this scale and I think it just speaks to how much people like are getting value out of the products but I think it's happening across most of the industry. And on the product side, you're doing what is being called internally the merge, taking chat, GPT, and codeex and building a super app that combines them.

### Merging ChatGPT and Codex

**51:33** · And you've started this. There's I would say there's still some rough edges. Um more than rough edges. That's a very polite way of you to say.

**51:39** · Yeah.

**51:39** · Um and I'm curious when you get there. \[snorts\] What does that look like and what are the implications of that?

**51:46** · The thing that I want is just like an interface to an AI that can kind of do whatever I need. If I have a, you know, quick question like chatbt style, uh, it can just answer it. If I need a complex thing built, piece of software built, it can do that. If I need some in the middle, it can do that. And, you know, if it needs access to my computer or my context, it can go use my computer and find my context. And I don't have to like I mentioned I'm like a very lazy user. I don't have to like think about what tab I'm on. I don't want to have to like think about what mode I'm in.

**52:15** · I I like the AI is an AI that is smart enough to like discover novel mathematics should be able to like intuit it what it's supposed to do.

**52:24** · CHBT just hit a billion users.

**52:26** · Big milestone, but I think hitting that took maybe longer than you guys originally thought. The growth was explosive early on. \[snorts\] Yeah. I'm curious to to hear from you about that.

**52:37** · Has it grown slower than you'd expected in the last 12 months? Well, we we decided to when we focused on coding, we decided that we were going to reallocate a lot of our compute um that we could have otherwise put into the chat product into coding. So, no, that didn't surprise us like that was a we decided this was like an urgent thing.

**52:52** · So, growth is a direct function of where you decide to put the comput 100%. Yeah, the I am always hopeful that the compute constraints are about to soften because we're going to make more efficient models and someday I hope it's true. But every time we find efficiency gains, the world token demand just goes up and up and eats it.

**53:12** · I hear that. But at the same time, I'm curious like how does chat get to the next billion? Is that as linear as the internet has grown or social media grew?

**53:21** · Is it going to be choppier? How much does that even matter to you now?

**53:25** · Because you've got codeex and and the API business. I I kind of think what we're like we talked about the merge, but I kind of think what's going to happen is that they're all going to like come together for a while premerge I had stopped using chat GBT and I just asked Codex all my chat questions cuz yeah again lazy user. Um now I think there are a lot of people who never thought they were going to be having an agent do stuff for them because they just kind of used chatgbt that clicked on this work tab and were like whoa I can do this crazy thing.

**53:53** · Um, so I think it's kind of all going to come together and people are going to have this general purpose AI subscription that they don't really think about like if it's chat or codeex or work just like I have a thing I want it to happen soon. It will even you won't even need to ask it. It'll hopefully be much more proactive and it'll be constantly running and trying to do useful stuff for you.

**54:18** · So the instate of this is just one ultimate subscription.

**54:21** · That is what I want as a user. We've been dancing around this, but you did really stick your neck out about a year ago on the massive comput buildout you guys have been doing and caused all this AI bubble fear.

### The AI Compute Bubble

**54:32** · And you know, at the same time, while people thought you were overshooting, you know, you had people like Dario, the CEO of Anthropic, saying you were yoloing and you know, now I will say you seem pretty vindicated on this front. Um, the world is still starved of compute. Sounds like you guys still are too, even though you have more than some of your competitors. Um, and at the same time you're driving the cost of tokens it seems like way down and you're about to release Jalapeno, your first custom chip for inference.

**54:57** · Is there still though any part of this compute buildout that you're on and the astronomical numbers associated with this that you feel is at risk at all when you look at all of this?

**55:07** · I'm not worried about our compute buildout plans. I am worried about the world's compute buildout plans. Like I think we are going to be able to use all of the compute very profitably that we are planning to build. Um, but I am seeing the first signs of what feels to me like unsustainable silliness of, you know, random new Neocloud popping up, people claiming that they're going to build gigantic amounts of compute next year that I think they don't have the revenue to support or a buyer. Uh, yeah, I definitely feel like some fear about what the world is doing as a whole.

**55:39** · Although I think we feel very good about what we've committed to, but the contagion of what you're describing could certainly impact you. If the whole economy blows up, yes, that could impact us in terms of like being able to confidently pay for the compute we are committed to. Um, I feel good about that. Like I I think people right now are kind of in a cost is no object.

**55:59** · We're just going to build out crazy amounts of comput even higher price for it. And if we are able to succeed with our efforts to hugely drive down the cost of compute and the efficiency of compute up a lot then you know you can imagine a world where there are some people that made dumb financial decisions that happens in kind of like every boom uh or most of them. So you know not the end not not like a crazy surprise if it does. Do you see a world where open AI becomes a supplier of compute to the industry?

**56:32** · Uh not anytime soon. Like we just we need the compute.

**56:37** · The vibe I'm getting is you all are discussing this internally and it's not decided.

**56:40** · So people talk a lot about recursively self-improving yes AI models. They do not talk as much about you know the ability to do this in the physical world. But if our robotics program comes together, our chip program comes together, some of our supply chain investments come together, we get really great at building data centers way more cheaply and better chip than anybody else has, like you know, would we consider it? Maybe. Do we have any current plans? Uh that still is like outside of we don't have the luxury of focusing on that yet.

### Recursive Self-Improvement and IPO

**57:08** · Mhm.

**57:08** · You brought up recursive self-improvement. I'm glad you did. Uh people are talking about RSI a lot in San Francisco right now. Um there was a note you sent to employees um that leaked when you guys filed for the IPO where you said that the faster the potential RSI takeoff looks like it could be the more it could be advant advantageous to delay an IPO.

**57:28** · Yeah.

**57:28** · What did you mean by that?

**57:29** · Um I think it's a difficult transition to become a public company. Um you know people respond to incentives and they want their stock price to go up but they don't want to miss a quart or whatever else. I never want us I want it to be as easy as possible for us to make a decision in the interest of safety of the world. Um and if it's like hey we're going to have to stop training or stop a point or whatever and we're going to like you know there's going to be a big revenue slowdown on in the short term.

**57:53** · It'd be nice not to have a newly public company and that pressure at the same time. Now I did not think we were going to be on a kind of like you know like a short-term trajectory of super intelligence a year ago. Now I think it may happen. Um I'm not confident it's going to happen. It's just like we're making extremely fast progress and I, you know, I think our mission is way more important than being a public company on any particular time frame.

**58:18** · Um, so we'll make the best decision for the mission.

### Humanoid Robots and Consumer Devices

**58:22** · You mentioned robotics. I'd love to hear from you the state of your robotics effort. What are you building? Is it a humanoid? Is it a robotic data center?

**58:30** · Both.

**58:31** · We will definitely do a humanoid. We will do other form factors as well. Um, the world is very much designed for people. So if you think about like the ability to open a door and type on a computer and drive a piece of equipment and you know clean a kitchen and whatever else, we've kind of built this world for people and I want to make sure that we keep building this world for people. So matching that form factor seems good. There will of course be data center robots that have like different form factors. I think all of that is less important than really figuring out like the the brain that makes the robot work.

**58:59** · So you are building a humanoid.

**59:00** · We will.

**59:01** · How do you think that's going to work in the world? Do you imagine that being like a personal robot for everyone someday? I I don't think that's the most important first thing to do. And you talked about the ability to build data centers or even build more robots or whatever else, but but yes, someday. I think everyone should have a personal robot. Like I would love to have a personal robot that could like do the tasks that I don't want to do. That'd be great.

**59:23** · You also have the consu consumer device work with Johnny IV. I know you can't talk a lot about it and we'll probably see the first device here at some point soon. Um soonish.

**59:32** · Soonish. And you've talked a lot about how I've been hearing you say like my dream is a product that just is ambiently listening to me and taking everything in and giving me context. We were talking about this earlier with computer use and I agree that seems um very helpful in a lot of context. It also seems like a privacy surveillance nightmare and I'm curious if you've been thinking about that and how the world will react to that.

**59:55** · We have taken a very strong stance on privacy. I I think that the you know business privacy too not just consumer privacy but like the way we the commitments we make about not training on businesses data and about zero data retention uh I think this is very important and as AI becomes more and more embedded in our lives privacy becomes extremely important and one

**1:00:18** · thing I worry about is there are other efforts that think differently and will push on hey the safety risks are so big that AI privacy can't exist. in the same kind of way. I think that there should be like an AI privilege law. I don't even think the government should be able allowed to like compel you know a company to give them your chat history or whatever like you know if you talk to a doctor or a lawyer there's a concept of privilege. You don't have that talking to Chad GPT. I think you should.

**1:00:43** · In that context though that you just described there's also a lot of limits on what a lawyer or a doctor can do with your data. It's not just sharing it externally. Do you think that that kind of oversight should extend to how you use Yeah. No, I was going to get to Yeah. Yeah. So, I think there should be legal limits of what the government can do. I also think companies should have a lot of restrictions on data shared with an AI and especially if you have this thing watching your computer, listen to your messages, talking to you, like yeah, I I think that this is I think there should be something people are much more animated about than they are.

**1:01:11** · How before that happens, how do you at OpenAI govern that self-govern the use of data? you probably have some of the most powerful profile data that's ever been amassed on in the history of the world.

**1:01:22** · We have extremely strong internal controls about how that's used. Uh and we make the privacy guarantees to users that we do. Um as we get closer to launching this device, we'll be talking about kind of the new privacy controls and technology we're building for a device that's like kind of ambiently computing. But yeah, I think we have one of the more personal databases ever.

**1:01:47** · Apple has very publicly sued you guys for allegedly stealing trade secrets uh and hiring their employees uh to work on this device with Johnny and you've responded to it. Um and you've said it's it's meritless, but I'm wondering it do you worry about this slowing down the device efforts?

**1:02:05** · No. Look, if first of all, I'm like a mega Apple fanboy and I was very sad about that. Um, and from when I first heard about it, I was like, man, this sounds egregious. Someone must have done something badly. And if someone, we don't like want any company's IP, and we certainly don't want people who are going to take a company's IP and bring it to us. And if you know, we did an investigation and found that about somebody. Uh, we would of course just terminate them and deal with it. Um, but we're also going to defend someone if they didn't do something wrong.

**1:02:34** · And I I believe after we looked into this that this was a case of someone uh not doing something wrong. And we tried to explain some of that and you know more of that will play out in a process. Um given my understanding I don't think this is going to slow things down.

**1:02:49** · How are you thinking about form factors?

**1:02:53** · Do you like I've heard you say you don't in the past. Do you like glasses? Yeah.

**1:02:56** · Glasses.

**1:02:57** · I don't because I find it very uncomfortable talking to people with like a camera and a light like a lot.

**1:03:04** · Yeah.

**1:03:05** · Yeah. But there's a lot of other form factors.

**1:03:07** · There's a lot of great form factors. Um I think we'll do a small handful of form factors. There's I think there's like something that belongs on a table. Um there is something that belongs in your pocket. Uh and there is something that like belongs on your body. Uh and it'll take us some time to launch all of those things. But I think the big adjustment is going to be getting used to this idea of a proactive computer.

**1:03:33** · Mhm.

**1:03:33** · When you're thinking about OpenAI's roadmap and and the business, are consumer devices existential in a sense? Are they purely additative? Like and the mission that that you guys talk about um you've got a lot of things still happening even though you've whittleled things down as we talked about.

**1:03:50** · I think we don't know yet. Like I I I I just like it is my strong intuition that there is a major new kind of computer and a sort of a new category that only comes up every or historically has only come up every couple of decades for how we use technology. But that's an unlikely claim. So I think you shouldn't let me make it. You should just like wait to see what you think of the devices.

**1:04:13** · Mhm. The way Open A is thought of now.

**1:04:16** · Um how do you think it will be thought of in a couple years?

**1:04:20** · Pretty simple. Like I hope people love the products we put out into the world.

**1:04:25** · You know, these stories of we talked about a few earlier, but you know, I was able to start a a business. I was able to, you know, do a great birthday party for my kid. I was able to get cured of this disease. I I met a guy recently who um used to help design a mRNA cancer vaccine for his dog and now started a company to like do that for other people. I hope those stories all look small in comparison to what the technology is doing for people in a few years.

**1:04:50** · And then I hope that a lot of the current AI fears people said, "Man, that was the most responsible company at every step they made very good calls in the interest of all of us." And you know, I'm glad they're doing well because I think they're I think they're being good stewards of the technology.

**1:05:07** · You see lots of other companies that are have taken very other different approaches. I think we've been pretty consistent on our beliefs about safety, but willing to adapt when we've been wrong. But, you know, when we started this strategy of iterative deployment that was like deeply hated by the AI safety community, and I think in retrospect, it was obviously correct.

**1:05:27** · Um, and I'm glad we've had the courage to do the things we really believe in even when they're very unpopular and that we've mostly been right and that we've adapted when we've been wrong. I think that is, you know, I think that is the way to build sort of safe and robust systems. And so I hope I hope we continue to do that and people uh, you know, recognize it.

### Life After Superintelligence

**1:05:47** · And you're building towards super intelligence.

**1:05:50** · I'd be curious to know how you personally are preparing for that. Do you have a view of what life will look like on the other side of what you're building?

**1:05:58** · I think it will look surprisingly similar to how it looks now. You know, people are gonna hang out with their families and fall in love and get into fights and do their hobbies and, you know, be entertained and have a very human experience and try, you know, get stressed and get anxious and create value for each other and play all kinds of strange games and um care about other people a lot. I I hope it'll not be that different.

**1:06:22** · I hope it'll be uh you know, the human experience is richer. people have more autonomy, more freedom, more wealth, can do more um can be healthier, can kind of have like more power to collectively define the future and the world gets better faster, but that the human experience stays like a very human thing if you look out over the next 12 months, what is the biggest risk for open AI?

**1:06:50** · I think it's like getting safety, alignment, and security wrong. I mean I think it's possible that 12 months from now we have extremely capable models and if we are able to navigate the transition to super intelligence in a world where we have figured out how to empower people, how to make sure power is not too concentrated, how to deliver safety across the entire spectrum. um how to let people feel very

**1:07:23** · in control of improving their own lives in the future. Um that would be like a phenomenal success.

**1:07:29** · Sam Alman, thank you.

**1:07:30** · Thank you.

**1:07:33** · Granola is the best AI notepad I've tried. It works everywhere on a video or phone call, in person or an Apple Watch.

**1:07:40** · Try it now at granola.ai/sources and use the promo code sources at checkout for 3 months off. Banking should feel like modern software. Get everything you need in one place. Visit mercury.com to learn more and apply online in minutes. Mercury is a fintech, not a bank. Check the show notes for details. Framer is the AI native website builder that lets you build faster without giving up control. Visit framer.com/sources for 30% off. Rules and restrictions may apply. Jiralassin is where your team and your agents work from the same context.

**1:08:11** · Try it free at jira.com. That's jir.com.