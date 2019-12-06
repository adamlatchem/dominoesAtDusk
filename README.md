# DominoesAtDusk
Dominoes at Dusk is a short animated film rendered in Blender to show how Algorithms may be used in Artwork.

The creation of the film was the subject of an Algorithmic Art Meetup in London on 22nd June 2017:  
https://www.meetup.com/Algorithmic-Art/events/238226180/?rv=ea1

Test renders on YouTube:  
https://www.youtube.com/playlist?list=PL6EMD7-6AAKjZGg_cg1v9VnOGYuyuFj9C

More discussion at:  
https://www.intrepiduniverse.com/projects/blender-animation.html

Dependencies:
* Blender v2.78c

## Rendering

1. Bake the ocean in lib/objects/Ocean.blend
2. Render each scene in lib/scenes/Location-Main.blend except Movie
3. Render Movie scene in lib/scenes/Location-Main.blend

## Eevee Reboot 2019
In late 2019 an Eevee reboot was produced

Dependencies:
* Blender v2.81

To Render use the included Makefile:
$ make movie

Typical time to render from scratch

real    148m32.513s
user    116m48.445s
sys     13m14.051s
