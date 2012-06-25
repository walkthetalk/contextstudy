fig_name=figclassdiag
tex_name=opencl-spec-zh

tex_deps=$(shell find . -type f -name \*.tex)
tex_deps+=$(shell find . -type f -name \*.bib)
tex_deps+=$(shell find . -type f -name \*.lua)
tex_deps+=$(shell find . -type f -name \*.mkiv)

all: $(fig_name)-1.pdf $(tex_name).pdf

clean:
	@rm -f $(fig_name).log $(fig_name).1 $(fig_name)-1.pdf
	@rm -f $(tex_name).tuc $(tex_name).log $(tex_name).pdf
	@rm -f $(tex_name).aux $(tex_name).bbl $(tex_name).blg $(tex_name).top

$(fig_name)-1.pdf: $(fig_name).mp
	mptopdf $(fig_name).mp

$(tex_name).pdf: $(tex_deps)
	context $(tex_name).tex

