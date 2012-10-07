tex_name=examination

tex_deps=$(shell find . -type f -name \*.tex)
tex_deps+=$(shell find . -type f -name \*.bib)
tex_deps+=$(shell find . -type f -name \*.lua)
tex_deps+=$(shell find . -type f -name \*.mkiv)

all: $(tex_name).pdf

clean:
	@rm -f $(tex_name).tuc $(tex_name).log $(tex_name).pdf
	@rm -f $(tex_name).aux $(tex_name).bbl $(tex_name).blg $(tex_name).top

$(tex_name).pdf: $(tex_deps)
	context $(tex_name).tex

