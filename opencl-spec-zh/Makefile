fig_name=figclassdiag
tex_name=opencl-spec-zh

tex_deps=$(shell find . -type f -name \*.tex)

all: $(fig_name)-1.pdf $(tex_name).pdf

clean:
	@rm -f $(fig_name).log $(fig_name).1 $(fig_name)-1.pdf
	@rm -f $(tex_name).tuc $(tex_name).log $(tex_name).pdf

$(fig_name)-1.pdf: $(fig_name).mp
	mptopdf $(fig_name).mp

$(tex_name).pdf: $(tex_deps)
	context $(tex_name).tex

