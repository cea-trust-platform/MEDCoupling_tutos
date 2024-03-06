TO = beamer
# pdf html js

exec = pandoc
opt_common = -s -N # --embed-resources

ifeq ($(TO),beamer)
format = pdf
opt_beamer = --slide-level=2 -t beamer -V theme=CEA2023
exec_opt = $(exec) $(opt_common) $(filename) $(opt_beamer)
prefix = pres_
template_dir = ../templates/slidesCEA2023

else ifeq ($(TO),pdf)
format = pdf
exec_opt = $(exec) $(opt_common) $(filename)
prefix =

else ifeq ($(TO),js)
format = html
opt_js = -t revealjs --css=../templates/revealjs-CEA/dist/theme/CEA.css -V revealjs-url=../templates/revealjs-CEA --embed-resources
exec_opt = $(exec) $(opt_common) $(filename) $(opt_js)
prefix = pres_

endif

../install/$(prefix)%.$(format): ../src/%.md
ifdef template_dir
	cp -r ./$(template_dir)/* .
endif
	# creates dir if not already created
	mkdir -p ../install
	$(exec_opt) -o $@ $<

.PHONY: pres_1
pres_1: ../install/$(prefix)SALOMETraining_MEDCoupling.$(format)

.PHONY: pres_2
pres_2: ../install/$(prefix)2_medfile_io.$(format)

.PHONY: pres_3
pres_3: ../install/$(prefix)3_remapper.$(format)

.PHONY: all
all: pres_1 pres_2 pres_3

clean:
	-rm ../install/*pdf
	-rm ../install/*html
	-rm *.err

clean_all: clean
	cp Makefile /tmp/
	-rm -r *
	cp /tmp/Makefile .
