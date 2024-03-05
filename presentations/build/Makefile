TO = beamer
# pdf html js

exec = pandoc
pdf_reader = zathura
navigator = firefox
opt_common = -s -N # --embed-resources

ifeq ($(TO),beamer)
format = pdf
opt_beamer = --slide-level=2 -t beamer -V theme=CEA2023
exec_opt = $(exec) $(opt_common) $(filename) $(opt_beamer)
prefix = pres_
viewer = $(pdf_reader)
template_dir = ../templates/slidesCEA2023

else ifeq ($(TO),pdf)
format = pdf
exec_opt = $(exec) $(opt_common) $(filename)
prefix =
viewer = $(pdf_reader)

else ifeq ($(TO),js)
format = html
opt_js = -t revealjs --css=../templates/revealjs-CEA/dist/theme/CEA.css -V revealjs-url=../templates/revealjs-CEA --embed-resources
exec_opt = $(exec) $(opt_common) $(filename) $(opt_js)
prefix = pres_
viewer = $(navigator)

endif

../install/$(prefix)%.$(format): ../src/%.md
ifdef template_dir
	cp -r ./$(template_dir)/* .
endif
	$(exec_opt) -o $@ $<
	$(viewer) $@ &

.PHONY: pres_1
pres_1: ../install/$(prefix)SALOMETraining_MEDCoupling.$(format)

.PHONY: pres_2
pres_2: ../install/$(prefix)SALOMETraining_MEDLoader.$(format)

.PHONY: pres_3
pres_3: ../install/$(prefix)SALOMETraining_Interpolation.$(format)

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
