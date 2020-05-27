help::
	#
	# Render Dominoes at Dusk
	# ========================================
	#

# ======================================
# Tools
BLENDER := /Applications/Blender.app/Contents/MacOS/Blender
ECHO := /bin/echo
MKDIR := /bin/mkdir
OPEN := open
RM := /bin/rm
TIMESTAMP := $(ECHO) -n TIMESTAMP: && date

# ======================================
# Directories
STILLS_DIR := stills

cache_ocean cache_ocean_wire cache_render $(STILLS_DIR):
	$(MKDIR) -p "$@"

# ======================================
# Files
CUTTING_ROOM := lib/scenes/Location-Main.blend
ENGINE := BLENDER_EEVEE
FOOTAGE := 	\
	cache_render/OceanRushMatrix0400.png \
	cache_render/OceanRush0500.png \
	cache_render/Timelapse0480.png \
	cache_render/TheFall1152.png
MOVIE := dominoesAtDusk0001-2640.mp4
MUSIC := DominoesAtDuskEeveeReboot.m4a
OCEAN := lib/objects/Ocean.blend
STILLS := $(STILLS_DIR)/AdamLatchem.png \
	$(STILLS_DIR)/DominoesAtDusk.png \
	$(STILLS_DIR)/Programming.png \
	$(STILLS_DIR)/TheGIMP.png \
	$(STILLS_DIR)/Rendering.png \
	$(STILLS_DIR)/多米諾骨牌在黃昏.png

cache_ocean_wire/disp_1000.exr: director.py $(OCEAN) | cache_ocean_wire
	$(TIMESTAMP)
	$(BLENDER) "$(OCEAN)" --python director.py -- Scene.Wireframe

cache_ocean/disp_1200.exr: director.py $(OCEAN) | cache_ocean
	$(TIMESTAMP)
	$(BLENDER) "$(OCEAN)" --python director.py -- OceanRushBake

cache_render/OceanRush0500.png: cache_ocean/disp_1200.exr | $(CUTTING_ROOM) cache_render
	$(TIMESTAMP)
	$(BLENDER) --background "$(CUTTING_ROOM)" --engine $(ENGINE) --scene OceanRush       --render-anim

cache_render/OceanRushMatrix0400.png: cache_ocean_wire/disp_1000.exr | $(CUTTING_ROOM) cache_render
	$(TIMESTAMP)
	$(BLENDER) --background "$(CUTTING_ROOM)" --engine $(ENGINE) --scene Scene.Wireframe --render-anim

cache_render/Timelapse0480.png: | $(CUTTING_ROOM) cache_render
	$(TIMESTAMP)
	$(BLENDER) --background "$(CUTTING_ROOM)" --engine $(ENGINE) --scene Timelapse       --render-anim

cache_render/TheFall1152.png: | $(CUTTING_ROOM) cache_render
	$(TIMESTAMP)
	$(BLENDER) --background "$(CUTTING_ROOM)" --engine $(ENGINE) --scene TheFall         --render-anim

$(STILLS):	| $(STILLS_DIR)

$(MOVIE):	$(FOOTAGE) $(MUSIC) $(STILLS) | $(CUTTING_ROOM)
	$(TIMESTAMP)
	$(BLENDER) --background "$(CUTTING_ROOM)" --engine $(ENGINE) --scene Movie           --render-anim

# ======================================
# The movie goal
help::
	# $$ make movie
	#    Render the movie

movie:	$(MOVIE)
	$(TIMESTAMP)
	$(OPEN) $(MOVIE)

# ======================================
# Clean directory
help::
	# $$ make clean
	#    Remove intermediate renders and caches

clean:
	$(TIMESTAMP)
	$(RM) -rf cache_ocean cache_ocean_wire cache_render

.PHONY: clean movie

help::
	#
