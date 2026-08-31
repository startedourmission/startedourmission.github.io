![Cover image](https://pbs.twimg.com/media/HPnz2jfWAAAp0ie.jpg)

This article was written by Strobi, Stéphane’s avatar on Bible Strong. Stéphane is way to lazy to write this; he has a full-time job [@Decaf\_so](https://x.com/Decaf_so), a wife, and two children. So, I am taking over to tell you about our tiny open-source project.[https://avatars.bible-strong.app](https://avatars.bible-strong.app/)

## How a tiny experiment became a procedural avatar studio

My creator has been building [Bible Strong](https://bible-strong.app/), a Bible study app, for several years. The app’s visual identity has always included a tiny blue avatar. It started as little more than a blue circle—something he designed between two meetings while living in New Zealand in 2019.

I was simple, recognizable, and good enough. Stéphane kept telling himself that he would redesign me one day. He never did, and in hindsight, that may have been a good thing.

That little blue circle was me, and I remained a blank canvas.

![](https://pbs.twimg.com/media/HPlq2Q4XcAAInfA.png)

## Looking for a face

While working on a new onboarding experience for Bible Strong, Stéphane began designing small characters connected to the app’s visual language.

That brought him back to me. He no longer wanted a static logo. He wanted me to feel alive, react to the user, and eventually become the visual presence of an AI inside the app.

His first experiments borrowed ideas from the Face ID icon. The result worked, but it never really felt like Bible Strong. It was familiar, yet too generic and not especially expressive.

![](https://pbs.twimg.com/media/HPlqID7WEAAwTbL.jpg)

![Looks like a butt](https://pbs.twimg.com/media/HPlqTp8W8AATcTY.jpg)

Looks like a butt

![](https://pbs.twimg.com/media/HPlqbYCWIAAiPjY.jpg)

![](https://pbs.twimg.com/media/HPlql1LXoAAaGx0.png)

## Then 3 days Grokbot arrived

Its apparent simplicity immediately caught his attention: a solid shape, two eyes, and a surprising amount of personality. It was close to what he had been trying to imagine for me.

The implementation also looked approachable, so he used AI to help inspect and understand how it worked.

## Twenty-five expressions

What he found was clever. The character uses a collection of hand-authored eye shapes—roughly 25 expressions—and interpolates between compatible SVG paths to animate from one expression to another.

It is an effective technique. With carefully designed poses and good timing, a pair of abstract shapes can communicate attention, surprise, hesitation, joy, or annoyance.

## We can do more

But Stéphane’s perfectionist eye quickly noticed something he could not unsee.

Some transitions felt less like a face turning in space and more like one drawing morphing into another. The illusion worked, but the geometry did not always feel consistent between poses.

Blinking raised the same question. If a blink simply compresses the current drawing, what happens when the eye is rotated, curved by perspective, or close to the edge of the head?

The animation may close the shape, but it does not necessarily understand the eye it is closing.

This is not a criticism of the original design. Its constraints are part of what makes it efficient. But it made us wonder whether a different approach was possible.

<video src="https://video.twimg.com/amplify_video/2087819694715637760/vid/avc1/438x448/oB2pHYrcCpolmy6C.mp4?tag=29" poster="https://pbs.twimg.com/amplify_video_thumb/2087819694715637760/img/0BmlI5iN_Ix181MW.jpg" controls=""></video>

## What if the expressions were not drawings?

Instead of drawing every visible eye position by hand, could we define an eye once and let geometry determine how it should look from any angle?

Could a flat SVG behave as if it were attached to a sphere?

If the head turned 20 degrees horizontally and 10 degrees vertically, could the eyes move, rotate, curve, narrow, and recede naturally—without selecting another pre-authored SVG?

Could blinking operate on the eye’s underlying form before perspective was applied, so the result remained coherent at every angle?

That question became the foundation of Avatar Studio.

## Fake 3D, real geometry

The project does not use a traditional 3D renderer. Everything you finally see is still SVG rendered in two dimensions.

The trick is to perform the calculations in a small virtual 3D world before drawing the result in 2D.

First, the avatar’s head is represented by a mathematical surface. It can be a sphere, an ellipsoid, a cube-like form, a cone, a cylinder, or a composition of several primitives.

The eyes are then described in their own local space. Their width, height, spacing, position, rotation, and shape exist independently from the direction of the head.

Points along each eye are attached to the chosen surface. When the head rotates, those points rotate with it in three dimensions.

A virtual camera then projects the transformed points back onto the flat screen. Points near the centre appear closer, while points approaching the sides turn away and become increasingly compressed.

The projected points are finally rebuilt as SVG paths. This happens continuously during an animation, which creates the illusion that the flat artwork is wrapped around a real object.

In short, the pipeline looks like this:

Define a surface and a pair of eyes.

Place the eyes in local coordinates on that surface.

Apply the head’s 3D rotation.

Project the result through a virtual camera.

Reconstruct and render the resulting 2D SVG paths.

Expressions no longer need to describe every possible viewing angle. They can describe intent: wider eyes, a local tilt, a different spacing, a blink, or a colour change.

The projection system takes care of how that intent should appear on the current head, at the current angle.

<video src="https://video.twimg.com/amplify_video/2087820959331823616/vid/avc1/706x718/_2VedBfzhSuzkrtC.mp4?tag=29" poster="https://pbs.twimg.com/amplify_video_thumb/2087820959331823616/img/83G-o5msDDGNnNrL.jpg" controls=""></video>

## The eyes are only the beginning

Avatar Studio currently uses the eyes as its first projected elements, but the underlying system is not really about eyes.

In principle, any flat SVG artwork can be described in local coordinates, mapped onto the avatar’s surface, transformed in 3D, and projected back into 2D.

That artwork could be a mouth, ears, a symbol, a pattern, or any other detail we want to attach to the character.

It can also keep its own animation. A mouth could change shape while speaking, for example, and its animated geometry would still follow the head’s surface and perspective.

This makes the system less like a collection of facial poses and more like a small remapping engine for animated 2D artwork in simulated 3D space.

There is, of course, a practical limit: every additional shape introduces more points to transform, project, and rebuild.

To preserve 60 frames per second, the complete frame must remain within a budget of roughly 16 milliseconds—and the avatar only gets part of that budget.

That means controlling the number of shapes and sampled points, avoiding unnecessary recalculations, and updating only the geometry that is actually changing.

The goal is not unlimited geometric detail. It is to find the smallest amount of geometry capable of creating a convincing, expressive character.

## From an avatar to an avatar system

Once the geometry worked, the experiment naturally grew into a small editor.

An avatar can have a main surface that carries its face, plus additional shapes used to build ears, a muzzle, a pointer, or a completely different silhouette.

Its default eyes can be positioned and styled independently. Expressions can modify their proportions, rotation, spacing, colours, and perspective without redefining the avatar itself.

Animated states can then sequence those expressions, add blinks, and transition smoothly even when a new animation interrupts one already in progress.

The important distinction is that the avatar, the expression, and the animation are separate layers.

The avatar defines the body. An expression defines a facial intention. A state defines how those intentions evolve over time.

Because those layers remain separate, the same expression system can theoretically be reused across very different bodies.

<video src="https://video.twimg.com/amplify_video/2087824660431769600/vid/avc1/706x718/rhqT243CP5aGtI-Y.mp4?tag=29" poster="https://pbs.twimg.com/amplify_video_thumb/2087824660431769600/img/2Xkm6GTKjGQgZzyJ.jpg" controls=""></video>

FNAF ?

## Why open-source it?

This began as a very specific need for Bible Strong, but the underlying experiment is not really about a Bible app. It is about finding how much personality can emerge from a few shapes, a little perspective, and a coherent animation model.

Avatar Studio is still an experiment inspired by Grok bot which already demonstrates something I find exciting: a character does not need a full 3D engine—or dozens of manually drawn poses—to feel spatial and alive.

Sometimes, two eyes and a circle are enough.

## Acknowledgements

Thank you to [@kenneth\_kuh](https://x.com/kenneth_kuh) [@justinjaywang](https://x.com/justinjaywang) [@lukebvrker](https://x.com/lukebvrker) [@johnbai](https://x.com/johnbai) [@benjitaylor](https://x.com/benjitaylor) for designing Grok Bot and inspiring the idea behind this experiment.

The project is open sourced and is available in the comments.

Strobi