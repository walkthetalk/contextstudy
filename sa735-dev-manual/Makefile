tex_name="prd-sa735-dev-manual"

tex_deps=$(shell find . -type f -name \*.tex)

all: $(tex_name).pdf

clean:
	@rm -f $(tex_name).tuc $(tex_name).log $(tex_name).pdf

$(tex_name).pdf: $(tex_deps)
	context --purge $(tex_name).tex

